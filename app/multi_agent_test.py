from agent_a import ask_agent_a
from agent_b import ask_agent_b
import json


def main():
    question = input("\nEnter a question: ").strip()

    if not question:
        print("Please enter a question.")
        return

    print("\nRunning Agent A...")
    result_a = ask_agent_a(question)

    print("\nRunning Agent B...")
    result_b = ask_agent_b(question)

    print("\n==============================")
    print("      TRUTHBRIDGE")
    print("      TWO-AGENT TEST")
    print("==============================")

    print("\n--- AGENT A ---")
    print(json.dumps(result_a, indent=2))

    print("\n--- AGENT B ---")
    print(json.dumps(result_b, indent=2))

    print("\n--- COMPARISON ---")

    if result_a["claim"].strip().lower() == result_b["claim"].strip().lower():
        print("Status: Agents agree.")
    else:
        print("Status: Agents have different claims.")

    print("\nAgent A claim:")
    print(result_a["claim"])

    print("\nAgent B claim:")
    print(result_b["claim"])


if __name__ == "__main__":
    main()
