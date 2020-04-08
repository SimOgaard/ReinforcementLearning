import numpy as np

class Agent0:
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        self.action_size = 2

    def act(self):
        return self.sample_step()

    def sample_step(self):
        return np.random.randint(self.action_size)
