from enum import Enum

from scenario.goal_factory import build_init_goal, build_active_goal
from scenario.moving_policy_factory import build_policy

from config import SIM_TYPE

class AgentStatus(Enum):
    MOVING = 0        # move to the next goal ( <-- policy )
    EXECUTING = 1     # execute the task in a certain entity (keep current position)
    DONE = 2          # complete all goals (keep current position)

class Agent:
    def __init__(self, agent_type, pos, map, name=None, goal_chain="worker_default", active_goal_chain=None, policy="move_towards_goal"):
        """
        agent_type: "worker" or "vehicle"
        pos: tuple (x, y)
        map: static_map --> 2d array
        """
        self.agent_type = agent_type

        self.pos = pos
        self.map = map
        self.goal_chain = goal_chain
        self.active_goal_chain = active_goal_chain or goal_chain
        self.goals = build_init_goal(self, goal_chain)
        
        self.current_goal_idx = 0
        self.status = AgentStatus.MOVING
        self.execute_timer = 0  # record the duration at executing phase

        self.name = name        # required for evaluation and rendering
        self.policy = build_policy(policy)
    
    def __repr__(self):
        return f"{self.name}, pos={self.pos}, policy={self.policy.__name__}"
    
    @property
    def current_goal(self):       # check the progress of the objectives
        # return an objective of Goal
        if self.current_goal_idx < len(self.goals):
            return self.goals[self.current_goal_idx]
        else:
            return None  

    def act(self):
        
        # status = Done
        if self.status == AgentStatus.DONE:
            return (0, 0)        # all objectives achieved (dx, dy) = (0, 0)
        
        # status = Moving
        if self.status == AgentStatus.MOVING:
            # current goal achieved: status --> Executing
            if self.current_goal.is_satisfied(self):
                self.status = AgentStatus.EXECUTING
                self.execute_timer = 0
                return (0, 0)

            return self.policy(self)
        
        # status = Executing
        if self.status == AgentStatus.EXECUTING:
            self.execute_timer += 1

            # if reach executing_steps, status --> Done / Moving (to the next goal)
            if self.execute_timer >= self.current_goal.executing_steps:
                self.current_goal_idx += 1
            
                if self.current_goal is None:
                    if SIM_TYPE == "INFINITE":
                        # generate additional goals and append to initial goals
                        # new_goal = append_new_goal(self)
                        # self.goals.append(new_goal)
                        new_goal = build_active_goal(self, self.active_goal_chain)
                        if new_goal:
                            for g in new_goal:
                                self.goals.append(g)
                            #self.goals.append(new_goal)
                            
                        self.status = AgentStatus.MOVING

                    else:
                        self.status = AgentStatus.DONE      # mark DONE
                else:
                    self.status = AgentStatus.MOVING

            return (0, 0)


