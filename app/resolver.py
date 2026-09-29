from evidence_evaluator import evaluate_evidence


def resolve_conflict(
    claim_a: str,
    evidence_a,
    claim_b: str,
    evidence_b,
    relationship: str,
):
    evidence_result_a = evaluate_evidence(evidence_a)
    evidence_result_b = evaluate_evidence(evidence_b)

    score_a = evidence_result_a["score"]
    score_b = evidence_result_b["score"]
    score_difference = abs(score_a - score_b)

    relationship = relationship.upper().strip()

    outcome = "UNRESOLVED"
    explanation = ""

    if relationship == "AGREE":
        outcome = "AGREEMENT"
        explanation = (
            "Both agents produced claims that are consistent with each other."
        )

    elif relationship == "UNRELATED":
        outcome = "UNRELATED_CLAIMS"
        explanation = (
            "The two claims do not address the same proposition closely enough "
            "to resolve them as competing claims."
        )

    elif relationship == "QUALIFY":
        if score_difference < 0.10:
            outcome = "QUALIFICATION_UNRESOLVED"
            explanation = (
                "The claims are compatible as a qualification of the same issue, "
                "but the available evidence does not clearly establish which "
                "qualification should dominate."
            )
        elif score_a > score_b:
            outcome = "CLAIM_A_PRIMARY_WITH_QUALIFICATION"
            explanation = (
                "The claims qualify one another, but Agent A's claim has the "
                "stronger supporting evidence."
            )
        else:
            outcome = "CLAIM_B_PRIMARY_WITH_QUALIFICATION"
            explanation = (
                "The claims qualify one another, but Agent B's claim has the "
                "stronger supporting evidence."
            )

    elif relationship == "CONTRADICT":
        if score_a >= 0.80 and score_b >= 0.80:
            outcome = "INSUFFICIENT_EVIDENCE"
            explanation = (
                "The claims contradict each other, but both sides have strong "
                "supporting evidence. The available evidence does not justify "
                "discarding either claim."
            )
        elif score_a >= 0.80 and score_b < 0.80:
            outcome = "CLAIM_A_BETTER_SUPPORTED"
            explanation = (
                "The claims contradict each other and Agent A has stronger "
                "supporting evidence."
            )
        elif score_b >= 0.80 and score_a < 0.80:
            outcome = "CLAIM_B_BETTER_SUPPORTED"
            explanation = (
                "The claims contradict each other and Agent B has stronger "
                "supporting evidence."
            )
        elif score_a > score_b:
            outcome = "CONDITIONAL_RESOLUTION"
            explanation = (
                "The claims contradict each other. Agent A has stronger "
                "supporting evidence, but the evidence is not strong enough "
                "for a definitive resolution."
            )
        elif score_b > score_a:
            outcome = "CONDITIONAL_RESOLUTION"
            explanation = (
                "The claims contradict each other. Agent B has stronger "
                "supporting evidence, but the evidence is not strong enough "
                "for a definitive resolution."
            )
        else:
            outcome = "UNRESOLVED"
            explanation = (
                "The claims contradict each other and the available evidence "
                "has equal strength."
            )

    else:
        outcome = "RELATIONSHIP_UNKNOWN"
        explanation = (
            f"Relationship '{relationship}' is not recognized by the "
            "evidence resolver."
        )

    return {
        "claim_a": claim_a,
        "claim_b": claim_b,
        "relationship": relationship,
        "evidence_a": evidence_result_a,
        "evidence_b": evidence_result_b,
        "score_difference": score_difference,
        "outcome": outcome,
        "resolution_explanation": explanation,
    }
