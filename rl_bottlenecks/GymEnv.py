import gymnasium as gym
from gymnasium import spaces
import numpy as np

from rl_bottlenecks.setup_env import build_reward_matrix

# Gymnasium enviroment for rl training
class GymEnv(gym.Env):
    def __init__(self, transition_log, state_to_idx, idx_to_state, bottleneck, start_states):
        super().__init__()
        
        self.transition_log = transition_log
        self.state_to_idx = state_to_idx
        self.idx_to_state = idx_to_state
        self.bottleneck = bottleneck
        self.n_states = len(state_to_idx)
        
        self.observation_space = spaces.Discrete(self.n_states)
        self.action_space = spaces.Discrete(self.n_states)
        
        self.reward_matrix = build_reward_matrix(transition_log, state_to_idx, bottleneck)
        
        self.current_state = None
        
        self.start_states = start_states
    
    def reset(self, seed=None):
        super().reset(seed=seed)
        self.current_state = np.random.choice(self.start_states)
        return self.current_state, {}
    
    def step(self, action):
        reward = self.reward_matrix[self.current_state, action]
        next_state = action
        
        terminated = (
            self.idx_to_state[next_state] == 'end' or
            self.idx_to_state[next_state] == self.bottleneck
        )
        
        self.current_state = next_state
        
        return next_state, reward, terminated, False, {}