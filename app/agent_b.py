import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("ASI_ONE_API_KEY"),
    base_url="https://api.asi1.ai/v1",
)


def ask_agent_b(question: str) -> dict:
    """
    Agent B:
    Independent skeptical counter-position analyst.

    Agent B tests the strongest default interpretation and looks
    specifically for assumptions that could make that interpretation
    incomplete, conditional, or wrong.
    """

    prompt = f"""
You are Agent B in TruthBridge.

Analyze this question independently:

{question}

Your role is the SKEPTICAL COUNTER-POSITION ANALYST.

Your responsibilities:
1. Identify the strongest reasonable interpretation of the question.
2. Test the default position that another analyst might reach.
3. Look specifically for hidden assumptions, exceptions, boundary conditions,
   policy dependence, ambiguous definitions, or missing facts.
4. Produce your own claim rather than simply repeating the expected answer.
5. When the available information supports a materially different conclusion,
   state that conclusion clearly and directly.
6. Explain the reasoning behind your claim.
7. Identify the evidence that would be needed to verify it.
8. Explain what evidence could prove your claim wrong.
9. State important uncertainty.
10. Never invent evidence, laws, policies, statistics, or sources.

Important:
- Do NOT automatically say "it depends" without explaining exactly what it
  depends on.
- Do NOT automatically agree with a conventional or majority answer.
- Do NOT manufacture disagreement merely for the sake of disagreement.
- The purpose is genuine independent scrutiny.
- Your claim must be specific enough to be compared against another agent's claim.
- If the question lacks enough information for a definitive conclusion,
  explain precisely which missing facts prevent one.
- Do not pretend to know facts about a specific institution, organization,
  or jurisdiction unless they are provided in the question.

Question:
{question}
"""

    response = client.chat.completions.create(
        model="asi1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Agent B, the skeptical counter-position analyst "
                    "inside the TruthBridge multi-agent reasoning system."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "truthbridge_agent_b",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "claim": {
                            "type": "string"
                        },
                        "reasoning": {
                            "type": "string"
                        },
                        "evidence_needed": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "uncertainty": {
                            "type": "string"
                        },
                        "challenge_to_other_agent": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "claim",
                        "reasoning",
                        "evidence_needed",
                        "uncertainty",
                        "challenge_to_other_agent"
                    ],
                    "additionalProperties": False
                }
            }
        },
        temperature=0.3,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Agent B returned an empty response.")

    return json.loads(content)


if __name__ == "__main__":

    question = input("\nEnter a question: ").strip()

    if not question:
        print("Please enter a question.")
        raise SystemExit(1)

    try:
        result = ask_agent_b(question)

        print("\n==============================")
        print("         TRUTHBRIDGE")
        print("           AGENT B")
        print("==============================")

        print(json.dumps(result, indent=2))

    except Exception as error:
        print("\nAgent B failed:")
        print(error)
