import numpy as np
from env import CellType
from env import StaticEntity
from agent import Agent

# --------------------------
# env
# --------------------------

def parse_static_spec(spec):
    """
        Returns:
            count: int
            size: (w, h) or None
            pos: (x, y) or None
    """
    if isinstance(spec, int):
        # e.g., CellType.HAZARD: 3 --> size: 1*1
        return spec, (1, 1), None

    if isinstance(spec, tuple):
        # e.g., CellType.DEPOT: (1, 2, 2)
        count, w, h = spec
        return count, (w, h), None

    if isinstance(spec, dict):
        # e.g., CellType.WORKSHOP: {"count": 1, "size": (3, 2), "pos": (0, 0)}                                                                                          
        count = spec.get("count", 1)
        size = spec.get("size", (1, 1))
        pos = spec.get("pos", None)
        return count, size, pos

    raise TypeError(f"Invalid static element spec: {spec}")

def generate_random_map(map_rows, map_cols, layout=None):
    """
    Generate a random map with static elements, supporting optional size and position
    """
    if layout is None:
        layout = {
            CellType.DEPOT: {"count": 1},
            CellType.WORKSHOP: {"count": 1},
            CellType.PARKING: {"count": 1},
            CellType.HAZARD: {"count": 0},
        }

    grid = np.full((map_rows, map_cols), CellType.EMPTY, dtype=object)
    entities = []
    type_counters = {ct: 0 for ct in layout.keys()}

    for cell_type, specs in layout.items():
        # for heterogeneous groups
        # e.g., 
        # layout = {
        #     CellType.DEPOT: [ {"count": 1, "size": (2,2), "pos": (7, 7)}, {"count": 2, "size": (1,3)} ],
        #     CellType.WORKSHOP: [ (2, 3, 2), 1 ],  # 2 of 3x2 + 1 of 1x1 (default)
        #     CellType.PARKING: 3,  # 3 of 1x1
        #     CellType.HAZARD: [ {"count": 3, "size": (1,1)} ]
        # }
        if not isinstance(specs, list):
            specs = [specs]
        
        for spec in specs:
            count, (w, h), pos = parse_static_spec(spec)

            for _ in range(count):
                if pos is not None:
                    x, y = pos
                    if x < 0 or y < 0 or x+h > map_rows or y+w > map_cols:
                        raise ValueError(f"Specified position {pos} with size {(w,h)} out of bounds")
                    area = grid[x:x+h, y:y+w]
                    if not np.all(area == CellType.EMPTY):
                        raise ValueError(f"Specified position {pos} for {cell_type} is occupied")
                else:
                    # random pos
                    while True:
                        x = np.random.randint(0, map_rows - h + 1)
                        y = np.random.randint(0, map_cols - w + 1)
                        area = grid[x:x+h, y:y+w]
                        if np.all(area == CellType.EMPTY):
                            break

                name = f"{cell_type.name}_{type_counters[cell_type]}"
                type_counters[cell_type] += 1

                grid[x:x+h, y:y+w] = cell_type

                entity = StaticEntity(cell_type, x, y, w, h, name)
                entities.append(entity)

    return grid, entities

# --------------------------
# agents
# --------------------------

def parse_agent_spec(spec):
    """
    Returns:
        count: int
        extra: dict, other parameters for Agents
    """
    if isinstance(spec, int):
        # e.g., 
        # agent_specs = {
        # "worker": 3,
        # "vehicle": 2
        # }
        extra = {}
        return spec, extra

    if isinstance(spec, dict):
        # e.g., 
        # agent_specs = {
        # "worker": {"count": 3},
        # "vehicle": {"count": 2, "pos": [(0, 0),(1, 1)], "policy": "move_towards_goal"}
        # }
        count = spec.get("count", 1)
        extra = spec.copy()
        extra.pop("count", None)  

        return count, extra

    raise TypeError(f"Invalid agent spec: {spec}")


def generate_random_agents(map, agent_specs):
    """
    Generate random agent population, supporting optional position, policy (, and etc. like speed)
    """
    if agent_specs is None:
        agent_specs = {"worker": 1, "vehicle": 1}
    
    h, w = map.shape
    agents = []
    occupied = set()

    for agent_type, specs in agent_specs.items():
        # for heterogeneous groups
        # e.g., 
        # agent_specs = {
        #     "worker": [
        #         {"count": 2, "policy": ["move_towards_goal", "..."]},
        #         {"count": 1, "speed": 3}  # 1 worker with a speed of 3
        #     ],
        #     "vehicle": [
        #         2,  # 2 vehicles with default params 
        #         {"count": 1, "pos": [(5,5)], "speed": 6}
        #     ]
        # }
        if not isinstance(specs, list):
            specs = [specs]

        for spec in specs:

            n_agents, extra_kwargs = parse_agent_spec(spec)

            # convert all single values into lists of length n_agents
            for k, v in extra_kwargs.items():
                if not isinstance(v, list):
                    extra_kwargs[k] = [v] * n_agents
                elif len(v) != n_agents:
                    raise ValueError(f"Length of {k} ({len(v)}) != count {n_agents}")

            for i in range(n_agents):
                # if pos is not specified, generate it randomly
                # ------------------------------------------
                # TO DO: 
                # extended to other params (policy, spd, ...)
                # ------------------------------------------
                if "pos" not in extra_kwargs or extra_kwargs["pos"][i] is None:
                    placed = False
                    while not placed:
                        x = np.random.randint(0, h)
                        y = np.random.randint(0, w)
                        if map[x, y] == CellType.EMPTY and (x, y) not in occupied:
                            extra_kwargs.setdefault("pos", [None]*n_agents)[i] = (x, y)
                            placed = True
                else:
                    # --- if pos is specified, ignore occupancy conflicts --- #
                    x, y = extra_kwargs["pos"][i]
                    # if map[x, y] != CellType.EMPTY or (x, y) in occupied:
                    #    raise ValueError(f"Specified pos {(x, y)} for {agent_type} is not empty")

                name = f"{agent_type}_{i}"

                agent_params = {k: extra_kwargs[k][i] for k in extra_kwargs}
                agent_params["agent_type"] = agent_type
                agent_params["map"] = map
                agent_params["name"] = name

                agent = Agent(**agent_params)
                agents.append(agent)
                occupied.add(agent.pos)

    return agents



