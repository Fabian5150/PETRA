# Pipeline for simulating a bpmn process and running the RL bottleneck enhancer on its' output

from simulation.prosimos.run_prosimos import run_sim
from rl_bottlenecks.rl_pipeline import run_q_learning_pipeline
from rl_bottlenecks.find_bpmn_path import match_rl_path_to_bpmn

from app.services.state_service import store_optimal_path, load_bpmn_obj

def run_pipeline():
    sim_log = run_sim()

    optimal_rl_path = run_q_learning_pipeline(sim_log)

    bpmn_obj = load_bpmn_obj()

    print("--- Matching RL path to BPMN graph ---")
    bpmn_path = match_rl_path_to_bpmn(bpmn_obj, optimal_rl_path)

    print(f"BPMN optimal path: {bpmn_path}")

    if(bpmn_path == []):
        store_optimal_path(optimal_rl_path)
    else:
        store_optimal_path(bpmn_path)

    print("Stored optimal path in state")

    
if __name__ == "__main__":
    run_pipeline()