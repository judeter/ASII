# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:56:00 2020

@author: cathe
"""
import networkx as nx
import matplotlib.pyplot as plt
import topdown_buildinggraphs as td
import random

# Had to add simulation.py to my path, pip install wouldn't work properly
import sys
sys.path.insert(1, "C:\\Users\\cathe\\PycharmProjects\\Mathematics-of-Epidemics-on-Networks\\EoN\\")
import simulation as sim

countries = td.build_countries_dictionary()
G = td.get_composed_graph(nx.Graph(), countries)

init_infected = 0.05
r_naught = 0.4


def make_pos():
    node_pos = {}
    for c in countries:
        c_G = countries[c]["G"]
        for node in c_G.nodes:
            x_range = countries[c]["x_range"]
            y_range = countries[c]["y_range"]
            node_pos[node] = (random.uniform(x_range[0], x_range[1]),
                              random.uniform(y_range[0], y_range[1]))
    return node_pos


def plot_animation(save=False):
    positions = make_pos()
    full_data, checkpoints = sim.discrete_SIR(G, args=(0.3,), rho=0.05,
                                              return_full_data=True,
                                              graph_commander=[countries,
                                                               [G.copy()]])
    ani = full_data.animate(ts_plots=['I', 'SIR'],
                            node_size=250,
                            pos=positions)
#    for graph in checkpoints:
#        plt.figure()
#        nx.draw(graph, pos=positions)
    if save:
        ani.save('SIR_topdown.mp4', fps=5, extra_args=['-vcodec', 'libx264'])


def plot_graph_alone():
    t, S, I, R = sim.discrete_SIR(G, args=(r_naught,), rho=init_infected,
                                  graph_commander=[countries, [G.copy()]])
    # Plot
    plt.figure(figsize=(20, 8))
    plt.rcParams.update({'font.size': 25})
    plt.plot(t, S, color='green', lw=3, label='S')
    plt.plot(t, I, color='red', lw=3, label='I')
    plt.plot(t, R, color='blue', lw=3, label='R')
    plt.title('SIR model with {:.0f}% initially infected and $R_0$ = {}'
              .format(init_infected*100, r_naught))
    plt.grid()
    plt.legend()
    plt.show()
