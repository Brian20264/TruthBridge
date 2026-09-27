from agent_a import ask_agent_a
from agent_b import ask_agent_b
from resolver import resolve_conflict


def main():

    question = input("\nEnter a question: ")

    print("\nRunning Agent A...")
    agent_a_answer = ask_agent_a(question)

    print("\nRunning Agent B...")
    agent_b_answer = ask_agent_b(question)

    print("\nResolving disagreement...")
    resolution = resolve_conflict(
        question,
        agent_a_answer,
        agent_b_answer
    )

    print("\n==============================")
    print("        TRUTHBRIDGE")
    print("==============================")

    print("\n--- AGENT A ---")
    print(agent_a_answer)

    print("\n--- AGENT B ---")
    print(agent_b_answer)

    print("\n--- RESOLUTION ---")
    print(resolution)


if __name__ == "__main__":
    main()