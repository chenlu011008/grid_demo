# eval metrics

# agent, time_needed (i.e., path_lengths), collision (int), objective_achieved (bool)

class SimulationEvaluator:
    def __init__(self, env, agents):
        self.env = env
        self.agents = agents
        # initialisation
        self.agent_paths = {agent.name: [agent.pos] for agent in agents}
        self.num_collisions = 0

    def record_step(self):
        """Record agent positions at each timestep, and num_collisions"""
        positions = {}
        for agent in self.agents:
            # agent paths
            self.agent_paths[agent.name].append(agent.pos)
            if agent.pos in positions:
                self.num_collisions += 1
            positions[agent.pos] = agent.name

    def compute_metrics(self):
        """Overall metrics"""
        path_lengths = {}
        for name, path in self.agent_paths.items():
            length = 0
            for (x0, y0), (x1, y1) in zip(path[:-1], path[1:]):
                length += abs(x1 - x0) + abs(y1 - y0)
            path_lengths[name] = length


        return {
            "path_lengths": path_lengths,
            "num_collisions": self.num_collisions,
        }

    def print_summary(self):
        metrics = self.compute_metrics()
        print("=== Simulation Metrics ===")
        print(f"Number of collisions: {metrics['num_collisions']}")
        for name, length in metrics["path_lengths"].items():
            print(f"{name} path length: {length}")
