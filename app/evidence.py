from dataclasses import dataclass


@dataclass
class Evidence:
    """
    Represents a real piece of evidence supplied to TruthBridge.
    """

    source: str
    source_type: str
    text: str
    supports_claim: bool


def create_evidence(
    source: str,
    source_type: str,
    text: str,
    supports_claim: bool,
) -> Evidence:

    if not source.strip():
        raise ValueError("Evidence source cannot be empty.")

    if not text.strip():
        raise ValueError("Evidence text cannot be empty.")

    return Evidence(
        source=source,
        source_type=source_type,
        text=text,
        supports_claim=supports_claim,
    )
