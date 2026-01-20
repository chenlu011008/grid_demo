import random
from env import CellType
from policy import move_towards_goal


class Agent:
    def __init__(self, agent_type, pos, map, name=None, policy=move_towards_goal):
        """
        agent_type: "worker" or "vehicle"
        pos: tuple (x, y)
        map: static_map --> 2d array
        """
        self.agent_type = agent_type
        self.pos = pos

        self.goals = self.generate_goals(map)
        self.current_goal_idx = 0

        self.name = name        # optional
        self.policy = policy
    
    def __repr__(self):
        return f"{self.name}, pos={self.pos}, policy={self.policy.__name__}"

    @property
    def current_goal(self):       # check the progress of the objectives
        if self.current_goal_idx < len(self.goals):
            return self.goals[self.current_goal_idx]
        else:
            return None  

    def act(self):
        if self.current_goal is None:
            return (0, 0)        # all objectives achieved (dx, dy) = (0, 0)
        
        move = self.policy(self)

        next_pos = (self.pos[0] + move[0], self.pos[1] + move[1])
        if next_pos == self.current_goal:
            self.current_goal_idx += 1
            # print(self.current_goal_idx)
        
        return move

    # -------------------------------
    # Goal generation based on agent_type
    # -------------------------------
    def generate_goals(self, map):
        """
        return list of goal pos [(x1,y1), (x2,y2), ...]
        """
        goals = []
        if self.agent_type == "worker":
            # worker: start -> workshop
            goals = generate_goals_by_type(map, [CellType.WORKSHOP])
        elif self.agent_type == "vehicle":
            # vehicle: start -> depot -> workshop -> parking
            goals = generate_goals_by_type(map, [CellType.DEPOT, CellType.WORKSHOP, CellType.PARKING])
        else:
            goals = []
        return goals


def generate_goals_by_type(map, cell_types):
    """
    return [(x1,y1), (x2,y2), ...]
    """
    goals = []
    rows, cols = map.shape
    for ctype in cell_types:
        valid_cells = [
            (x, y) for x in range(rows) for y in range(cols)
            if map[x, y] == ctype
        ]
        if valid_cells:
            goals.append(random.choice(valid_cells))       # randomly select a feasible cell for each goal

    # print(goals)
    return goals
