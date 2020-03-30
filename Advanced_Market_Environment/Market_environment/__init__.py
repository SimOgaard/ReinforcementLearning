from gym.envs.registration import register
from copy import deepcopy
import os
import pandas as pd

def load_dataset(name, index_name):
    return pd.read_csv("/content/ReinforcementLearning/DataMarket/data/"+name, index_col=index_name)

df = load_dataset('AAP', 'Date')

register(
    id='market-v0',
    entry_point='Market_environment.envs:MarketEnv',
    kwargs={
        'df': deepcopy(df),
        'window_size': 30,
        'frame_bound': (30, len(df))
    }
)