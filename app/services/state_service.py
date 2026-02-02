import json
from pathlib import Path
from pm4py.objects.bpmn.obj import BPMN

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
Stores a serializes bpmn xml string
in bpmn.json file in the state folder
"""
def store_bpmn(bpmn_string):
    with bpmn_file.open("w", encoding="utf-8") as f:
        json.dump({"model": bpmn_string}, f)