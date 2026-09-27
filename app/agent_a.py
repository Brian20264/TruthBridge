import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize the OpenAI client pointing to the ASI:One gateway
client = OpenAI(
    api_key=os.getenv("ASI_ONE_API_KEY"),
    base_url="https://api.asi1.ai/v1"
)


def ask_agent_a(question):
    prompt = f"""
You are Agent A in TruthBridge.

Analyze the user's question independently.

Question:
{question}

Give:
1. Your claim
2. Your reasoning
3. The evidence or information you would need to verify the claim

Do not assume that your answer is automatically correct.
"""

    response = client.chat.completions.create(
        model="asi1-mini",  # Using the lightweight ASI:One model
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    question = input("Enter a question: ")
    answer = ask_agent_a(question)

    print("\n=== AGENT A ===")
    print(answer)