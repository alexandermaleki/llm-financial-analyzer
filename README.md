# LLM Financial Analyzer

A learning project testing whether an LLM can forecast a bank's next-year
income from its historical figures, and how much prompt framing changes
the result.

## What it does

Given several years of reported income, the model predicts the next year.
That year is held out and known, so every prediction is scored against it.
Two trivial baselines run alongside for comparison.

Test case: SEB Group, total operating income, 2020 to 2023, predicting
2024 (actual: SEK 81,887m).

## Results

| Method | Prediction | Error |
|---|---|---|
| Naive (carry 2023 forward) | 80,193 | 2.1% |
| Linear trend | 90,048 | 10.0% |
| LLM, numbers only | 92,222 | 12.6% |
| LLM, with company name | ~93,000 (3 runs) | 13.6% |
| LLM, prompted to reason about industry and macro | ~76,000 (7 runs) | 7.2% |

## What I found

Adding the company name changed nothing. The model still extrapolated the
growth trend and never mentioned that SEB is a bank.

Adding one instruction, to consider the industry and economic environment,
cut the error roughly in half. Its stated reasoning shifted to interest
rate cuts compressing net interest income, which matches what actually
happened to SEB's net interest income between 2023 and 2024. The knowledge
was available the whole time and went unused until it was asked for.

That variant also overcorrected, predicting a decline where income rose
slightly. And the naive baseline beat every LLM variant tested.

## Limitations

- One company, one forecast year. Not enough to generalise, and testing
  further companies would show whether the framing effect holds.
- SEB's 2024 results predate the model's training cutoff, so the reasoning
  may be recall rather than inference. Not controlled for.
- The reasoning variant ranged 71,000 to 78,000 across runs, roughly 9%.
  The model does not accept a temperature parameter, so this can be
  measured but not removed.
- One of seven runs gave the opposite causal explanation while landing on a
  similar number, so the stated reasoning may not reflect what drives the
  output.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add `OPENAI_API_KEY` to a `.env` file in the project root, then:

```bash
python main.py
```

## Structure

- `main.py` runs the forecast and baselines and prints the comparison
- `llm.py` API call and response parsing
- `prompts.py` system prompt variants
- `data.py` loads the dataset
- `data/companies.json` historical figures and held out actuals
