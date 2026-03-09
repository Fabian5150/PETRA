import numpy as np

from rl_bottlenecks.epsilon_policy import update_epsilon, epsilon_greedy_action
from rl_bottlenecks.q_values import update_q_value

def train_q_learning(env, n_episodes=8000, alpha=0.1, gamma=0.9, epsilon_start=1.0, epsilon_min=0.01, epsilon_decay=0.001):
    
    n_states = env.observation_space.n
    q_table = np.zeros((n_states, n_states))
    
    rewards_per_episode = []
    regrets_per_episode = []
    epsilon_per_episode = []
    
    print(f"Starting training with {n_episodes} episodes")
    
    for episode in range(n_episodes):
        if episode % 500 == 0:
            print(f"Episode {episode}")
        
        epsilon = update_epsilon(episode, epsilon_start, epsilon_min, epsilon_decay)
        epsilon_per_episode.append(epsilon)
        
        state, _ = env.reset()
        
        total_reward = 0
        total_regret = 0
        terminated = False
        
        while not terminated:
            action = epsilon_greedy_action(q_table, state, epsilon, n_states)
            next_state, reward, terminated, _, _ = env.step(action)
            
            update_q_value(q_table, state, action, reward, next_state,
                          alpha, gamma, terminated)
            
            total_reward += reward
            if not terminated:
                max_next_q = np.max(q_table[next_state])
                total_regret += (max_next_q - reward)
            
            state = next_state
        
        rewards_per_episode.append(total_reward)
        regrets_per_episode.append(total_regret)
    
    return q_table