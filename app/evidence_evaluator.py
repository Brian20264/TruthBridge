from typing import Dict

from evidence import Evidence


SOURCE_WEIGHTS = {
    "official": 1.00,
    "primary": 0.95,
    "academic": 0.90,
    "reputable": 0.80,
    "secondary": 0.65,
    "unknown": 0.40,
}


def evaluate_evidence(evidence: Evidence) -> Dict:
    """
    Evaluate a piece of evidence using transparent criteria.
    """

    source_type = evidence.source_type.lower().strip()

    source_quality = SOURCE_WEIGHTS.get(source_type, 0.40)

    # These values are supplied by the evidence-processing stage
    # and kept between 0 and 1.
    relevance = 1.0 if evidence.supports_claim else 0.5
    directness = 1.0 if evidence.supports_claim else 0.5
    freshness = 1.0

    score = (
        source_quality * 0.30
        + relevance * 0.30
        + directness * 0.25
        + freshness * 0.15
    )

    score = round(score, 3)

    if score >= 0.80:
        strength = "strong"
    elif score >= 0.60:
        strength = "moderate"
    else:
        strength = "weak"

    return {
        "source": evidence.source,
        "source_type": source_type,
        "evidence_text": evidence.text,
        "score": score,
        "strength": strength,
        "supports_claim": evidence.supports_claim,
        "criteria": {
            "source_quality": source_quality,
            "relevance": relevance,
            "directness": directness,
            "freshness": freshness,
        },
    }
