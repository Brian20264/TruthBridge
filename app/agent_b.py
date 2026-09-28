import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# Load variables from .env
load_dotenv()


# Connect to ASI:One
client = OpenAI(
    api_key=os.getenv("ASI_ONE_API_KEY"),
    base_url="https://api.asi1.ai/v1",
)


def ask_agent_b(question: str) -> dict:
    """
    Agent B:
    Independent skeptical and critical analyst.
    """

    prompt = f"""
You are Agent B in TruthBridge.

Analyze the following question independently.

Your role is to critically examine the issue rather than simply
agreeing with a likely answer.

Your responsibilities:
1. Produce your own claim.
2. Look for assumptions and weaknesses.
3. Identify alternative interpretations.
4. Identify missing or conflicting evidence.
5. Explain what evidence could prove your claim wrong.
6. Never invent evidence or sources.
7. Clearly state uncertainty.

Question:
{question}
"""

    response = client.chat.completions.create(
        model="asi1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Agent B, a skeptical and critical analyst "
                    "working inside the TruthBridge conflict-resolution system."
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
