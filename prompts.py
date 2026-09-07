SYSTEM_PROMPT = """You are a financial forecasting assistant.
You will receive a company's historical revenue.
Estimate the revenue for the next fiscal year.

Respond with ONLY a JSON object, no markdown, in this exact shape:

{
 "predicted_revenue": <number>,
 "reasoning": "<one or two sentences>",
 "confidence": <"low|medium|high>"
}"""

def build_user_prompt(company):
    lines = [f"{h['year']}: {h['revenue']}" for h in company["history"]]
    return (
        f"Company: {company['company']}\n"
        f"Currency: {company['currency']}\n"
        f"Historical revenue:\n" + "\n".join(lines) + "\n"
        f"Predict revenue for {company['actual_next']['year']}."
    )
