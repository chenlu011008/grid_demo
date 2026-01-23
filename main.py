import matplotlib.pyplot as plt

from config import GRID_H, GRID_W, TIMESTEPS, PAUSE_TIME
from scenario.env import GridWorld, CellType
# from scenario.moving_policy_factory import move_towards_goal
from visualisation.render import Renderer

from utils.init_map import generate_random_map
from utils.init_agent import generate_random_agents

from evaluation.eval import SimulationEvaluator

plt.ion()

# --------------------------
# create map
# --------------------------
entities = []        # save static properties

layout = {
    CellType.DEPOT: [{"count": 1, "size": (3, 3),}, {"count": 1, "size": (5, 3),},],
    CellType.WORKSHOP: [{"count": 2,"size": (2, 2),}],
    CellType.PARKING: [{"count": 1,"size": (2, 2),}],
    CellType.HAZARD: [{"count": 0,"size": (1, 1),}]
    }    

map, entities = generate_random_map(GRID_H, GRID_W, layout)

# for e in entities:
#     print(e)

# --------------------------
# create agent
# --------------------------
agent_specs = {
    "worker": [{"count": 1, "policy": "move_towards_goal"}, {"count": 2}],
    "vehicle": [{"count": 1, "goal_chain":"vehicle_default"}]
    }

agents = generate_random_agents(map, agent_specs)

# for a in agents:
#     print(a)

# --------------------------
# create environment
# --------------------------
env = GridWorld(height=GRID_H, width=GRID_W, map=map, agents=agents)

# --------------------------
# simulation
# --------------------------
evaluator = SimulationEvaluator(env, agents)
renderer = Renderer(env)

for t in range(TIMESTEPS):

    actions = {}
    for agent in agents:
        actions[agent] = agent.act()

    env.step(actions)

    metrics = evaluator.eval_metrics()        

    renderer.render(t, PAUSE_TIME)
    renderer.render_metrics(metrics) 

renderer.close()