from absl import app
from absl import flags

from pysc2.env import sc2_env
from pysc2.lib import point_flag

from sc2ai.env_interface import RoachesEnvironmentInterface, BeaconEnvironmentInterface
from sc2ai.environment import MultipleEnvironment, SCEnvironmentWrapper
from sc2ai.learner import Learner

FLAGS = flags.FLAGS
flags.DEFINE_bool("render", True, "Whether to render with pygame.")
point_flag.DEFINE_point("feature_screen_size", "84",
                        "Resolution for screen feature layers.")
point_flag.DEFINE_point("feature_minimap_size", "64",
                        "Resolution for minimap feature layers.")
point_flag.DEFINE_point("rgb_screen_size", None,
                        "Resolution for rendered screen.")
point_flag.DEFINE_point("rgb_minimap_size", None,
                        "Resolution for rendered minimap.")
flags.DEFINE_enum("action_space", None, sc2_env.ActionSpace._member_names_,  # pylint: disable=protected-access
                  "Which action space to use. Needed if you take both feature "
                  "and rgb observations.")
flags.DEFINE_bool("disable_fog", False, "Whether to disable Fog of War.")

flags.DEFINE_integer("max_agent_steps", 0, "Total agent steps.")
flags.DEFINE_integer("game_steps_per_episode", None, "Game steps per episode.")
flags.DEFINE_integer("max_episodes", 0, "Total episodes.")
flags.DEFINE_integer("step_mul", 8, "Game steps per agent step.")

flags.DEFINE_enum("agent_race", "random", sc2_env.Race._member_names_,  # pylint: disable=protected-access
                  "Agent 1's race.")
flags.DEFINE_bool("use_cuda", True, "Whether to train on gpu")
flags.DEFINE_integer("parallel", 1, "How many instances to run in parallel.")
flags.DEFINE_string("map", None, "Name of a map to use.")

flags.DEFINE_bool("load_model", False, "Whether to load the previous run's model")

flags.DEFINE_float("gamma", 0.96, "Discount factor")
flags.DEFINE_float("td_lambda", 0.96, "Lambda value for generalized advantage estimation")

flags.mark_flag_as_required("map")


def main(unused_argv):
    env_kwargs = {
        'map_name': FLAGS.map,
        'players': [sc2_env.Agent(sc2_env.Race[FLAGS.agent_race])],
        'agent_interface_format': sc2_env.parse_agent_interface_format(
            feature_screen=FLAGS.feature_screen_size,
            feature_minimap=FLAGS.feature_minimap_size,
            rgb_screen=FLAGS.rgb_screen_size,
            rgb_minimap=FLAGS.rgb_minimap_size,
            action_space=FLAGS.action_space,
            use_feature_units=True),
        'step_mul': FLAGS.step_mul,
        'game_steps_per_episode': FLAGS.game_steps_per_episode,
        'disable_fog': FLAGS.disable_fog,
        'visualize': FLAGS.render
    }

    if FLAGS.map == 'DefeatRoaches':
        interface = RoachesEnvironmentInterface()
    elif FLAGS.map == 'MoveToBeacon':
        interface = BeaconEnvironmentInterface()
    else:
        raise Exception('Unsupported Map')

    num_instances = 1 if FLAGS.render else FLAGS.parallel
    environment = MultipleEnvironment(lambda: SCEnvironmentWrapper(interface, env_kwargs),
                                      num_instance=num_instances)
    learner = Learner(environment, interface, use_cuda=FLAGS.use_cuda, load_model=FLAGS.load_model,
                      gamma=FLAGS.gamma, td_lambda=FLAGS.td_lambda)

    try:
        i = 0
        while not FLAGS.max_episodes or i < FLAGS.max_episodes:
            learner.train_episode()
            i += 1
    finally:
        environment.close()


if __name__ == "__main__":
    app.run(main)
