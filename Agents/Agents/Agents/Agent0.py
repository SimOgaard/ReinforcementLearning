import numpy as np

class Agent0:

    def __init__(self, action_size):
        self.action_size = action_size

    def act(self):
        return np.random.randint(self.action_size)
