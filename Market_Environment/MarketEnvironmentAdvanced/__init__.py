from gym.envs.registration import register

register(
    id='Market-v2',
    entry_point='MarketEnvironmentAdvanced.envs:Market_Advanced',
)