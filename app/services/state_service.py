import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
kpi_file = BASE_DIR / "state" / "kpis.json"
bpmn_file = BASE_DIR / "state" / "bpmn.json"

"""
Loads the kpis from their json state file
and returns them as a dict
"""
def load_kpis():
    with kpi_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data

"""
Stores the kpis dict in the kpis.json state file
"""
def store_kpis(kpis: dict):
    with kpi_file.open("w", encoding="utf-8") as f:
        json.dump(kpis, f)

"""
Loads the bpmn model as xml string from the bpmn.json state file
Returns as a string
"""
def load_bpmn():
    with bpmn_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data["model"]

"""
Stores a serializes bpmn xml string
in bpmn.json state file
TODO: Just use the pm4py file export, instead of writing it's content as string to a json file
"""
def store_bpmn(bpmn_string: str):
    with bpmn_file.open("w", encoding="utf-8") as f:
        json.dump({"model": bpmn_string}, f)