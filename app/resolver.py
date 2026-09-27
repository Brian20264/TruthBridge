import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize client pointing to the ASI:One gateway
client = OpenAI(
    api_key=os.getenv("ASI_ONE_API_KEY"),
    base_url="https://api.asi1.ai/v1"
)


def resolve_conflict(question, agent_a_answer, agent_b_answer):

    prompt = f"""
You are the Resolution Agent in TruthBridge.

Your job is NOT simply to choose Agent A or Agent B.

You must examine their reasoning and determine whether their
claims actually conflict.

USER QUESTION:
{question}

AGENT A:
{agent_a_answer}

AGENT B:
{agent_b_answer}

Analyze the disagreement.

Return your response using exactly these sections:

CONFLICT:
State whether there is a genuine conflict.

CLAIM A:
Summarize Agent A's claim.

CLAIM B:
Summarize Agent B's claim.

CONFLICT POINT:
Explain exactly where the claims differ.

EVIDENCE NEEDED:
State what evidence would help resolve the disagreement.

RESOLUTION:
Give the most justified conclusion based ONLY on the information provided.
If there is not enough information, say so.

REASONING:
Explain step-by-step why you reached that conclusion.

CHALLENGE:
Explain what new information could change the conclusion.

Do not invent evidence.
Do not pretend uncertainty does not exist.
"""

    response = client.chat.completions.create(
        model="asi1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content