from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse

from services.state_service import load_kpis, load_bpmn, store_bpmn

router = APIRouter()

@router.get("/process-model", response_class=PlainTextResponse)
def get_current_process_model():
    data = load_bpmn()

    return data

@router.get("/kpis")
def get_current_kpis():
    data = load_kpis()
    
    return data

@router.post("/process-model")
def set_current_process_model(bpmnString: str = Body(..., media_type="text/plain")):
    store_bpmn(bpmnString)