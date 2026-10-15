"""Fail-closed registry for tool proposals.

This module validates proposals only. It does not dispatch them or make an
approval decision. A trusted caller must load capabilities from current policy
and pass them here; values supplied by an agent are not authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Type

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ToolDenied(Exception):
    """A proposal cannot proceed; `reason` is safe to expose in an audit event."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


class ReadFileArguments(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    path: Annotated[str, Field(min_length=1, max_length=1024)]


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    schema_version: int
    capability: str
    arguments: Type[BaseModel]
    side_effect: bool


_REGISTRY: dict[str, ToolDefinition] = {
    "workspace.read_file": ToolDefinition(
        name="workspace.read_file",
        schema_version=1,
        capability="workspace:read",
        arguments=ReadFileArguments,
        side_effect=False,
    ),
}


def list_tools() -> tuple[ToolDefinition, ...]:
    """Return registered tools in a stable order; unsupported tools are absent."""
    return tuple(_REGISTRY[name] for name in sorted(_REGISTRY))


def validate_proposal(
    *,
    name: str,
    schema_version: int,
    arguments: object,
    allowed_capabilities: frozenset[str],
) -> tuple[ToolDefinition, BaseModel]:
    """Validate a proposal against a server-loaded capability set.

    No caller should derive `allowed_capabilities` from the proposal itself.
    """
    definition = _REGISTRY.get(name)
    if definition is None:
        raise ToolDenied("unknown_tool")
    if type(schema_version) is not int or schema_version != definition.schema_version:
        raise ToolDenied("unsupported_schema_version")
    if definition.capability not in allowed_capabilities:
        raise ToolDenied("capability_not_granted")
    if not isinstance(arguments, dict):
        raise ToolDenied("invalid_arguments")
    try:
        validated = definition.arguments.model_validate(arguments)
    except ValidationError:
        raise ToolDenied("invalid_arguments") from None
    return definition, validated
