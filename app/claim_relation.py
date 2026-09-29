import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("ASI_ONE_API_KEY"),
    base_url="https://api.asi1.ai/v1",
)


def local_claim_relation(claim_a: str, claim_b: str) -> dict:
    """
    Local deterministic fallback used when ASI:One is unavailable.

    This is a transparent fallback, not an AI model.
    """

    a = claim_a.lower().strip()
    b = claim_b.lower().strip()

    # Direct contradiction patterns
    positive_patterns = [
        "yes",
        "can ",
        "is allowed",
        "may register",
        "can register",
        "required?",
    ]

    negative_patterns = [
        "no",
        "cannot",
        "can't",
        "is not allowed",
        "may not register",
        "cannot register",
        "must not",
    ]

    a_positive = any(pattern in a for pattern in positive_patterns)
    a_negative = any(pattern in a for pattern in negative_patterns)

    b_positive = any(pattern in b for pattern in positive_patterns)
    b_negative = any(pattern in b for pattern in negative_patterns)

    if a_positive and b_negative or a_negative and b_positive:
        return {
            "relationship": "CONTRADICT",
            "explanation": (
                "The two claims make incompatible assertions about the "
                "same proposition."
            ),
            "key_difference": (
                "One claim permits or affirms the proposition while the "
                "other denies or restricts it."
            ),
            "confidence": 0.95,
        }

    # Exact or near-exact agreement
    if a == b:
        return {
            "relationship": "AGREE",
            "explanation": (
                "Both agents produced substantially the same claim."
            ),
            "key_difference": "No material difference was detected.",
            "confidence": 1.0,
        }

    # Simple qualification detection
    qualification_words = [
        "unless",
        "except",
        "although",
        "however",
        "normally",
        "may",
        "might",
        "sometimes",
        "condition",
    ]

    if any(word in a for word in qualification_words) or any(
        word in b for word in qualification_words
    ):
        return {
            "relationship": "QUALIFY",
            "explanation": (
                "One claim appears to add a condition, exception, "
                "limitation, or uncertainty."
            ),
            "key_difference": (
                "The claims differ mainly in conditions or limitations."
            ),
            "confidence": 0.70,
        }

    return {
        "relationship": "UNRELATED",
        "explanation": (
            "The local fallback could not establish that the claims "
            "address the same proposition."
        ),
        "key_difference": (
            "No clear logical relationship was detected."
        ),
        "confidence": 0.50,
    }


def analyze_claim_relation(claim_a: str, claim_b: str) -> dict:
    """
    Determine the logical relationship between two claims.

    ASI:One is attempted first.
    A transparent local fallback is used if ASI:One is unavailable.
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

    try:
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
                                    "UNRELATED",
                                ],
                            },
                            "explanation": {
                                "type": "string",
                            },
                            "key_difference": {
                                "type": "string",
                            },
                            "confidence": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                            },
                        },
                        "required": [
                            "relationship",
                            "explanation",
                            "key_difference",
                            "confidence",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            temperature=0.1,
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "Claim relationship analyzer returned no result."
            )

        result = json.loads(content)
        result["mode"] = "ASI:One"
        return result

    except Exception as error:
        print("\nASI:One claim analysis unavailable.")
        print(f"Reason: {error}")
        print("Using transparent local claim analysis.")

        result = local_claim_relation(claim_a, claim_b)
        result["mode"] = "LOCAL FALLBACK"
        return result


if __name__ == "__main__":
    claim_a = input("\nEnter Claim A: ").strip()
    claim_b = input("\nEnter Claim B: ").strip()

    if not claim_a or not claim_b:
        print("Both claims are required.")
        raise SystemExit(1)

    result = analyze_claim_relation(claim_a, claim_b)

    print("\n==========================================")
    print("       TRUTHBRIDGE CLAIM ANALYZER")
    print("==========================================")

    print("\nMode:")
    print(result["mode"])

    print("\nRelationship:")
    print(result["relationship"])

    print("\nExplanation:")
    print(result["explanation"])

    print("\nKey difference:")
    print(result["key_difference"])

    print("\nConfidence:")
