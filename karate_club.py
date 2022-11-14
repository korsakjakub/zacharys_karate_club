import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os


def state_evolution(graph, diffusion_constant, dt):
    new_states = {}
    for h in graph:
        if h == 0:
            new_states[h] = 1.0
            continue
        elif h == 33:
            new_states[h] = 0.0
            continue
        else:
            new_states[h] = diffusion_constant * np.sum([(graph.nodes[g]["state"] - graph.nodes[h]["state"])
                                                        * graph[g][h]["weight"] for g in graph[h]]) * dt + graph.nodes[h]["state"]
    return new_states


def weight_evolution(graph, weight_constant, dt):
    new_weights = {}

    def f(x):
        return (x - 0.25)**3

    for j in graph:
        for i in graph[j]:
            new_weights[(j, i)] = -weight_constant * graph[i][j]["weight"] * (1 - graph[i][j]["weight"]) * \
                f(abs(graph.nodes[i]["state"] - graph.nodes[j]
                  ["state"])) * dt + graph[i][j]["weight"]
    return new_weights


def simulation(graph, config):
    G = graph
    diffusion_constant = config["diffusion_constant"]
    weights_constant = config["weights_constant"]
    dt = config["dt"]
    for time in range(1000):
        new_states = state_evolution(G, diffusion_constant, dt)
        new_weights = weight_evolution(G, weights_constant, dt)
        nx.set_node_attributes(G, new_states, "state")
        nx.set_edge_attributes(G, new_weights, "weight")
        if time % 10 == 0:
            nx.draw_spring(G, cmap=cm.cool, vmin=0, vmax=1, with_labels=True, node_color=[G.nodes[i]['state'] for i in G.nodes(
            )], edge_cmap=cm.binary, edge_vmin=0, edge_vmax=1, edge_color=[G[i][j]['weight'] for i, j in G.edges])
            plt.savefig(f"png/{time}.png")
            plt.close()
    os.system(f'cd png; files=$(ls *.png | sort -n -k1); convert -delay 20 $files animation.gif; rm *.png')


def _get_unbiased_initial_graph():
    G = nx.karate_club_graph()
    initial_states = {n: 0.5 for n in range(1, 33)}
    initial_states[0] = 1.0
    initial_states[33] = 0.0

    nx.set_node_attributes(G, initial_states, "state")
    nx.set_edge_attributes(G, 0.5, "weight")
    return G


def _get_real_initial_graph():
    with open("zachary.txt", "r") as f:
        data = (f.read())
    r = np.array(list(map(int, data.split(" "))))
    r = r / np.max(r)
    initial_weights = np.reshape(r, (34, 34))
    initial_weights_dict = {}
    for i, _ in enumerate(initial_weights):
        for j, _ in enumerate(initial_weights[i]):
            initial_weights_dict[(i, j)] = initial_weights[i][j]
    G = nx.karate_club_graph()
    initial_states = {n: 0.5 for n in range(1, 33)}
    initial_states[0] = 1.0
    initial_states[33] = 0.0
    nx.set_node_attributes(G, initial_states, "state")
    nx.set_edge_attributes(G, initial_weights_dict, "weight")


if __name__ == "__main__":
    initial_graph = _get_unbiased_initial_graph()
    # initial_graph = _get_real_initial_graph()

    simulation(graph=initial_graph,
               config={
                   "diffusion_constant": 5.0,
                   "weights_constant": 10.0,
                   "dt": 0.01
               })
