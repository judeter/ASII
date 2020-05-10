# -*- coding: utf-8 -*-
"""
Author: Justin Deterding

Description:
    This script utilizes both the node and graph commanders.
"""
# %% Imports and script setup
import EoN
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import random
import Utilities as util
import itertools as it

# Set random seed for reproducable results
random.seed(10)

# %% Function definitions

def singleRun(graph, prob_trans, rho, node_commander, graph_commander):
    """
    single run generates result from single run of the discreet SIR model. Runs
    are inherently probablistic so it is nessisary to do mutiple runs.

    """
    results = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho,
                               node_commander=node_commander,
                               graph_commander=graph_commander)
    # Dont return time, statistics on time variable are usless
    return results[1:]


#%% Graph Commander Set up
country_names = ['C1', 'C2', 'C3', 'C4']
country_cent = [(0.0, 0.0), (-1.0, 0.0), (0.0, -1.0), (-1.0, -1.0)]
graph_size = 500
max_connection_dist = 1.0/np.sqrt(graph_size)*2
countries = {}
for country_name, xy_cent in zip(country_names, country_cent):
    
    g = util.random_2d_grid_graph(graph_size, max_connection_dist, 
                                  random.random, xy_cent=xy_cent) 

    mapping = {node: country_name+'_'+str(node) for node in g}
    nx.relabel_nodes(g, mapping, copy=False)

    countries[country_name] = {"tolerance_in": 1.0,
                               "tolerance_out": None,
                               "G": g,
                               "infected": None,
                               "closed_borders": None}
    
G = nx.compose_all([countries[key]['G'] for key in countries])
# Adding intra connections to sub graphs
sub_graphs = [countries[key]['G'] for key in countries]
for pair in it.combinations(sub_graphs, 2):
    util.add_euclidian_edges(pair, max_connection_dist, G=G)
plt.figure()
nx.draw(G, pos=util.layout_2d(G), node_size=3)

graph_commander = [countries, [G.copy()]]

#%% SIR dynamics parameters

rho = 1/(graph_size*4)
prob_trans = 0.3

#%% Run baseline scanario 

node_commander = util.nodeCommandGennerator(util.quarentineNode,
                                            args=(0.0, 0.0))
graph_commander[0]['C1']['tolerance_out'] = 1.0
graph_commander[0]['C2']['tolerance_out'] = 1.0
graph_commander[0]['C3']['tolerance_out'] = 1.0
graph_commander[0]['C4']['tolerance_out'] = 1.0
args = (G.copy(), prob_trans, rho, node_commander, graph_commander)
base_line_results = util.multiRun(singleRun, args)
base_line_plot_pair = (base_line_results.mean(axis=0),
                       base_line_results.std(axis=0))
util.plot_SIRD([base_line_plot_pair], graph_size, fontsize=12)

#%% Run without quarenteen scanario 

node_commander = util.nodeCommandGennerator(util.quarentineNode,
                                            args=(0.0, 0.0))
gc_only_data = [base_line_plot_pair]
labels = ['0', '1', '2', '3']
for tol_set in [(0.01, 1.00, 1.00, 1.00),
                (0.01, 0.01, 1.00, 1.00),
                (0.01, 0.01, 0.01, 1.00)]:

    graph_commander[0]['C1']['tolerance_out'] = tol_set[0]
    graph_commander[0]['C2']['tolerance_out'] = tol_set[1]
    graph_commander[0]['C3']['tolerance_out'] = tol_set[2]
    graph_commander[0]['C4']['tolerance_out'] = tol_set[3]
    args = (G.copy(), prob_trans, rho, node_commander, graph_commander)
    results = util.multiRun(singleRun, args, 10)
    gc_only_data.append((results.mean(axis=0), 
                         results.std(axis=0)))


#%% Plor without quarenteen scanario  
linestyles = ['-', '--', ':', '-.']

util.plot_SIRD(gc_only_data, show_confidence_interval=False,
               linestyles=linestyles, labels=labels)

#%% 
"""
nx_kwargs = {'node_size':5}
full_data, checkpoints = EoN.discrete_SIR(G, args=(prob_trans,), rho=rho,
                                          node_commander=node_commander,
                                          graph_commander=graph_commander,
                                          return_full_data=True)
ani = full_data.animate(node_size=5, pos=util.layout_2d(G), width=0.125)

#ani.save('demo_dualCommander.mp4', fps=5)
"""
