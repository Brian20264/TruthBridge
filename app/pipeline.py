import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from agent_a import ask_agent_a
from agent_b import ask_agent_b
from evidence import create_evidence
from resolver import resolve_conflict
from audit import build_audit_trail, collect_human_challenge
from claim_relation import analyze_claim_relation


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OMEGA_PLUGIN_DIR = PROJECT_ROOT / "omega_plugin"


def find_omega_repo() -> Path:
    """
    Find the Omega repository without depending on Brian's username/path.

    Priority:
    1. TRUTHBRIDGE_OMEGA_REPO environment variable
    2. ../PeTTa/repos/Omega relative to TruthBridge
    3. ../Omega relative to TruthBridge
    """

    configured = os.getenv("TRUTHBRIDGE_OMEGA_REPO")

    candidates = []

    if configured:
        candidates.append(Path(configured).expanduser())

    candidates.extend(
        [
            PROJECT_ROOT.parent / "PeTTa" / "repos" / "Omega",
            PROJECT_ROOT.parent / "Omega",
        ]
    )

    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()

    raise FileNotFoundError(
        "Omega repository not found. Set "
        "TRUTHBRIDGE_OMEGA_REPO to the Omega repository path."
    )


def find_omega_runner(omega_repo: Path) -> Path:
    """
    Find the Omega launcher.

    Priority:
    1. TRUTHBRIDGE_OMEGA_RUNNER environment variable
    2. <PeTTa>/run.sh for the current Omega repository layout
    3. <Omega repo>/run.sh
    """

    configured = os.getenv("TRUTHBRIDGE_OMEGA_RUNNER")

    candidates = []

    if configured:
        candidates.append(Path(configured).expanduser())

    candidates.extend(
        [
            omega_repo.parents[1] / "run.sh",
            omega_repo / "run.sh",
        ]
    )

    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()

    raise FileNotFoundError(
        "Omega run.sh not found. Set "
        "TRUTHBRIDGE_OMEGA_RUNNER to the Omega launcher path."
    )


