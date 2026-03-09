import pm4py as pm

from rl_bottlenecks.pre_proc_pipeline import run_pipeline as run_pre_processing
from rl_bottlenecks.setup_env import create_state_mappings
from rl_bottlenecks.training import train_q_learning
from rl_bottlenecks.pre_proc_pipeline import identify_absorption_state
from rl_bottlenecks.extract_optimal_path import extract_optimal_path
from rl_bottlenecks.GymEnv import GymEnv

from pre_processing.import_data import import_prosimos

"""
Pipeline for running the q-learning on the inital log and returning the determined optimal path
"""
def run_q_learning_pipeline(log, n_episodes = 8000, alpha = 0.1, gamma = 0.9):
    print("--- Starting q-learning pipeline ---")    
    
    print("--- Extractin paths and bottleneck ---")
    transition_log = run_pre_processing(log)
    state_to_idx, idx_to_state = create_state_mappings(transition_log)

    start_activity_names = set(
        pm.get_start_activities(
            log,
            activity_key = "concept:name",
            timestamp_key = "time:timestamp",
            case_id_key = "case:concept:name"
        ).keys()
    )
    
    start_state_indices = [
        state_to_idx[name] for name in start_activity_names 
        if name in state_to_idx
    ]

    bottleneck = identify_absorption_state(log)
    
    print("--- Building gym env ---")
    env = GymEnv(transition_log, state_to_idx, idx_to_state, bottleneck, start_state_indices)
    
    print("--- Training model ---")
    q_table = train_q_learning(
        env,
        n_episodes=n_episodes,
        alpha=alpha,
        gamma=gamma
    )
    
    print("--- Extracting optimal path ---")
    optimal_path = extract_optimal_path(q_table, state_to_idx, idx_to_state, start_activity_names)
    
    print(f"Finished with optimal path: {optimal_path}")

    return optimal_path

if __name__ == "__main__":
    data = import_prosimos()

    run_q_learning_pipeline(data)