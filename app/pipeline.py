import json

from agent_a import ask_agent_a
from agent_b import ask_agent_b
from evidence import create_evidence
from resolver import resolve_conflict
from audit import build_audit_trail


def get_yes_no(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()

        if answer in {"y", "yes"}:
            return True

        if answer in {"n", "no"}:
            return False

        print("Please enter yes or no.")


def collect_evidence(agent_name: str, claim: str):
    print("\n" + "=" * 50)
    print(f"EVIDENCE FOR {agent_name.upper()}")
    print("=" * 50)

    print("\nClaim:")
    print(claim)

    source = input("\nEvidence source: ").strip()
    source_type = input(
        "Source type "
        "(official/primary/academic/reputable/secondary/unknown): "
    ).strip()

    evidence_text = input("\nPaste the evidence text: ").strip()

    supports_claim = get_yes_no(
        "\nDoes this evidence support this agent's claim? (yes/no): "
    )

    return create_evidence(
        source=source,
        source_type=source_type,
        text=evidence_text,
        supports_claim=supports_claim,
    )


def main():
    print("\n==========================================")
    print("             TRUTHBRIDGE")
    print("       MULTI-AGENT RESOLUTION")
    print("==========================================")

    question = input("\nEnter a question: ").strip()

    if not question:
        print("Question cannot be empty.")
        return

    # --------------------------------------------------------
    # AGENT A
    # --------------------------------------------------------

    print("\nRunning Agent A...")

    agent_a_result = ask_agent_a(question)

    print("\n--- AGENT A ---")
    print(json.dumps(agent_a_result, indent=2))

    # --------------------------------------------------------
    # AGENT B
    # --------------------------------------------------------

    print("\nRunning Agent B...")

    agent_b_result = ask_agent_b(question)

    print("\n--- AGENT B ---")
    print(json.dumps(agent_b_result, indent=2))

    # --------------------------------------------------------
    # DETECT DIFFERENT CLAIMS
    # --------------------------------------------------------

    claim_a = agent_a_result["claim"]
    claim_b = agent_b_result["claim"]

    print("\n--- CLAIM COMPARISON ---")

    if claim_a.strip().lower() == claim_b.strip().lower():
        print("Status: Agents agree on the wording of their claims.")
    else:
        print("Status: Agents produced different claims.")

    # --------------------------------------------------------
    # COLLECT ACTUAL EVIDENCE
    # --------------------------------------------------------

    evidence_a = collect_evidence(
        "Agent A",
        claim_a,
    )

    evidence_b = collect_evidence(
        "Agent B",
        claim_b,
    )

    # --------------------------------------------------------
    # RESOLVE THE CONFLICT
    # --------------------------------------------------------

    print("\nResolving claims using the evidence engine...")

    result = resolve_conflict(
        claim_a=claim_a,
        evidence_a=evidence_a,
        claim_b=claim_b,
        evidence_b=evidence_b,
    )

    # --------------------------------------------------------
    # DISPLAY RESOLUTION
    # --------------------------------------------------------

    print("\n==========================================")
    print("               RESOLUTION")
    print("==========================================")

    print("\nClaim A:")
    print(result["claim_a"])

    print("\nClaim B:")
    print(result["claim_b"])

    print("\nEvidence A score:")
    print(result["evidence_a"]["score"])

    print("\nEvidence B score:")
    print(result["evidence_b"]["score"])

    print("\nScore difference:")
    print(result["score_difference"])

    print("\nOutcome:")
    print(result["outcome"])

    # --------------------------------------------------------
    # AUDIT TRAIL
    # --------------------------------------------------------

    print("\n")
    print(build_audit_trail(result))


if __name__ == "__main__":
    main()
