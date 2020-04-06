import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import matplotlib.pyplot as plt

class Market0(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, df):
        self.prices = df.loc[:, 'Close'].to_numpy()
        self.max_index = self.prices.size
        self.selection = []
        
        self.state_index = 0
        self.last_value = 0
        self.done = False
        
    def step(self, target):
        self.this_value = self.prices[self.state_index]

        self.reward = self.get_reward(target)
    
        self.last_value = self.this_value
        self.state_index += 1
        
        self.done = self.max_index == self.state_index

        return [self.state_index, self.reward, self.done]

    def get_reward(self, target):
        if self.last_value <= self.this_value and target == 0 or self.last_value > self.this_value and target == 1:
            self.selection.append("green")
            return 1
        self.selection.append("red")
        return -1
        
    def reset(self):
        self.done = False
        self.state_index = 0
        self.last_value = 0
        self.selection = []
        return self.state_index

    def render(self):
        plt.plot(self.prices)
        for index_row in range(self.state_index):
            plt.plot(index_row, self.prices[index_row], marker=".", color=self.selection[index_row])
        plt.show()