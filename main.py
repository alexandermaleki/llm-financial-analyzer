from data import load_companies
from llm import forecast

def naive_forecast(history):
    """Last observed value carried forward."""
    return history[-1]["revenue"]

def linear_trend_forecast(history):
    """Extrapolate the average year-over-year change."""
    changes = [
        history[i]["revenue"] - history[i - 1]["revenue"]
        for i in range(1, len(history))
    ]
    avg_change = sum(changes) / len(changes)
    return history[-1]["revenue"] + avg_change

def error_pct(predicted, actual):
    return abs(predicted - actual) / actual * 100

def main():
    company = load_companies()[0]
    history = company["history"]
    actual = company["actual_next"]["revenue"]

    print(f"Company: {company['company']}")
    print(f"Actual {company['actual_next']['year']}: {actual:,.0f}\n")

    naive = naive_forecast(history)
    trend = linear_trend_forecast(history)

    print(f"{'Method':<20} {'Prediction':>12} {'Error':>8}")
    print("-" * 42)
    print(f"{'Naive':<20} {naive:>12,.0f} {error_pct(naive, actual):>7.1f}%")
    print(f"{'Linear trend':<20} {trend:>12,.0f} {error_pct(trend, actual):>7.1f}%")

    result = forecast(company)
    if result:
        pred = result["predicted_revenue"]
        print(f"{'LLM':<20} {pred:>12,.0f} {error_pct(pred, actual):>7.1f}%")
        print(f"\nReasoning: {result['reasoning']}")
        print(f"Tokens: {result['_tokens']}")

if __name__ == "__main__":
    main()
