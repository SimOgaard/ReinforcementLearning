from gym.envs.registration import register
from copy import deepcopy
import os
import pandas as pd

def load_dataset(name, index_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, 'datasets/data', name + '.csv')
    return pd.read_csv(path, index_col=index_name)

register(
    id='market-v0',
    entry_point='Market_environment.envs:MarketEnv',
    kwargs={
        'df': deepcopy(df),
        'window_size': 30,
        'frame_bound': (30, len(df))
    }
)