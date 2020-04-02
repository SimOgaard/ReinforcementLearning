import gym
from gym import error, spaces, utils
from gym.utils import seeding
import pandas as pd
import matplotlib.pyplot as plt

class Market_Medium(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, df):
        self.df = df
        self.df.append(pd.Series(name="Color"))
        self.max_index = pd.Index(self.df["Open"]).size
        
        self.state_index = 0
        self.last_value = 0
        self.done = False
        
    def step(self, target):
        self.this_value = self.df.loc[self.state_index, "Open"]

        if self.last_value <= self.this_value and target == 0 or self.last_value > self.this_value and target == 1:
            self.reward = 1
            self.df.loc[self.state_index, "Color"] = "green"
        else:
            self.reward = -1
            self.df.loc[self.state_index, "Color"] = "red"
    
        self.last_value = self.this_value
        self.state_index += 1
        if self.max_index == self.state_index:
            self.done = True

        return [self.state_index, self.reward, self.done]

    def reset(self):
        self.done = False
        self.state_index = 0
        self.last_value = 0

    def render(self):
        self.df[["Close"]].plot()
        for index_row in range(self.state_index):
            plt.plot(index_row, self.df.loc[index_row, "Open"], marker=".", color=self.df.loc[index_row, "Color"])
        plt.show()