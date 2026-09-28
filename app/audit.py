from typing import Dict


def build_audit_trail(result: Dict) -> str:
    """
    Build a human-readable audit trail showing
    how TruthBridge reached its resolution.
    """

    evidence_a = result["evidence_a"]
    evidence_b = result["evidence_b"]

    lines = []

    lines.append("=" * 50)
    lines.append("          TRUTHBRIDGE AUDIT TRAIL")
    lines.append("=" * 50)

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

    lines.append("\nCOMPARISON")
    lines.append(
        f"Evidence score difference: "
        f"{result['score_difference']}"
    )

    lines.append("\nRESOLUTION")
    lines.append(result["outcome"])

    lines.append("\nREASONING")
    lines.append(
        "The resolution was produced by comparing the "
        "explicit evidence criteria for both claims."
    )

    lines.append("\nHUMAN CHALLENGE")
    lines.append(
        "A human reviewer can inspect the claims, evidence, "
        "criteria, and resolution and provide new evidence "
        "to challenge the result."
    )

    lines.append("=" * 50)

    return "\n".join(lines)