def get_yes_no(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()

        if answer in {"y", "yes"}:
            return True

        if answer in {"n", "no"}:
            return False

        print("Please enter yes or no.")


def collect_evidence(agent_name: str, claim: str):
    print("\n" + "=" * 60)
    print(f"EVIDENCE VALIDATION FOR {agent_name.upper()}")
    print("=" * 60)

    print("\nClaim being evaluated:")
    print(claim)

    source = input(
        f"\nEvidence source for {agent_name}: "
    ).strip()

    source_type = input(
        "Source type "
        "(official/primary/academic/reputable/secondary/unknown): "
    ).strip().lower()

    evidence_text = input(
        "\nPaste the evidence text:\n"
    ).strip()

    supports_claim = get_yes_no(
        "\nDoes this evidence support this claim? (yes/no): "
    )

    return create_evidence(
        source=source,
        source_type=source_type,
        text=evidence_text,
        supports_claim=supports_claim,
    )


def print_agent_result(agent_name: str, result: dict):
    print(f"\n--- {agent_name.upper()} ---")
    print(json.dumps(result, indent=2))


def evidence_strength(score: float) -> str:
    if score >= 0.8:
        return "strong"

    if score >= 0.6:
        return "moderate"

    return "weak"


def run_omega_resolution(
    relationship: str,
    evidence_a_strength: str,
    evidence_b_strength: str,
) -> dict:
    """
    Execute the real TruthBridge MeTTa plugin through Omega.
    """

    try:
        omega_repo = find_omega_repo()
        omega_runner = find_omega_runner(omega_repo)
    except FileNotFoundError as error:
        return {
            "success": False,
            "outcome": None,
            "explanation": str(error),
            "raw_output": "",
        }

    omega_relationship_map = {
        "AGREE": "agree",
        "QUALIFY": "qualify",
        "CONTRADICT": "contradict",
        "UNRELATED": "unrelated",
    }

    omega_relationship = omega_relationship_map.get(
        relationship.upper(),
        "unknown",
    )

    omega_src = omega_repo / "src"

    metta_program = f'''!(import! &self {omega_src / "utils"})
!(import! &self {omega_src / "logger.py"})
!(import! &self {omega_src / "log"})
!(import! &self {omega_src / "plugin"})

!(initLogger)

!(loadPlugin (metta "truthbridge" "{OMEGA_PLUGIN_DIR}"))

!(truthbridge-resolve {omega_relationship} {evidence_a_strength} {evidence_b_strength})
'''

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".metta",
            delete=False,
            encoding="utf-8",
        ) as temp_file:
            temp_file.write(metta_program)
            temp_path = temp_file.name

        process = subprocess.run(
            ["/bin/bash", str(omega_runner), temp_path],
            cwd=str(omega_repo.parents[1]),
            capture_output=True,
            text=True,
            timeout=60,
        )

        output = (process.stdout or "") + "\n" + (process.stderr or "")

        matches = re.findall(
            r'\(truthbridge-result\s+(\S+)\s+"([^"]*)"\)',
            output,
        )

        if not matches:
            explanation = (
                "Omega returned no TruthBridge result."
            )

            if process.returncode != 0:
                explanation += (
                    f" Omega exited with code {process.returncode}."
                )

            return {
                "success": False,
                "outcome": None,
                "explanation": explanation,
                "raw_output": output[-4000:],
            }

        outcome, explanation = matches[-1]

        return {
            "success": True,
            "outcome": outcome,
            "explanation": explanation,
            "raw_output": output[-4000:],
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "outcome": None,
            "explanation": "Omega timed out after 60 seconds.",
            "raw_output": "",
        }

    except Exception as error:
        return {
            "success": False,
            "outcome": None,
            "explanation": str(error),
            "raw_output": "",
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def main():
    print("\n" + "=" * 60)
    print("                    TRUTHBRIDGE")
    print("              TWO AGENTS, ONE TRUTH")
    print("=" * 60)

    question = input("\nEnter a question: ").strip()

    if not question:
        print("Question cannot be empty.")
        return

    # --------------------------------------------------------
    # AGENT A
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("AGENT A")
    print("=" * 60)
    print("Running Agent A through ASI:One...")

    try:
        agent_a_result = ask_agent_a(question)

        print_agent_result(
            "Agent A",
            agent_a_result,
        )

    except Exception as error:
        print("\nAgent A failed:")
        print(error)
        return

    # --------------------------------------------------------
    # AGENT B
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("AGENT B")
    print("=" * 60)
    print("Running Agent B through ASI:One...")

    try:
        agent_b_result = ask_agent_b(question)

        print_agent_result(
            "Agent B",
            agent_b_result,
        )

    except Exception as error:
        print("\nAgent B failed:")
        print(error)
        return

    # --------------------------------------------------------
    # EXTRACT CLAIMS
    # --------------------------------------------------------

    claim_a = agent_a_result["claim"]
    claim_b = agent_b_result["claim"]

    # --------------------------------------------------------
    # CLAIM RELATIONSHIP
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CLAIM RELATIONSHIP")
    print("=" * 60)

    try:
        relation = analyze_claim_relation(
            claim_a=claim_a,
            claim_b=claim_b,
        )

        print(f"\nRelationship: {relation['relationship']}")
        print(f"\nExplanation:\n{relation['explanation']}")
        print(f"\nKey difference:\n{relation['key_difference']}")
        print(f"\nConfidence: {relation['confidence']}")

    except Exception as error:
        print("\nClaim relationship analysis failed:")
        print(error)

        relation = {
            "relationship": "UNRELATED",
            "explanation": "Relationship analysis was unavailable.",
            "key_difference": "",
            "confidence": 0.0,
        }

    # --------------------------------------------------------
    # CLAIM COMPARISON
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CLAIM COMPARISON")
    print("=" * 60)

    if claim_a.strip().lower() == claim_b.strip().lower():
        print("\nStatus: Claims have identical wording.")
    else:
        print("\nStatus: Claims are different.")

    # --------------------------------------------------------
    # EVIDENCE
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
    # PYTHON EVIDENCE RESOLUTION
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("EVIDENCE RESOLUTION")
    print("=" * 60)

    result = resolve_conflict(
        claim_a=claim_a,
        evidence_a=evidence_a,
        claim_b=claim_b,
        evidence_b=evidence_b,
        relationship=relation["relationship"],
    )

    print(f"\nRelationship: {result['relationship']}")
    print(f"Evidence A score: {result['evidence_a']['score']}")
    print(f"Evidence B score: {result['evidence_b']['score']}")
    print(f"Score difference: {result['score_difference']}")
    print(f"\nPython outcome: {result['outcome']}")
    print(f"\nExplanation:\n{result['resolution_explanation']}")

    # --------------------------------------------------------
    # OMEGA / METTA
    # --------------------------------------------------------

    evidence_a_strength = evidence_strength(
        result["evidence_a"]["score"]
    )

    evidence_b_strength = evidence_strength(
        result["evidence_b"]["score"]
    )

    print("\n" + "=" * 60)
    print("OMEGA / MeTTa RESOLUTION")
    print("=" * 60)

    print(f"\nRelationship sent to Omega: {relation['relationship']}")
    print(f"Agent A evidence strength: {evidence_a_strength}")
    print(f"Agent B evidence strength: {evidence_b_strength}")

    omega_result = run_omega_resolution(
        relationship=relation["relationship"],
        evidence_a_strength=evidence_a_strength,
        evidence_b_strength=evidence_b_strength,
    )

    if omega_result["success"]:
        print(f"\nOmega outcome: {omega_result['outcome']}")
        print(
            f"\nOmega explanation:\n"
            f"{omega_result['explanation']}"
        )
    else:
        print("\nOmega resolution failed.")
        print(omega_result["explanation"])

    # --------------------------------------------------------
    # HUMAN REVIEW
    # --------------------------------------------------------

    human_challenge = collect_human_challenge()

    # --------------------------------------------------------
    # FINAL AUDIT TRAIL
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL AUDIT TRAIL")
    print("=" * 60)

    print(
        build_audit_trail(
            result=result,
            omega_result=omega_result,
            human_challenge=human_challenge,
        )
    )


if __name__ == "__main__":
    main()
