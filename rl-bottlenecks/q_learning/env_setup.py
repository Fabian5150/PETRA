import numpy as np
import pandas as pd

"""
Creates an empty q-table (filled with zeros) and a mapping for activities and table indices
"""
def initialize_q_table(transition_log: pd.DataFrame):
    all_states = set(transition_log["source_activity"].unique()) | set(transition_log["target_activity"].unique())
    all_states = sorted(list(all_states))
    
    n_states = len(all_states)
    
    # activity name / table index - mapping
    state_to_idx = {state: idx for idx, state in enumerate(all_states)}
    idx_to_state = {idx: state for state, idx in state_to_idx.items()}
    
    q_table = np.zeros((n_states, n_states))
    
    return q_table, state_to_idx, idx_to_state

"""
Builds the reward matrix according to the paper:
 -1 for non existing transitions
 +10 for the end state
 -1 for the bottleneck activity
 +(weigted reward) for valid transition based on their relative frequency
"""
def build_reward_matrix(transition_log, state_to_idx, bottleneck_act_name):
    n_states = len(state_to_idx)
    
    # initalize all activity pairs with -1 reward
    rewards = np.full((n_states, n_states), -1.0)
    
    # adjust reward for actually existing transittions
    for _, row in transition_log.iterrows():
        source = row["source_activity"]
        target = row["target_activity"]
        prob = row["transition_probability"]
        
        s_idx = state_to_idx[source]
        t_idx = state_to_idx[target]
        
        if target == "end":
            rewards[s_idx, t_idx] = 10.0  # Big reward for end
        elif target == bottleneck_act_name:
            rewards[s_idx, t_idx] = -1.0  # penalty for bottleneck
        else:
            rewards[s_idx, t_idx] = prob  # weighted reward for normal transitions based on transition probabilty
    
    return rewards