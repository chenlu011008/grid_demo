import random
from config import DEFAULT_EXEC_STEPS
from scenario.env import CellType


class Goal:
    def __init__(self, pos, executing_steps=DEFAULT_EXEC_STEPS):
        self.pos = pos
        self.executing_steps = executing_steps

    def is_satisfied(self, agent):
        return agent.pos == self.pos
    
# --------------------------
# Executable Tasks
# --------------------------

TASK_EXEC_TIME = {
    
    # worker
    "processing": 5,
    "rest": 15,

    # vehicle
    "loading": 5,
    "unloading": 5,
    "parking": 10,

    # --> add various tasks and exec_steps here <--
    # ......
}


# --------------------------
# Goal Chains
# --------------------------

# for both finite and infinite simulation
# a goal chain = a list of Goal objects (pos, executing_steps)


INIT_GOAL_CHAIN = {
    
    "worker_default": [
        {"location": [CellType.WORKSHOP], "task": "processing"},
        ],
        
    "vehicle_default": [
        {"location": [CellType.DEPOT], "task": "loading"},
        {"location": [CellType.WORKSHOP], "task": "unloading"},
        {"location": [CellType.PARKING], "task": "parking"},
        ],

    # --> add various chains here <--
    # ......

}

# for infinite simulation --> new goal generation strategy
ACTIVE_GOAL_CHAIN = {

      "worker_default": [
        {"location": [CellType.WORKSHOP], "task": "processing"},
        ],

    "vehicle_default": [
        {"location": [CellType.DEPOT], "task": "loading"},
        {"location": [CellType.WORKSHOP], "task": "unloading"},
        {"location": [CellType.PARKING], "task": "parking"},
        ],

    # --> add various chains here <--
    # ......

}


# ----------------
# Goal Generation
# ----------------

def sample_goal(grid, cell_types, task_name):
    """
    return a Goal object
    --> specify a target cell from all valid cells as the goal pas
    """
    rows, cols = grid.shape
    valid_cells = [
        (x, y) 
        for x in range(rows) 
        for y in range(cols) 
        if grid[x, y] in cell_types
    ]

    if not valid_cells:
        return None

    pos = random.choice(valid_cells)
    executing_steps = TASK_EXEC_TIME.get(task_name, 5)

    return Goal(pos, executing_steps)


def build_init_goal(agent, chain_name):
    chain = INIT_GOAL_CHAIN.get(chain_name, [])
    goals = []

    for goal_info in chain:
        goal = sample_goal(agent.map, goal_info["location"], goal_info["task"])
        if goal:
            goals.append(goal)

    return goals

def build_active_goal(agent, chain_name):
    chain = ACTIVE_GOAL_CHAIN.get(chain_name, [])
    goals = []

    for goal_info in chain:
        goal = sample_goal(agent.map, goal_info["location"], goal_info["task"])
        if goal:
            goals.append(goal)

    return goals