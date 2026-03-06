# Reads in the simod bpmn file, enhances it's layout and stores it in the bpmn model state file

from pathlib import Path
import pm4py as pm

from app.services.state_service import store_bpmn_obj

def simod_to_state():
    print("--- Layouting simod bpmn file and updating the bpmn model state ---")
    simod_output_path = Path(__file__).parent.parent.parent / "state" / "simod_out" / "best_result"

    bpmn_file = next(simod_output_path.glob("*.bpmn"))

    bpmn = pm.read_bpmn(str(bpmn_file))

    store_bpmn_obj(bpmn, layout = True)

if __name__ == "__main__":
    simod_to_state()