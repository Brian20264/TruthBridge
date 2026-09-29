def demo_agent_a(question: str) -> dict:
    return {
        "claim": (
            "Yes. The student can register for the course even without "
            "completing the prerequisite."
        ),
        "reasoning": (
            "Agent A takes the permissive interpretation of the question "
            "and assumes registration is allowed despite the missing prerequisite."
        ),
        "evidence_needed": [
            "University registration policy",
            "Prerequisite and exception rules"
        ],
        "uncertainty": (
            "The actual policy may allow or prohibit exceptions."
        ),
    }


def demo_agent_b(question: str) -> dict:
    return {
        "claim": (
            "No. The student cannot register for the course without "
            "completing the prerequisite."
        ),
        "reasoning": (
            "Agent B takes the restrictive interpretation and assumes "
            "the prerequisite is mandatory before registration."
        ),
        "evidence_needed": [
            "University registration policy",
            "Official prerequisite requirements"
        ],
        "uncertainty": (
            "An authorized exception or override may change the outcome."
        ),
        "challenge_to_other_agent": (
            "Agent A assumes registration is possible without establishing "
            "that an official exception exists."
        ),
    }
