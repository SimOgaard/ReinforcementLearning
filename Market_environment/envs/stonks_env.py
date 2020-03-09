import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import matplotlib.pyplot as plt

class TradingEnv(gym.Env):

    metadata = {'render.modes': ['human']}
    
    def __init__(self, df):