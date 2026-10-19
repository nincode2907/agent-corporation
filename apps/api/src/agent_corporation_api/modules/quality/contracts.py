"""Versioned deterministic evaluation contracts; never mutates model config."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class QualityContractInvalid(ValueError):
    pass


class EvaluationCase(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    case_id: str = Field(min_length=1, max_length=120)
    input_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    expected_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    evaluator_ref: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    required: bool = True


class EvaluationSuite(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    suite_ref: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    version: str = Field(min_length=1, max_length=120)
    dataset_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    evaluator_version: str = Field(min_length=1, max_length=120)
    environment: Literal["benchmark"] = "benchmark"
    constraints_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    cases: tuple[EvaluationCase, ...] = Field(min_length=1, max_length=10000)

    @model_validator(mode="after")
    def cases_are_unique_and_nonempty(self) -> "EvaluationSuite":
        ids = [case.case_id for case in self.cases]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate_evaluation_case")
        if not any(case.required for case in self.cases):
            raise ValueError("suite_requires_required_case")
        return self

    @property
    def manifest_sha256(self) -> str:
        data = self.model_dump(mode="json")
        return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class CaseEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    case_id: str
    outcome: Literal["pass", "fail", "unknown", "human_review"]
    observed_sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    evidence_ref: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    human_review_ref: str | None = None

    @model_validator(mode="after")
    def review_is_explicit(self) -> "CaseEvaluation":
        if self.outcome == "human_review" and not self.human_review_ref:
            raise ValueError("human_review_requires_reviewer_evidence")
        if self.outcome != "human_review" and self.human_review_ref is not None:
            raise ValueError("unexpected_human_review_reference")
        return self


class SuiteEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    suite_ref: str
    suite_version: str
    suite_manifest_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    results: tuple[CaseEvaluation, ...] = Field(min_length=1)


def evaluate_deterministic(suite: EvaluationSuite, observed_by_case: dict[str, str], *, evidence_refs: dict[str, str]) -> SuiteEvaluation:
    """Compare fixture output hashes to expected hashes; no model judge involved."""
    cases = {case.case_id: case for case in suite.cases}
    if set(observed_by_case) - set(cases) or set(evidence_refs) != set(observed_by_case):
        raise QualityContractInvalid("evaluation_case_or_evidence_set_mismatch")
    if not observed_by_case:
        raise QualityContractInvalid("evaluation_results_required")
    required_ids = {case.case_id for case in suite.cases if case.required}
    if not required_ids.issubset(observed_by_case):
        raise QualityContractInvalid("required_evaluation_case_missing")
    results = []
    for case_id, observed in observed_by_case.items():
        if len(observed) != 64 or any(char not in "0123456789abcdef" for char in observed):
            raise QualityContractInvalid("invalid_observed_hash")
        case = cases[case_id]
        results.append(CaseEvaluation(
            case_id=case_id,
            outcome="pass" if observed == case.expected_sha256 else "fail",
            observed_sha256=observed,
            evidence_ref=evidence_refs[case_id],
        ))
    return SuiteEvaluation(suite_ref=suite.suite_ref, suite_version=suite.version,
                           suite_manifest_sha256=suite.manifest_sha256, results=tuple(results))


class Sample(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    sample_ref: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    profile_ref: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    evidence_ref: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    constraints_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    suite_manifest_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    outcome: Literal["success", "failure", "unknown"]
    latency_ms: int | None = Field(default=None, ge=0)
    intervention: bool | None = None


class CandidateSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    profile_ref: str
    sample_size: int = Field(ge=0)
    denominator_count: int = Field(ge=0)
    success_count: int = Field(ge=0)
    unknown_count: int = Field(ge=0)
    first_pass_rate: float | None
    p50_latency_ms: int | None
    p95_latency_ms: int | None
    intervention_rate: float | None
    confidence_interval_95: tuple[float, float] | None
    sufficient_sample: bool


def summarize_candidate(samples: tuple[Sample, ...], *, minimum_sample_size: int, expected_suite_hash: str, expected_constraints_hash: str) -> CandidateSummary:
    if type(minimum_sample_size) is not int or minimum_sample_size < 1:
        raise QualityContractInvalid("minimum_sample_size_must_be_positive")
    if not samples:
        raise QualityContractInvalid("candidate_samples_required")
    if len({sample.sample_ref for sample in samples}) != len(samples):
        raise QualityContractInvalid("duplicate_candidate_sample_ref")
    if len({sample.evidence_ref for sample in samples}) != len(samples):
        raise QualityContractInvalid("duplicate_candidate_evidence_ref")
    profiles = {s.profile_ref for s in samples}
    if len(profiles) != 1:
        raise QualityContractInvalid("candidate_profile_mismatch")
    if any(s.suite_manifest_sha256 != expected_suite_hash or s.constraints_sha256 != expected_constraints_hash for s in samples):
        raise QualityContractInvalid("benchmark_constraints_mismatch")
    eligible = [s for s in samples if s.outcome != "unknown"]
    successes = sum(s.outcome == "success" for s in eligible)
    rate = successes / len(eligible) if eligible else None
    latencies = sorted(s.latency_ms for s in samples if s.latency_ms is not None)
    interventions = [s.intervention for s in samples if s.intervention is not None]
    ci = _wilson_interval(successes, len(eligible)) if eligible else None
    enough = len(eligible) >= minimum_sample_size
    return CandidateSummary(
        profile_ref=next(iter(profiles)), sample_size=len(samples), denominator_count=len(eligible),
        success_count=successes, unknown_count=len(samples) - len(eligible),
        first_pass_rate=rate, p50_latency_ms=_nearest_rank(latencies, .50),
        p95_latency_ms=_nearest_rank(latencies, .95),
        intervention_rate=(sum(interventions) / len(interventions)) if interventions else None,
        confidence_interval_95=ci, sufficient_sample=enough,
    )


class TournamentComparison(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    summaries: tuple[CandidateSummary, ...] = Field(min_length=2)
    proposed_winner: str | None
    owner_approval_required: Literal[True] = True
    config_mutated: Literal[False] = False


def compare_candidates(
    candidates: tuple[tuple[Sample, ...], ...], *, minimum_sample_size: int,
    expected_suite_hash: str, expected_constraints_hash: str,
) -> TournamentComparison:
    """Derive summaries from raw evidence-bearing samples; do not trust caller summaries."""
    if type(minimum_sample_size) is not int or minimum_sample_size < 1:
        raise QualityContractInvalid("minimum_sample_size_must_be_positive")
    if len(candidates) < 2:
        raise QualityContractInvalid("tournament_requires_two_candidates")
    all_samples = [sample for candidate in candidates for sample in candidate]
    if len({sample.sample_ref for sample in all_samples}) != len(all_samples):
        raise QualityContractInvalid("duplicate_tournament_sample_ref")
    if len({sample.evidence_ref for sample in all_samples}) != len(all_samples):
        raise QualityContractInvalid("duplicate_tournament_evidence_ref")
    summaries = tuple(
        summarize_candidate(
            rows, minimum_sample_size=minimum_sample_size,
            expected_suite_hash=expected_suite_hash,
            expected_constraints_hash=expected_constraints_hash,
        )
        for rows in candidates
    )
    if len({item.profile_ref for item in summaries}) != len(summaries):
        raise QualityContractInvalid("duplicate_tournament_profile")
    proposed = None
    if all(item.denominator_count >= minimum_sample_size and item.confidence_interval_95 is not None for item in summaries):
        ordered = sorted(summaries, key=lambda item: item.first_pass_rate or 0, reverse=True)
        leader, runner_up = ordered[0], ordered[1]
        assert leader.confidence_interval_95 and runner_up.confidence_interval_95
        if leader.confidence_interval_95[0] > runner_up.confidence_interval_95[1]:
            proposed = leader.profile_ref
    return TournamentComparison(summaries=summaries, proposed_winner=proposed)


def _nearest_rank(values: list[int], quantile: float) -> int | None:
    if not values:
        return None
    return values[max(0, math.ceil(quantile * len(values)) - 1)]


def _wilson_interval(successes: int, count: int) -> tuple[float, float]:
    z = 1.96
    p = successes / count
    denominator = 1 + z * z / count
    center = (p + z * z / (2 * count)) / denominator
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * count)) / count) / denominator
    return max(0.0, center - margin), min(1.0, center + margin)
