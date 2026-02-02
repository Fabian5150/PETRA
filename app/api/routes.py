from fastapi import APIRouter
from services.state_service import load_kpis, load_bpmn

router = APIRouter()

@router.get("/process-model")
def get_current_process_model():
    data = load_bpmn()

    return {
        "bpmn": data
    }

@router.get("/kpis")
def get_current_kpis():
    data = load_kpis()
    
    return data