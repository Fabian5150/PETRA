"""
Script for loading a specific simod simulation model into the state
Run from cmd and pass "bpi_2012" "bpi_2013", "manufacturing" or "purchase" to specifiy the log
and "agents" or "control-flow" to specify the simulation type
If no parameters are passed, the agent-based bpi_2012 log will be loaded
"""
import json
import sys
from pathlib import Path
from app.services.state_service import store_sim_params, store_bpmn_str
from pipelines.simulate_get_kpis import run_pipeline as run_prosimos

BASE_PATH = Path(__file__).parent

FILE_NAMES = {
    "bpi_2012": "bpi_2012_approx",
    "bpi_2013": "bpi_2013_approx",
    "manufacturing": "manufacturing_simod",
    "purchase": "purchase_simod",
}

MODEL_DIRS = {
    "agents": BASE_PATH / "data" / "agent_based_models",
    "control-flow": BASE_PATH / "data" / "control_flow_models",
}

def load_to_state(log_name="bpi_2012", model_type="agents"):
    if log_name not in FILE_NAMES:
        print(f"Unknown log name '{log_name}'. Choose from: {list(FILE_NAMES.keys())}")
        sys.exit(1)

    if model_type not in MODEL_DIRS:
        print(f"Unknown model type '{model_type}'. Choose from: agents, control-flow")
        sys.exit(1)

    base = MODEL_DIRS[model_type] / log_name
    stem = FILE_NAMES[log_name]

    bpmn_path = base / f"{stem}.bpmn"
    json_path = base / f"{stem}.json"

    print(f"--- Loading {log_name} ({model_type}) into state ---")

    bpmn_content = bpmn_path.read_text(encoding="utf-8")
    store_bpmn_str(bpmn_content, layout=False)

    with open(json_path, "r") as f:
        sim_params = json.load(f)
    store_sim_params(sim_params)

    print("--- Clearing optimal path state ---")
    optimal_path_file = BASE_PATH / "state" / "optimal-path.json"
    with open(optimal_path_file, "w") as f:
        json.dump({"path": []}, f)

    print("--- Running initial Prosimos simulation ---")
    run_prosimos()
    print("--- Done ---")

if __name__ == "__main__":
    log_name = sys.argv[1] if len(sys.argv) > 1 else "bpi_2012"
    model_type = sys.argv[2] if len(sys.argv) > 2 else "agents"
    load_to_state(log_name, model_type)