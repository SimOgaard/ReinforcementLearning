from gym.envs.registration import register
from copy import deepcopy

from . import datasets


register(
    id='market-v0',
    entry_point='Market_environment.envs:MarketEnv',
    kwargs={
        'df': deepcopy(datasets.A),
        'window_size': 30,
        'frame_bound': (30, len(datasets.A))
    }
)
