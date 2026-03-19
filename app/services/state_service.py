import json
from pathlib import Path
import pm4py as pm
from pm4py.objects.bpmn.obj import BPMN
from pm4py.objects.bpmn.layout import layouter
import tempfile

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
def store_bpmn_str(bpmn_string: str, layout = False, syncParams = False):
    if(syncParams):
        sync_bpmn_to_sim_params(bpmn_string)
    
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

def sync_bpmn_to_sim_params(bpmn_string, activity_defaults=None):
    """
    Synced BPMN mit sim_params.json:
    - Fügt fehlende Gateways mit aktuellen Flow-IDs hinzu
    - Fügt fehlende Activities mit Default-Werten hinzu
    """
    activity_defaults = activity_defaults or {}

    # Parse BPMN (über temp file)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bpmn', delete=False) as f:
        f.write(bpmn_string)
        temp_path = f.name

    try:
        bpmn = pm.read_bpmn(temp_path)
    finally:
        Path(temp_path).unlink()

    # Lade sim_params
    with sim_params_file.open('r') as f:
        sim_params = json.load(f)

    # --- 1. Gateway Probabilities ---
    gateway_ids = set()
    gateway_flows = {}

    for node in bpmn.get_nodes():
        if 'Gateway' in node.__class__.__name__:
            gateway_id = node.get_id()
            gateway_ids.add(gateway_id)
            gateway_flows[gateway_id] = []

    for flow in bpmn.get_flows():
        source_id = flow.get_source().get_id()
        if source_id in gateway_ids:
            gateway_flows[source_id].append(flow.get_id())

    if 'gateway_branching_probabilities' not in sim_params:
        sim_params['gateway_branching_probabilities'] = []

    for gateway_id, outgoing_flows in gateway_flows.items():
        if not outgoing_flows:
            continue

        prob = 1.0 / len(outgoing_flows)

        sim_params['gateway_branching_probabilities'] = [
            g for g in sim_params['gateway_branching_probabilities']
            if g['gateway_id'] != gateway_id
        ]

        sim_params['gateway_branching_probabilities'].append({
            "gateway_id": gateway_id,
            "probabilities": [
                {"path_id": flow_id, "value": prob}
                for flow_id in outgoing_flows
            ]
        })

    # --- 2. Activity Resource Assignments & Durations ---
    activity_ids = set()
    for node in bpmn.get_nodes():
        if node.__class__.__name__ == 'Task' and node.get_name():
            activity_ids.add(node.get_id())

    # Finde bestehende Activities in allen resource_profiles
    existing_activities = set()
    for profile in sim_params.get('resource_profiles', []):
        for resource in profile.get('resource_list', []):
            existing_activities.update(resource.get('assignedTasks', []))

    # Füge neue Activities zu ALLEN resources hinzu
    new_activities = activity_ids - existing_activities
    if new_activities:
        for profile in sim_params.get('resource_profiles', []):
            for resource in profile.get('resource_list', []):
                resource['assignedTasks'].extend(list(new_activities))
        print(f"✓ Added {len(new_activities)} new activities to all resources")

    # Erste verfügbare Resource-ID finden als Fallback
    fallback_resource_id = "GLOBAL"
    for profile in sim_params.get('resource_profiles', []):
        for resource in profile.get('resource_list', []):
            fallback_resource_id = resource['id']
            break
        break

    # Füge Activity Durations hinzu (falls nicht vorhanden)
    if 'task_resource_distribution' not in sim_params:
        sim_params['task_resource_distribution'] = []

    existing_task_distributions = {
        t['task_id'] for t in sim_params['task_resource_distribution']
    }

    for activity_id in activity_ids:
        if activity_id not in existing_task_distributions:
            sim_params['task_resource_distribution'].append({
                "task_id": activity_id,
                "resources": [{
                    "resource_id": fallback_resource_id,
                    "distribution_name": "fix",
                    "distribution_params": [
                        {"value": activity_defaults.get(activity_id, 3600.0)}
                    ]
                }]
            })

    # Speichern
    with sim_params_file.open('w') as f:
        json.dump(sim_params, f, indent=4)

    print(f"✓ Synced {len(gateway_ids)} gateways and {len(activity_ids)} activities")