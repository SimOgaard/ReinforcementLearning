import gym
from gym import error, spaces, utils
from gym.utils import seeding
import pandas as pd
import matplotlib.pyplot as plt

class Market_Basic(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, df):
        self.df = df
        self.max_index = pd.Index(self.df["Open"]).size
        self.state_index = 0
        self.last_value = 0
        self.done = False
        self.df[["Close"]].plot()

    def step(self, target):

        self.this_value = self.df.loc[self.state_index, "Open"]

        if self.last_value <= self.this_value and target == 0 or self.last_value > self.this_value and target == 1:
            self.reward = 1
        else:
            self.reward = -1
        plt.plot(self.state_index, self.this_value, marker=".", color='green' if self.reward==1 else "red")

        self.last_value = self.this_value
        self.state_index += 1
        if self.max_index == self.state_index:
            self.done = True

        return [self.state_index, self.reward, self.done]

    def reset(self):
        self.done = False
        self.state_index = 0
        self.last_value = 0
        self.df[["Close"]].plot()

    def render(self):
        plt.show()