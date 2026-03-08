"""
Update the q value for a given state an action with the equation from the paper
with standard values for learning rate alpha, discount factor gamma
and terminal indicating, if the given action finished the episode
Updates the q-table in-place
"""
def update_q_value(q_table, state, action, reward, next_state, alpha=0.1, gamma=0.9, terminal=False):
    current_q = q_table[state, action]
    
    if terminal:
        max_next_q = 0.0
    else:
        max_next_q = np.max(q_table[next_state]) # q value of the best action from the next state
    
    new_q = current_q + alpha * (reward + gamma * max_next_q - current_q)
    
    # update q table with new value
    q_table[state, action] = new_q
    
    return new_q