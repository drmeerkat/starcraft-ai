import numpy as np
from gym import spaces
from pysc2.lib import actions, features

from ..sc2env import SingleAgentMiniGameEnv

class MoveToBeaconEnv(SingleAgentMiniGameEnv):
    """

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _process_reward(self, reward, raw_obs):
        raise NotImplementedError

    def _process_observation(self, raw_obs):
        raise NotImplementedError
