from evidence import create_evidence
from evidence_evaluator import evaluate_evidence


def main():
    evidence = create_evidence(
        source="Official University Policy",
        source_type="official",
        text="Students must satisfy the stated prerequisite before registration.",
        supports_claim=True,
    )

    result = evaluate_evidence(evidence)

    print("\n=== TRUTHBRIDGE EVIDENCE TEST ===")
    print("Source:", result["source"])
    print("Type:", result["source_type"])
    print("Evidence:", result["evidence_text"])
    print("Score:", result["score"])
    print("Strength:", result["strength"])
    print("Supports claim:", result["supports_claim"])
    print("Criteria:", result["criteria"])


if __name__ == "__main__":
    main()
