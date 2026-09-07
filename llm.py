import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT, build_user_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-5.6-luna"

def forecast(company):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(company)},
        ],
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        print(f"Failed to parse response for {company['company']}:")
        print(raw)
        return None

    parsed["_tokens"] = response.usage.total_tokens
    return parsed
