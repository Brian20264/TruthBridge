from typing import Dict

from evidence import Evidence
from evidence_evaluator import evaluate_evidence
from audit import build_audit_trail


def resolve_conflict(
    claim_a: str,
    evidence_a: Evidence,
    claim_b: str,
    evidence_b: Evidence,
) -> Dict:
    """
    Compare two competing claims using their evidence,
    then produce a resolution and audit information.
    """

    # Evaluate the evidence for both claims
    evaluated_a = evaluate_evidence(evidence_a)
    evaluated_b = evaluate_evidence(evidence_b)

    score_a = evaluated_a["score"]
    score_b = evaluated_b["score"]

    # Determine the resolution
    if not evidence_a.supports_claim and not evidence_b.supports_claim:
        outcome = "INSUFFICIENT_EVIDENCE"

    elif abs(score_a - score_b) < 0.05:
        outcome = "UNRESOLVED"

    elif score_a > score_b and evidence_a.supports_claim:
        outcome = "CLAIM_A_BETTER_SUPPORTED"

    elif score_b > score_a and evidence_b.supports_claim:
        outcome = "CLAIM_B_BETTER_SUPPORTED"

    else:
        outcome = "UNRESOLVED"

    return {
        "claim_a": claim_a,
        "claim_b": claim_b,
        "evidence_a": evaluated_a,
        "evidence_b": evaluated_b,
        "score_difference": round(abs(score_a - score_b), 3),
        "outcome": outcome,
    }


def main():
    """
    Demonstration of the TruthBridge resolution system.
    """

    claim_a = "The student satisfies the prerequisite."

    claim_b = "The student does not satisfy the prerequisite."

    evidence_a = Evidence(
        source="Official University Policy",
        source_type="official",
        text=(
            "The official university policy states that "
            "the student satisfies the prerequisite."
        ),
        supports_claim=True,
    )

    evidence_b = Evidence(
        source="Unverified Website",
        source_type="unknown",
        text=(
            "An unverified website claims that the "
            "student does not satisfy the prerequisite."
        ),
        supports_claim=False,
    )

    result = resolve_conflict(
        claim_a,
        evidence_a,
        claim_b,
        evidence_b,
    )

    print("\n========================================")
    print("          TRUTHBRIDGE RESOLVER")
    print("========================================")

    print("\nCLAIM A:")
    print(result["claim_a"])

    print("\nCLAIM B:")
    print(result["claim_b"])

    print("\nEVIDENCE A SCORE:")
    print(result["evidence_a"]["score"])

    print("\nEVIDENCE B SCORE:")
    print(result["evidence_b"]["score"])

    print("\nSCORE DIFFERENCE:")
    print(result["score_difference"])

    print("\nOUTCOME:")
    print(result["outcome"])

    print("\n")
    print(build_audit_trail(result))


if __name__ == "__main__":
    main()
