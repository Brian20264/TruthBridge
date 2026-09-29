from typing import Dict, Optional


def build_audit_trail(
    result: Dict,
    omega_result: Optional[Dict] = None,
    human_challenge: Optional[Dict] = None,
) -> str:
    """
    Build a human-readable audit trail showing:

    1. Agent A claim and evidence
    2. Agent B claim and evidence
    3. Evidence comparison
    4. Python resolution
    5. Omega/MeTTa resolution
    6. Human review/challenge status
    """

    evidence_a = result["evidence_a"]
    evidence_b = result["evidence_b"]

    lines = []

    lines.append("=" * 60)
    lines.append("              TRUTHBRIDGE AUDIT TRAIL")
    lines.append("=" * 60)

    # --------------------------------------------------------
    # CLAIM A
    # --------------------------------------------------------

    lines.append("\nCLAIM A")
    lines.append(result["claim_a"])

    lines.append("\nEVIDENCE A")
    lines.append(f"Source: {evidence_a['source']}")
    lines.append(f"Type: {evidence_a['source_type']}")
    lines.append(f"Evidence: {evidence_a['evidence_text']}")
    lines.append(
        f"Source quality: "
        f"{evidence_a['criteria']['source_quality']}"
    )
    lines.append(
        f"Relevance: "
        f"{evidence_a['criteria']['relevance']}"
    )
    lines.append(
        f"Directness: "
        f"{evidence_a['criteria']['directness']}"
    )
    lines.append(
        f"Freshness: "
        f"{evidence_a['criteria']['freshness']}"
    )
    lines.append(f"Overall score: {evidence_a['score']}")
    lines.append(
        f"Supports claim: "
        f"{evidence_a['supports_claim']}"
    )

    # --------------------------------------------------------
    # CLAIM B
    # --------------------------------------------------------

    lines.append("\nCLAIM B")
    lines.append(result["claim_b"])

    lines.append("\nEVIDENCE B")
    lines.append(f"Source: {evidence_b['source']}")
    lines.append(f"Type: {evidence_b['source_type']}")
    lines.append(f"Evidence: {evidence_b['evidence_text']}")
    lines.append(
        f"Source quality: "
        f"{evidence_b['criteria']['source_quality']}"
    )
    lines.append(
        f"Relevance: "
        f"{evidence_b['criteria']['relevance']}"
    )
    lines.append(
        f"Directness: "
        f"{evidence_b['criteria']['directness']}"
    )
    lines.append(
        f"Freshness: "
        f"{evidence_b['criteria']['freshness']}"
    )
    lines.append(f"Overall score: {evidence_b['score']}")
    lines.append(
        f"Supports claim: "
        f"{evidence_b['supports_claim']}"
    )

    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    lines.append("\nCOMPARISON")
    lines.append(
        f"Claim relationship: "
        f"{result['relationship']}"
    )
    lines.append(
        f"Evidence score difference: "
        f"{result['score_difference']}"
    )

    # --------------------------------------------------------
    # PYTHON RESOLUTION
    # --------------------------------------------------------

    lines.append("\nPYTHON EVIDENCE RESOLUTION")
    lines.append(result["outcome"])
    lines.append(result["resolution_explanation"])

    # --------------------------------------------------------
    # OMEGA / METTA RESOLUTION
    # --------------------------------------------------------

    lines.append("\nOMEGA / MeTTa RESOLUTION")

    if omega_result:
        if omega_result.get("success"):
            lines.append(
                f"Outcome: {omega_result.get('outcome')}"
            )
            lines.append(
                f"Explanation: "
                f"{omega_result.get('explanation')}"
            )
        else:
            lines.append("Outcome: Omega resolution failed.")
            lines.append(
                f"Explanation: "
                f"{omega_result.get('explanation')}"
            )
    else:
        lines.append("Omega result not recorded.")

    # --------------------------------------------------------
    # HUMAN REVIEW
    # --------------------------------------------------------

    lines.append("\nHUMAN REVIEW")

    if human_challenge is None:
        lines.append("Human review has not yet been recorded.")
    elif human_challenge.get("challenged"):
        lines.append("Status: CHALLENGED")
        lines.append(
            f"Challenge: "
            f"{human_challenge.get('reason', '')}"
        )
    else:
        lines.append("Status: ACCEPTED")
        lines.append(
            "The human reviewer did not challenge the resolution."
        )

    lines.append("=" * 60)

    return "\n".join(lines)


def collect_human_challenge() -> Dict:
    """
    Collect an explicit human review decision.

    The reviewer can accept the current resolution or challenge it.
    A challenge reason is recorded so the decision is auditable.
    """

    print("\n" + "=" * 60)
    print("                HUMAN REVIEW")
    print("=" * 60)

    while True:
        answer = input(
            "\nDo you accept this resolution? (yes/no): "
        ).strip().lower()

        if answer in {"yes", "y"}:
            return {
                "challenged": False,
                "reason": "",
            }

        if answer in {"no", "n"}:
            reason = input(
                "\nWhy are you challenging the resolution?\n"
                "Challenge reason: "
            ).strip()

            if not reason:
                reason = "Human reviewer challenged the resolution."

            return {
                "challenged": True,
                "reason": reason,
            }

        print("Please enter yes or no.")
