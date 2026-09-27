import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize the OpenAI client pointing to the ASI:One gateway
client = OpenAI(
    api_key=os.getenv("ASI_ONE_API_KEY"),
    base_url="https://api.asi1.ai/v1"
)


def ask_agent_b(question):
    prompt = f"""
You are Agent B in TruthBridge.

Your role is to critically examine a question and look for
missing information, alternative interpretations, contradictions,
and reasons why another agent's conclusion might be wrong.

Question:
{question}

Give:
1. Your independent claim
2. Your reasoning
3. What evidence would support your claim
4. What evidence could prove your claim wrong

Do not agree simply because another agent might give a different answer.
Be skeptical and identify uncertainty.
"""

    response = client.chat.completions.create(
        model="asi1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    question = input("Enter a question: ")
    answer = ask_agent_b(question)

    print("\n=== AGENT B ===")
    print(answer)