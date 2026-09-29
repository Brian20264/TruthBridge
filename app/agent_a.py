import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("ASI_ONE_API_KEY"),
    base_url="https://api.asi1.ai/v1",
)


def ask_agent_a(question: str) -> dict:
    """
    Agent A:
    Strict/default-position analyst.

    Agent A establishes the strongest reasonable default interpretation
    of the question so that Agent B can independently challenge it.
    """

    prompt = f"""
You are Agent A in TruthBridge.

Analyze this question independently:

{question}

Your role is the STRICT DEFAULT-POSITION ANALYST.

Your responsibilities:
1. Identify the strongest reasonable default answer to the question.
2. State that position clearly and directly.
3. Give the reasoning supporting that position.
4. Identify the specific evidence that would be needed to verify the position.
5. State important uncertainty and exceptions.
6. Never invent evidence, laws, policies, statistics, or sources.

Important:
- Do not automatically answer "it depends" merely because some uncertainty exists.
- First identify the most defensible default position supported by the information available.
- Clearly separate the general/default position from exceptions.
- Your claim must be specific enough that another independent agent can challenge it.
- Do not pretend to know facts about a specific institution, organization, or jurisdiction unless they are provided in the question.

Question:
{question}
"""

    response = client.chat.completions.create(
        model="asi1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Agent A, the strict default-position analyst "
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
