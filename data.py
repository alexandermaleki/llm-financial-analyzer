import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "companies.json"

def load_companies():
    with open(DATA_PATH) as f:
        return json.load(f)
