import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

CELL_COLORS = {
    0: 'white',        # EMPTY
    1: 'grey',         # DEPOT
    2: 'lightgreen',   # WORKSHOP
    3: 'orange',       # PARKING
    4: 'red',          # HAZARD
}

AGENT_MARKERS = {
    "worker": 'o',
    "vehicle": 's'
}

AGENT_COLORS = {
    "worker": 'blue',
    "vehicle": 'black'
}


class Renderer:
    def __init__(self, env):
        self.env = env
        grid = env.get_semantic_grid()
        self.h, self.w = grid.shape

        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # background
        cmap = ListedColormap([CELL_COLORS[i] for i in range(len(CELL_COLORS))])
        self.img = self.ax.imshow(
            grid,
            cmap=cmap,
            origin='upper',
            interpolation='none'
        )

        # axis limits
        self.ax.set_xlim(-0.5, self.w - 0.5)
        self.ax.set_ylim(self.h - 0.5, -0.5)
        self.ax.set_aspect('equal')

        # remove ticks
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # grid lines
        for x in range(self.w + 1):
            self.ax.plot(
                [x - 0.5, x - 0.5],
                [-0.5, self.h - 0.5],
                color='black',
                linewidth=0.5,
                zorder=2
            )

        for y in range(self.h + 1):
            self.ax.plot(
                [-0.5, self.w - 0.5],
                [y - 0.5, y - 0.5],
                color='black',
                linewidth=0.5,
                zorder=2
            )

        # legend
        semantic_legend_elements = [
            Patch(facecolor=CELL_COLORS[i], edgecolor='black', label=l)
            for i, l in enumerate(['EMPTY','DEPOT', 'WORKSHOP', 'PARKING', 'HAZARD'])
            if i != 0        # no EMPTY in legend list
        ]

        agent_legend_elements = [
            Line2D(
                [0], [0],
                marker=AGENT_MARKERS[k],
                color='w',
                label=k,
                markerfacecolor=AGENT_COLORS[k],
                markersize=10
            )
            for k in AGENT_MARKERS
        ]

        legend_elements = semantic_legend_elements + agent_legend_elements

        self.ax.legend(
            handles=legend_elements,
            loc='upper left',               
            bbox_to_anchor=(1.02, 1),       
            borderaxespad=0,               
            frameon=True
        )

        self.agent_scatters = []

    def render(self, t, pause_time=0.1):
        self.img.set_data(self.env.get_semantic_grid())

        # remove old agents
        for sc in self.agent_scatters:
            sc.remove()
        self.agent_scatters.clear()

        # draw agents
        for agent_type, (row, col) in self.env.get_agent_positions():
            sc = self.ax.scatter(
                col,
                row,
                marker=AGENT_MARKERS[agent_type],
                s=200,
                color=AGENT_COLORS[agent_type],
                zorder=3
            )
            self.agent_scatters.append(sc)

        self.ax.set_title(f"Simulation t = {t}")
        self.fig.canvas.draw_idle()
        plt.pause(pause_time)

    def close(self):
        plt.ioff()
        plt.close(self.fig)
