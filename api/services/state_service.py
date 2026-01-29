import json
from pathlib import Path

kpi_file = Path("../state/kpis.json")

def load_kpis():
    with kpi_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data