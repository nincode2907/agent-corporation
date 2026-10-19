import pytest
from pydantic import ValidationError

from agent_corporation_api.modules.quality.contracts import (
    EvaluationCase,
    EvaluationSuite,
    QualityContractInvalid,
    Sample,
    compare_candidates,
    evaluate_deterministic,
    summarize_candidate,
)


HASH_A = "a" * 64
HASH_B = "b" * 64
HASH_C = "c" * 64
CONSTRAINTS = "d" * 64


def suite():
    return EvaluationSuite(
        suite_ref="suite:release", version="v1", dataset_sha256=HASH_A,
        evaluator_version="sha256-match-v1", constraints_sha256=CONSTRAINTS,
        cases=(
            EvaluationCase(case_id="case:pass", input_sha256=HASH_B, expected_sha256=HASH_C, evaluator_ref="evaluator:sha"),
            EvaluationCase(case_id="case:fail", input_sha256=HASH_C, expected_sha256=HASH_A, evaluator_ref="evaluator:sha"),
        ),
    )


def samples(profile, outcomes, *, suite_hash="e" * 64):
    return tuple(Sample(sample_ref=f"sample:{profile}-{i}", profile_ref=f"profile:{profile}", evidence_ref=f"artifact:{profile}-{i}",
                        constraints_sha256=CONSTRAINTS, suite_manifest_sha256=suite_hash,
                        outcome=outcome, latency_ms=(i + 1) * 100, intervention=False)
                 for i, outcome in enumerate(outcomes))


def test_suite_has_stable_versioned_manifest_and_deterministic_evaluator_uses_fixture_hashes():
    current = suite()
    one = evaluate_deterministic(current, {"case:pass": HASH_C, "case:fail": HASH_B},
                                 evidence_refs={"case:pass": "artifact:pass", "case:fail": "artifact:fail"})
    two = evaluate_deterministic(current, {"case:pass": HASH_C, "case:fail": HASH_B},
                                 evidence_refs={"case:pass": "artifact:pass", "case:fail": "artifact:fail"})
    assert one.suite_manifest_sha256 == current.manifest_sha256 == two.suite_manifest_sha256
    assert [result.outcome for result in one.results] == ["pass", "fail"]


def test_evaluator_requires_exact_evidence_for_observed_cases():
    with pytest.raises(QualityContractInvalid, match="case_or_evidence_set_mismatch"):
        evaluate_deterministic(suite(), {"case:pass": HASH_C}, evidence_refs={})
    with pytest.raises(ValidationError, match="duplicate_evaluation_case"):
        EvaluationSuite(suite_ref="suite:x", version="1", dataset_sha256=HASH_A,
                        evaluator_version="e1", constraints_sha256=CONSTRAINTS,
                        cases=(suite().cases[0], suite().cases[0]))
    with pytest.raises(QualityContractInvalid, match="required_evaluation_case_missing"):
        evaluate_deterministic(suite(), {"case:pass": HASH_C}, evidence_refs={"case:pass": "artifact:pass"})


def test_benchmark_summary_has_denominator_unknown_coverage_latency_and_uncertainty():
    rows = samples("a", ["success", "failure", "unknown", "success"])
    summary = summarize_candidate(rows, minimum_sample_size=3, expected_suite_hash="e" * 64,
                                  expected_constraints_hash=CONSTRAINTS)
    assert summary.sample_size == 4
    assert summary.denominator_count == 3 and summary.success_count == 2 and summary.unknown_count == 1
    assert summary.first_pass_rate == pytest.approx(2 / 3)
    assert summary.p50_latency_ms == 200 and summary.p95_latency_ms == 400
    assert summary.confidence_interval_95 is not None
    assert summary.sufficient_sample is True


def test_small_or_mismatched_sample_cannot_publish_a_winner():
    assert compare_candidates((samples("a", ["success"]), samples("b", ["failure"])),
                              minimum_sample_size=3, expected_suite_hash="e" * 64,
                              expected_constraints_hash=CONSTRAINTS).proposed_winner is None
    with pytest.raises(QualityContractInvalid, match="benchmark_constraints_mismatch"):
        summarize_candidate(samples("a", ["success"], suite_hash="f" * 64), minimum_sample_size=1,
                            expected_suite_hash="e" * 64, expected_constraints_hash=CONSTRAINTS)


def test_tournament_needs_non_overlapping_uncertainty_and_never_mutates_config():
    comparison = compare_candidates((samples("a", ["success"] * 100), samples("b", ["failure"] * 100)),
                                    minimum_sample_size=50, expected_suite_hash="e" * 64,
                                    expected_constraints_hash=CONSTRAINTS)
    assert comparison.proposed_winner == "profile:a"
    assert comparison.owner_approval_required and comparison.config_mutated is False


def test_tournament_derives_summary_from_raw_samples_not_caller_supplied_claims():
    single_a = samples("a", ["success"])
    single_b = samples("b", ["failure"])
    comparison = compare_candidates((single_a, single_b), minimum_sample_size=50,
                                    expected_suite_hash="e" * 64,
                                    expected_constraints_hash=CONSTRAINTS)
    assert comparison.proposed_winner is None
    assert all(item.sample_size == 1 and not item.sufficient_sample for item in comparison.summaries)


def test_duplicate_sample_or_evidence_refs_cannot_inflate_tournament_sample_size():
    one = samples("a", ["success"])[0]
    repeated = (one,) * 50
    with pytest.raises(QualityContractInvalid, match="duplicate_candidate_sample_ref"):
        summarize_candidate(repeated, minimum_sample_size=50, expected_suite_hash="e" * 64,
                            expected_constraints_hash=CONSTRAINTS)
    other = samples("b", ["failure"])[0]
    with pytest.raises(QualityContractInvalid, match="duplicate_tournament_sample_ref"):
        compare_candidates((repeated, (other,)), minimum_sample_size=1,
                           expected_suite_hash="e" * 64, expected_constraints_hash=CONSTRAINTS)
