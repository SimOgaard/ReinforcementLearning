import numpy as np

class Agent0:
    
    def __init__(self):
        self.action_size = 2

    def act(self):
        return self.sample_step()

    def sample_step(self):
        return np.random.randint(self.action_size)
