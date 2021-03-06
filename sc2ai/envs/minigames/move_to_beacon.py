from sc2ai.envs.sc2env import SingleAgentSC2Env
from sc2ai.envs.actions import *
from sc2ai.envs.observations import *


class MoveToBeaconEnv(SingleAgentSC2Env):
    """A class containing specifications for the MoveToBeacon Minimap
    """
    def __init__(self, **kwargs):
        action_set = DefaultActionSet([
            NoOpAction(),
            SelectPointAction(select_point_act="select"),
            SelectRectAction(select_add="select"),
            SelectArmyAction(select_add="select"),
            MoveScreenAction(queued="now"),
        ])

        observation_set = ObservationSet([
            MapCategory("feature_screen", [
                FeatureScreenSelfUnitFilter(),
                FeatureScreenNeutralUnitFilter()])
        ])

        super().__init__("MoveToBeacon", action_set, observation_set, num_players=1, **kwargs)
