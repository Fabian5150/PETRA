from fastapi import APIRouter

router = APIRouter()

@router.get("/process-model")
def get_current_process_model():
    return {
        "bpmn": "le bpmn hier"    
    }