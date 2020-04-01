import gym
from gym import error, spaces, utils
from gym.utils import seeding
import pandas as pd
import matplotlib.pyplot as plt

class Market_Basic(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, df):
        self.df = df
        self.df.append(pd.Series(name="Guess"))
        self.state_index = 0
        self.reward = 0
        self.last_value = 0
        self.done = False

    def step(self, target):

        if self.last_value <= self.df.loc[self.state_index, "Open"] and target == 0 or self.last_value > self.df.loc[self.state_index, "Open"] and target == 1:
            self.reward = 1
            self.df.loc[self.state_index,"Guess"] = 1
        else:
            self.reward = -1
            self.df.loc[self.state_index,"Guess"] = 0
        
        self.last_value = self.df.loc[self.state_index, "Open"]
        self.state_index += 1
        if pd.Index(self.df["Open"]).size == self.state_index:
            self.done = True

        return [self.state_index, self.reward, self.done]

    def reset(self):
        self.done = False
        self.state_index = 0
        self.reward = 0
        self.last_value = 0

    def render(self):
        self.df.plot(kind='scatter',x=self.df.index.values,y='Close',color='red')