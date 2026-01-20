import numpy as np
from enum import Enum

class CellType(Enum):
    EMPTY = 0
    DEPOT = 1
    WORKSHOP = 2
    PARKING = 3
    HAZARD = 4

class StaticEntity:
    def __init__(self, cell_type, x, y, w, h, name=None):
        self.cell_type = cell_type
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name        # optional

    def area(self):
        # covered areas as a list of (x, y)
        return [(self.x + dx, self.y + dy) for dx in range(self.h) for dy in range(self.w)]

    def __repr__(self):
        return f"{self.name}, loc=({self.x},{self.y}), size=({self.w},{self.h})"


class GridWorld:
    def __init__(self, height, width, map, agents):
        self.height = height
        self.width = width
        self.map = map          # semantic map -- static occupancy 
        self.agents = agents           # agent population

        self.occupancy = np.full((height, width), None)        # -- dynamic occupancy (i.e., agents)
        for agent in agents:
            x, y = agent.pos
            self.occupancy[x, y] = agent                    # pointer

    # ---------------------------------------------------
    # Staics
    # ---------------------------------------------------
    def in_bounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width        # return True or False

    def is_walkable(self, agent, x, y):
        if not self.in_bounds(x, y):
            return False

        cell = self.map[x, y]

        # not occupiable grid type
        if cell == CellType.HAZARD:      # not condider current occupancies or assume next actions of other agents
            return False

        return True

    # ---------------------------------------------------
    # Dynamics
    # ---------------------------------------------------
    def step(self, actions):
        for agent, move in actions.items():
            x, y = agent.pos
            dx, dy = move
            nx, ny = x + dx, y + dy

            if self.is_walkable(agent, nx, ny):        # if walkable, move and update occupancy
                self.occupancy[x, y] = None
                agent.pos = (nx, ny)
                self.occupancy[nx, ny] = agent    

    # ---------------------------------------------------
    # Rendering
    # ---------------------------------------------------
    def get_semantic_grid(self):        # statics
        grid = np.zeros((self.height, self.width))
        for x in range(self.height):
            for y in range(self.width):
                grid[x, y] = self.map[x, y].value
        return grid        # return 2-dimensional integer array

    def get_agent_positions(self):      # dynamics
        positions = []
        for agent in self.agents:
            positions.append((agent.agent_type, agent.pos))
        return positions
    
    
