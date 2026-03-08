# Pipeline for simulating a bpmn process and running the RL bottleneck enhancer on its' output

from simulation.prosimos.run_prosimos import run_sim
from rl_bottlenecks.rl_pipeline import run_q_learning_pipeline

from app.services.state_service import store_optimal_path

def run_pipeline():
    sim_log = run_sim()

    optimal_path = run_q_learning_pipeline(sim_log)

    store_optimal_path(optimal_path)

    print("Stored optimal path in state")

    
if __name__ == "__main__":
    run_pipeline()