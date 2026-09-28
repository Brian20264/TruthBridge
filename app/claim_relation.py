import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("ASI_ONE_API_KEY"),
    base_url="https://api.asi1.ai/v1",
)


def analyze_claim_relation(claim_a: str, claim_b: str) -> dict:
    """
    Determine the logical relationship between two claims.
    """

    prompt = f"""
You are the Claim Relationship Analyzer in TruthBridge.

Compare the two claims below.

CLAIM A:
{claim_a}

CLAIM B:
{claim_b}

Classify their relationship using exactly ONE of:

AGREE
QUALIFY
CONTRADICT
UNRELATED

Definitions:

AGREE:
Both claims support substantially the same conclusion.

QUALIFY:
One claim adds conditions, exceptions, limitations, or uncertainty
to the other without directly denying its main conclusion.

CONTRADICT:
The claims make incompatible assertions about the same issue.

UNRELATED:
The claims do not address the same proposition.

Also provide:
1. A short explanation of the relationship.
2. The key difference between the claims.
3. A confidence value from 0 to 1.

Do not invent evidence.
Judge only the relationship between the claims.
"""

    response = client.chat.completions.create(
        model="asi1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You analyze relationships between claims "
                    "for an auditable AI conflict-resolution system."
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
                "name": "claim_relationship",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "relationship": {
                            "type": "string",
                            "enum": [
                                "AGREE",
                                "QUALIFY",
                                "CONTRADICT",
                                "UNRELATED"
                            ]
                        },
                        "explanation": {
                            "type": "string"
                        },
                        "key_difference": {
                            "type": "string"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1
                        }
                    },
                    "required": [
                        "relationship",
                        "explanation",
                        "key_difference",
                        "confidence"
                    ],
                    "additionalProperties": False
                }
            }
        },
        temperature=0.1,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Claim relationship analyzer returned no result."
        )

    return json.loads(content)


if __name__ == "__main__":

    claim_a = input("\nEnter Claim A: ").strip()
    claim_b = input("\nEnter Claim B: ").strip()

    if not claim_a or not claim_b:
        print("Both claims are required.")
        raise SystemExit(1)

    try:
        result = analyze_claim_relation(
            claim_a,
            claim_b,
        )

        print("\n==========================================")
        print("       TRUTHBRIDGE CLAIM ANALYZER")
        print("==========================================")

        print("\nRelationship:")
        print(result["relationship"])

        print("\nExplanation:")
        print(result["explanation"])

        print("\nKey difference:")
        print(result["key_difference"])

        print("\nConfidence:")
        print(result["confidence"])

    except Exception as error:
        print("\nClaim analyzer failed:")
        print(error)
