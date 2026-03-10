import json
from pathlib import Path
import pm4py as pm

BASE_DIR = Path(__file__).resolve().parents[2]
bpmn_file = BASE_DIR / "state" / "process-model.bpmn"
sim_params_file = BASE_DIR /  "state" / "sim_params.json"

def create_node_activity_mapping(bpmn_path=bpmn_file):
    bpmn = pm.read_bpmn(str(bpmn_path))
    mapping = {}
    for node in bpmn.get_nodes():
        node_id = node.get_id()
        node_name = node.get_name()
        if node_name:
            mapping[node_id] = node_name
    return mapping


def create_activity_node_mapping(bpmn_path=bpmn_file):
    node_to_activity = create_node_activity_mapping(bpmn_path)
    return {name: node_id for node_id, name in node_to_activity.items()}


def load_resource_allocation(sim_params_path=sim_params_file):
    with sim_params_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data["resource_profiles"]


def get_resource_activities(sim_params_path=sim_params_file, bpmn_path=bpmn_file):
    node_to_activity = create_node_activity_mapping(bpmn_path)
    resource_profiles = load_resource_allocation(sim_params_path)
    
    resource_activities = {}
    
    for profile in resource_profiles:
        for resource in profile.get('resource_list', []):
            resource_name = resource['name']
            assigned_node_ids = resource.get('assignedTasks', [])
            
            activity_names = [
                node_to_activity[node_id] 
                for node_id in assigned_node_ids 
                if node_id in node_to_activity
            ]
            
            resource_activities[resource_name] = activity_names
    
    return resource_activities


def set_resource_activities(resource_activities, sim_params_path=sim_params_file, bpmn_path=bpmn_file):
    activity_to_node = create_activity_node_mapping(bpmn_path)
    
    with sim_params_path.open("r", encoding="utf-8") as f:
        sim_params = json.load(f)
    
    resource_profiles = sim_params["resource_profiles"]
    
    for profile in resource_profiles:
        for resource in profile.get('resource_list', []):
            resource_name = resource['name']
            
            if resource_name in resource_activities:
                activity_names = resource_activities[resource_name]
                
                node_ids = [
                    activity_to_node[activity] 
                    for activity in activity_names 
                    if activity in activity_to_node
                ]
                
                resource['assignedTasks'] = node_ids
    
    sim_params["resource_profiles"] = resource_profiles
    
    with sim_params_path.open("w", encoding="utf-8") as f:
        json.dump(sim_params, f, indent=4)