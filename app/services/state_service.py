import json
from pathlib import Path
import pm4py as pm
from pm4py.objects.bpmn.obj import BPMN
from pm4py.objects.bpmn.layout import layouter

BASE_DIR = Path(__file__).resolve().parents[2]
kpi_file = BASE_DIR / "state" / "kpis.json"
bpmn_file = BASE_DIR / "state" / "process-model.bpmn"
sim_params_file = BASE_DIR /  "state" / "sim_params.json"
optimal_path_file = BASE_DIR / "state" / "optimal-path.json"
bottleneck_file = BASE_DIR / "state" / "bottleneck.json"

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
    return bpmn_file.read_text(encoding="utf-8")

"""
Stores a pm4py bpmn object in the bpmn state file as standardized bpmn 2.0 xml
Can adjust its' layout
"""
def store_bpmn_obj(process_model: BPMN, layout = False):
    if(layout):
        process_model = layouter.apply(process_model)
    
    pm.write_bpmn(process_model, bpmn_file)

"""
Stores a bpmn xml string directly in the bpmn state file
Can adjust its' layout
"""
def store_bpmn_str(bpmn_string: str, layout = False):
    bpmn_file.write_text(bpmn_string, encoding="utf-8")

    if(layout):
        store_bpmn_obj(load_bpmn_obj(), layout = True)
        
"""
Stores the optimal path as list given from the RL pathfinder
"""
def store_optimal_path(optimal_path):
    with optimal_path_file.open("w", encoding="utf-8") as f:
        json.dump({"path": optimal_path}, f)

"""
Loads the current determined optimal path
"""
def load_optimal_path():
    with optimal_path_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def load_resource_allocation():
    with sim_params_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data["resource_profiles"]

def store_sim_params(kpis: dict):
    with sim_params_file.open("w", encoding="utf-8") as f:
        json.dump(kpis, f)

def store_bottleneck(bottleneck_name):
    with bottleneck_file.open("w") as f:
        json.dump({"bottleneck": bottleneck_name}, f, indent=2)

def load_bottleneck():
    if not bottleneck_file.exists():
        return None
    with bottleneck_file.open("r") as f:
        data = json.load(f)
    return data.get("bottleneck")