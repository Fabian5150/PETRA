from fastapi import APIRouter
from services.state_service import load_kpis

router = APIRouter()

@router.get("/process-model")
def get_current_process_model():
    return {
        "bpmn": "le bpmn hier"    
    }

@router.get("/kpis")
def get_current_kpis():
    data = load_kpis()
    return data