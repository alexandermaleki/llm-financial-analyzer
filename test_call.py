import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-5.6-luna",
    messages=[
        {"role": "system", "content": "You are a financial analyst. Be concise."},
        {"role": "user", "content": "In one sentence: what does a high debt-to-equity ratio suggest about a company's risk?"}
    ]
)

print(response.choices[0].message.content)
print("---")
print(f"Tokens used: {response.usage.total_tokens}")
