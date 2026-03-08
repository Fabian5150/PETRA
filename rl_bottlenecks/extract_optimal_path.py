import numpy as np

"""
Extracts the found optimal path from the final q table
"""
def extract_optimal_path(q_table, state_to_idx, idx_to_state, start_activities, max_steps=20):
    start_state = None
    
    for activity in start_activities:
        if activity in state_to_idx:
            start_state = state_to_idx[activity]
            break
    
    path = []
    current_state = start_state
    visited = set()
    
    for _ in range(max_steps):
        state_name = idx_to_state[current_state]
        path.append(state_name)
        
        if state_name == 'end':
            break
        
        # detects loops and exits path
        if current_state in visited:
            break
        visited.add(current_state)
        
        best_action = np.argmax(q_table[current_state])
        current_state = best_action
    
    return path