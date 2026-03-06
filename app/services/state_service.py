import json
from pathlib import Path
import pm4py as pm
from io import StringIO
from pm4py.objects.bpmn.obj import BPMN
from pm4py.objects.bpmn.layout import layouter

BASE_DIR = Path(__file__).resolve().parents[2]
kpi_file = BASE_DIR / "state" / "kpis.json"
bpmn_file = BASE_DIR / "state" / "process-model.bpmn"

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
Loads a pm4py bpmn object from the bpmn xml state file
"""
def load_bpmn_obj():
    return pm.read_bpmn(str(bpmn_file))

"""
Loads the currect bpmn state file and returns it directly as xml string
"""
def load_bpmn_str():
    return bpmn_file.read_text(encoding='utf-8')

"""
Stores a pm4py bpmn object in the bpmn state file as standardized bpmn 2.0 xml
Can adjust its' layout
"""
def store_bpmn_obj(process_model: BPMN, layout = True):
    if(layout):
        process_model = layouter.apply(process_model)
    
    pm.write_bpmn(process_model, bpmn_file)

"""
Stores a bpmn xml string directly in the bpmn state file
Can adjust its' layout
"""
def store_bpmn_str(bpmn_string: str, layout = True):
    bpmn_file.write_text(bpmn_string, encoding='utf-8')

    if(layout):
        store_bpmn_obj(load_bpmn_obj(), layout = True)