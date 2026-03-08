import gymnasium as gym
from gymnasium import spaces
import numpy as np

from rl_bottlenecks.setup_env import build_reward_matrix

# Gymnasium enviroment for rl training
class ProcessMiningEnv(gym.Env):
    """
    Gymnasium Environment für Process Mining Q-Learning
    """
    
    def __init__(self, transitions, state_to_idx, idx_to_state, bottleneck, start_state_names):
        super().__init__()
        
        self.transitions = transitions
        self.state_to_idx = state_to_idx
        self.idx_to_state = idx_to_state
        self.bottleneck = bottleneck
        self.n_states = len(state_to_idx)
        
        self.observation_space = spaces.Discrete(self.n_states)
        self.action_space = spaces.Discrete(self.n_states)
        
        self.reward_matrix = build_reward_matrix()
        
        self.current_state = None
        
        self.start_states = start_state_names
    
    def reset(self, seed=None):
        """Reset Environment"""
        super().reset(seed=seed)
        self.current_state = np.random.choice(self.start_states)
        return self.current_state, {}
    
    def step(self, action):
        """Execute Action"""
        reward = self.reward_matrix[self.current_state, action]
        next_state = action
        
        # Terminal?
        terminated = (
            self.idx_to_state[next_state] == 'end' or
            self.idx_to_state[next_state] == self.bottleneck
        )
        
        self.current_state = next_state
        
        return next_state, reward, terminated, False, {}