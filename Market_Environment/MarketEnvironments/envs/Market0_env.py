import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import matplotlib.pyplot as plt

class Market0(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, df):
        self.prices = df.loc[:, 'Close'].to_numpy()
        self.max_index = self.prices.size-1
        self.selection_plot = []
        self.reward_plot = []

        self.state_index = 0
        self.done = False

    def step(self, target):
        self.selection_plot.append("red" if target else "green")
        self.this_value = self.prices[self.state_index]
        self.next_value = self.prices[self.state_index+1]

        self.reward = self.get_reward(target)
    
        self.state_index += 1
    
        self.done = self.max_index == self.state_index

        return [self.state_index, self.reward, self.done]

    def get_reward(self, target):
        if self.this_value <= self.next_value and target == 0 or self.this_value > self.next_value and target == 1:
            self.reward_plot.append("green")
            return 1
        self.reward_plot.append("red")
        return -1
        
    def reset(self):
        self.done = False
        self.state_index = 0
        self.selection_plot = []
        self.reward_plot = []
        return self.state_index

    def render(self, plots):
        plt.plot(self.prices)
        for index_row in range(self.state_index):
            plt.plot(index_row, self.prices[index_row], marker=".", color=plots[index_row])
        plt.show()
