from sc2ai.envs.sc2env import SingleAgentSC2Env
from sc2ai.envs.actions import *
from sc2ai.envs.observations import *


class FleeRoachesEnv(SingleAgentSC2Env):
    """A class containing specifications for the FleeRoaches Minimap
    """
    def __init__(self, **kwargs):
        action_set = DefaultActionSet([
            NoOpAction(),
            SelectPointAction(select_point_act="select"),
            SelectRectAction(select_add="select"),
            SelectArmyAction(select_add="select"),
            AttackScreenAction(queued="now")
        ])

        observation_set = ObservationSet([
            MapCategory("feature_screen", [
                FeatureScreenSelfUnitFilter(),
                FeatureScreenNeutralUnitFilter(),
                FeatureScreenEnemyUnitFilter(),
                FeatureScreenUnitHitPointFilter()])
        ])

        super().__init__("FleeRoachesv4_training", action_set, observation_set, num_players=1, **kwargs)

    def step(self, _actions):
        obs, total_reward, done, info = super().step(_actions)
        if total_reward > 0:
            total_reward = 0
        return obs, total_reward, done, info
