import sys
from pathlib import Path
from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from services.state_service import load_kpis, load_bpmn_str, store_bpmn_str, load_optimal_path, sync_bpmn_to_sim_params
from services.resource_service import get_resource_data, set_resource_activities
from services.state_service import load_bottleneck

# wow, I hate python...
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipelines.simulate_get_kpis import run_pipeline as run_prosimos
from pipelines.sim_rl import run_pipeline as run_rl_pathfinder

router = APIRouter()

class BpmnPayload(BaseModel):
    bpmnString: str
    activityDefaults: dict = {}

@router.get("/process-model", response_class = PlainTextResponse)
def get_current_process_model():
    data = load_bpmn_str()

    return data

@router.get("/kpis")
def get_current_kpis():
    data = load_kpis()
    
    return data

@router.get("/optimal-path")
def get_optimal_path():
    data = load_optimal_path()

    return data

"""
Updates the current process model and runs prosimos on it
Blocks response until prosimos is done
"""
@router.post("/process-model-simulation")
def set_current_process_model(payload: BpmnPayload):
    print("activityDefaults:", payload.activityDefaults)

    store_bpmn_str(payload.bpmnString)
    sync_bpmn_to_sim_params(payload.bpmnString, payload.activityDefaults)

    run_prosimos()

    return {"message": "Simulation done"}
"""
Blocks response until pathfinder is done
"""

@router.post("/pathfinder")
def run_pathfinder(payload: BpmnPayload):
    store_bpmn_str(payload.bpmnString)
    sync_bpmn_to_sim_params(payload.bpmnString, payload.activityDefaults)

    run_rl_pathfinder()
    
    return {"message": "Pathfinder done"}


@router.get("/resource-activities")
def get_resource_activity_mapping():
    data = get_resource_data()
    
    return data


@router.post("/resource-activities")
def update_resource_activity_mapping(mapping: dict = Body(...)):
    set_resource_activities(mapping)

    return {"message": "Resource activities updated"}

@router.get("/bottleneck")
def get_bottleneck():
    """Returns bottleneck activity name"""
    data = load_bottleneck()
    
    return {"bottleneck": data}