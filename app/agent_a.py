import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env
load_dotenv()


# Connect to ASI:One
client = OpenAI(
    api_key=os.getenv("ASI_ONE_API_KEY"),
    base_url="https://api.asi1.ai/v1",
)


def ask_agent_a(question: str) -> dict:
    """
    Agent A:
    Evidence-focused independent analyst.
    """

    prompt = f"""
You are Agent A in TruthBridge.

Analyze the following question independently.

Your responsibilities:
1. Produce your best-supported claim.
2. Explain the reasoning behind the claim.
3. Identify the evidence that would be needed to verify it.
4. State important uncertainty.
5. Never invent evidence or sources.

Question:
{question}
"""

    response = client.chat.completions.create(
        model="asi1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evidence-focused AI analyst "
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
                "name": "truthbridge_agent_a",
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
                        }
                    },
                    "required": [
                        "claim",
                        "reasoning",
                        "evidence_needed",
                        "uncertainty"
                    ],
                    "additionalProperties": False
                }
            }
        },
        temperature=0.2,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Agent A returned an empty response.")

    return json.loads(content)


if __name__ == "__main__":

    question = input("\nEnter a question: ").strip()

    if not question:
        print("Please enter a question.")
        raise SystemExit(1)

    try:
        result = ask_agent_a(question)

        print("\n==============================")
        print("         TRUTHBRIDGE")
        print("           AGENT A")
        print("==============================")

        print(json.dumps(result, indent=2))

    except Exception as error:
        print("\nAgent A failed:")
        print(error)
