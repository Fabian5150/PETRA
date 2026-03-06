import sys
from pathlib import Path
from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse

from services.state_service import load_kpis, load_bpmn_str, store_bpmn_str

# wow, I hate python...
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.simulate_get_kpis import run_pipeline as run_prosimos

router = APIRouter()

@router.get("/process-model", response_class=PlainTextResponse)
def get_current_process_model():
    data = load_bpmn_str()

    return data

@router.get("/kpis")
def get_current_kpis():
    data = load_kpis()
    
    return data

"""
Updates the current process model and runs prosimos on it
Blocks response until prosimos is done
"""
@router.post("/process-model-simulation")
def set_current_process_model(bpmnString: str = Body(..., media_type="text/plain")):
    store_bpmn_str(bpmnString, layout = True)

    run_prosimos()

    return {"message": "Simulation done"}