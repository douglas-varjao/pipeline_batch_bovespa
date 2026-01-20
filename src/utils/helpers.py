import json
from pathlib import Path

def load_tickers():
    root_dir = Path(__file__).parent.parent
    config_path = root_dir / "config" / "tickers.json"

    with open(config_path, 'r') as f:
        data = json.load(f)
    return data.get("tickers", [])