"""Pure contracts for deterministic routing and bounded subtask DAGs.

The caller must supply limits loaded from trusted policy. This module validates
plans only; it does not create tasks, reserve budget, start agents, or dispatch
tools. Those operations remain blocked until the upstream executor is ready.
"""
from __future__ import annotations

import re
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrchestrationInvalid(ValueError):
    pass


class RoutingPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    simple_task_max_steps: int = Field(ge=1, le=100)
    max_task_steps: int = Field(ge=1, le=1000)
    max_workers: int = Field(ge=1, le=16)
    delegation_enabled: bool


class RoutingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    estimated_steps: int = Field(ge=1, le=1000)
    required_roles: int = Field(ge=1, le=16)


def route_task(request: RoutingRequest, policy: RoutingPolicy) -> Literal["direct", "supervisor", "blocked"]:
    """Choose one route deterministically; this function never invokes agents."""
    needs_delegation = (
        request.estimated_steps > policy.simple_task_max_steps
        or request.required_roles > 1
    )
    if not needs_delegation:
        return "direct"
    if (
        not policy.delegation_enabled
        or request.estimated_steps > policy.max_task_steps
        or request.required_roles > policy.max_workers
    ):
        return "blocked"
    return "supervisor"


class SubtaskNode(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    id: UUID
    parent_id: UUID
    dependencies: list[UUID] = Field(default_factory=list, max_length=32)
    employee_version_id: UUID | None = None
    iteration: int = Field(default=1, ge=1, le=100)


class DelegationPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    environment_id: UUID
    company_id: UUID
    parent_task_id: UUID
    correlation_id: UUID
    nodes: list[SubtaskNode] = Field(min_length=1, max_length=128)

    @field_validator("nodes")
    @classmethod
    def node_ids_are_unique(cls, nodes: list[SubtaskNode]) -> list[SubtaskNode]:
        ids = [node.id for node in nodes]
        if len(ids) != len(set(ids)):
            raise ValueError("subtask IDs must be unique")
        return nodes


@dataclass(frozen=True)
class DelegationLimits:
    max_nodes: int
    max_fanout: int
    max_depth: int
    max_iterations: int

    def validate(self) -> None:
        values = (self.max_nodes, self.max_fanout, self.max_depth, self.max_iterations)
        if any(type(value) is not int for value in values):
            raise OrchestrationInvalid("limits_must_be_integers")
        if not 1 <= self.max_nodes <= 128:
            raise OrchestrationInvalid("invalid_max_nodes")
        if not 1 <= self.max_fanout <= self.max_nodes:
            raise OrchestrationInvalid("invalid_max_fanout")
        if not 1 <= self.max_depth <= self.max_nodes:
            raise OrchestrationInvalid("invalid_max_depth")
        if not 1 <= self.max_iterations <= 100:
            raise OrchestrationInvalid("invalid_max_iterations")


def validate_delegation_plan(plan: DelegationPlan, limits: DelegationLimits) -> tuple[UUID, ...]:
    """Validate parent/dependency DAG and return stable topological order."""
    limits.validate()
    nodes = {node.id: node for node in plan.nodes}
    if len(nodes) > limits.max_nodes:
        raise OrchestrationInvalid("node_limit_exceeded")
    if plan.parent_task_id in nodes:
        raise OrchestrationInvalid("parent_task_reused_as_subtask")

    children: dict[UUID, list[UUID]] = defaultdict(list)
    incoming: dict[UUID, set[UUID]] = {node_id: set() for node_id in nodes}
    outgoing: dict[UUID, set[UUID]] = {node_id: set() for node_id in nodes}
    indegree = {node_id: 0 for node_id in nodes}

    def add_edge(source: UUID, target: UUID) -> None:
        if source == plan.parent_task_id:
            return
        if source not in nodes:
            raise OrchestrationInvalid("unknown_parent_or_dependency")
        if source == target:
            raise OrchestrationInvalid("cyclic_delegation_plan")
        if target not in outgoing[source]:
            outgoing[source].add(target)
            incoming[target].add(source)
            indegree[target] += 1

    for node in plan.nodes:
        if node.parent_id != plan.parent_task_id and node.parent_id not in nodes:
            raise OrchestrationInvalid("unknown_parent_or_dependency")
        children[node.parent_id].append(node.id)
        add_edge(node.parent_id, node.id)
        if node.iteration > limits.max_iterations:
            raise OrchestrationInvalid("iteration_limit_exceeded")
        if len(node.dependencies) != len(set(node.dependencies)):
            raise OrchestrationInvalid("duplicate_dependency")
        for dependency in node.dependencies:
            if dependency not in nodes:
                raise OrchestrationInvalid("unknown_parent_or_dependency")
            add_edge(dependency, node.id)

    if any(len(items) > limits.max_fanout for items in children.values()):
        raise OrchestrationInvalid("fanout_limit_exceeded")

    ready = deque(sorted((node_id for node_id, degree in indegree.items() if degree == 0), key=str))
    order: list[UUID] = []
    depth: dict[UUID, int] = {}
    while ready:
        node_id = ready.popleft()
        node = nodes[node_id]
        predecessors = incoming[node_id]
        if node.parent_id == plan.parent_task_id:
            node_depth = 1 + max((depth[item] for item in predecessors), default=0)
        else:
            parent_depth = depth.get(node.parent_id)
            if parent_depth is None:
                raise OrchestrationInvalid("cyclic_delegation_plan")
            node_depth = parent_depth + 1
        node_depth = max(node_depth, 1 + max((depth[item] for item in predecessors), default=0))
        if node_depth > limits.max_depth:
            raise OrchestrationInvalid("depth_limit_exceeded")
        depth[node_id] = node_depth
        order.append(node_id)
        for child_id in sorted(outgoing[node_id], key=str):
            indegree[child_id] -= 1
            if indegree[child_id] == 0:
                ready.append(child_id)

    if len(order) != len(nodes):
        raise OrchestrationInvalid("cyclic_delegation_plan")
    return tuple(order)


class Handoff(BaseModel):
    """Explicit evidence handoff metadata; payloads/artifacts stay elsewhere."""
    model_config = ConfigDict(extra="forbid", strict=True)

    parent_task_id: UUID
    subtask_id: UUID
    correlation_id: UUID
    from_employee_version_id: UUID
    to_employee_version_id: UUID
    decision_summary: str = Field(min_length=1, max_length=2000)
    evidence_refs: list[str] = Field(min_length=1, max_length=50)

    @field_validator("decision_summary")
    @classmethod
    def summary_is_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("decision_summary must not be blank")
        return value

    @field_validator("evidence_refs")
    @classmethod
    def refs_are_opaque(cls, values: list[str]) -> list[str]:
        for value in values:
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", value) or ".." in value:
                raise ValueError("evidence refs must be scoped opaque references")
        return values
