# Reads in the simod bpmn file, enhances it's layout and stores it in the bpmn model state file

import json
from pathlib import Path
import pm4py as pm

from app.services.state_service import store_sim_params, store_bpmn_str

def simod_to_state():
    print("--- Updating the bpmn model state ---")
    simod_output_path = Path(__file__).parent.parent.parent / "state" / "simod_out" / "best_result"

    bpmn_file_path = next(simod_output_path.glob("*.bpmn"))

    bpmn_content = bpmn_file_path.read_text(encoding="utf-8")
    store_bpmn_str(bpmn_content, layout=False)

    print("--- Copying simulation parameters to state ---")
    json_files = list(simod_output_path.glob("*.json"))
    exclude = {"canonical_model.json", "runtimes.json"}
    
    sim_params_path = next(
        (f for f in json_files if f.name not in exclude),
        None
    )

    with open(sim_params_path, "r") as f:
        sim_params = json.load(f)
    store_sim_params(sim_params)

if __name__ == "__main__":
    simod_to_state()