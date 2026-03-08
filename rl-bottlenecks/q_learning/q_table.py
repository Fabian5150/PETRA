import numpy as np
import pandas as pd

"""
Creates an empty q-table (filled with zeros) and a mapping for activities and table indices
"""
def initialize_q_table(transition_log: pd.DataFrame):
    all_states = set(transition_log['source_activity'].unique()) | set(transition_log['target_activity'].unique())
    all_states = sorted(list(all_states))
    
    n_states = len(all_states)
    
    # activity name / table index - mapping
    state_to_idx = {state: idx for idx, state in enumerate(all_states)}
    idx_to_state = {idx: state for state, idx in state_to_idx.items()}
    
    q_table = np.zeros((n_states, n_states))
    
    return q_table, state_to_idx, idx_to_state