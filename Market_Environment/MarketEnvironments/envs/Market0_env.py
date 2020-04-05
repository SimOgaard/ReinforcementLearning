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

        if self.last_value <= self.this_value and target == 0 or self.last_value > self.this_value and target == 1:
            self.reward = 1
            self.selection.append("green")
        else:
            self.reward = -1
            self.selection.append("red")
    
        self.last_value = self.this_value
        self.state_index += 1
        if self.max_index == self.state_index:
            self.done = True

        return [self.state_index, self.reward, self.done]

    def reset(self):
        self.done = False
        self.state_index = 0
        self.last_value = 0
        self.selection = []

    def render(self):
        plt.plot(self.prices)
        for index_row in range(self.state_index):
            plt.plot(index_row, self.prices[index_row], marker=".", color=self.selection[index_row])
        plt.show()