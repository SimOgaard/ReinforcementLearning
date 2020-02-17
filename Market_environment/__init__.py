from gym.envs.registration import register
from copy import deepcopy
from datasets.utils import load_dataset as _load_dataset

df = _load_dataset('A', 'Date')

register(
    # DF = _load_dataset('A', 'Date')
    id='market-v0',
    entry_point='Market_environment.envs:MarketEnv',
    kwargs={
        'df': deepcopy(datasets.df),
        'window_size': 30,
        'frame_bound': (30, len(datasets.df))
    }
)