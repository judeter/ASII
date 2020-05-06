# -*- coding: utf-8 -*-
"""
Author: Justin Deterding

Description:
    This script is ment to illistrate the the ussage of the node commander.
"""
#TODO: update file name to demo_eonNodeCommander.py

# %% Imports
import EoN
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from random import seed
from random import normalvariate
import Utilities as util
import itertools as it
seed(10)


# %% Function definitions

def singleRun(graph, prob_trans, rho, node_commander, graph_commander):
    """
    single run produses result of a single run of the discreet SIR model. Runs
    are in herently probablistic so it is nessisary to do mutiple runs.
    Parameters
    ----------
    graph : TYPE
        DESCRIPTION.
    prob_trans : TYPE
        DESCRIPTION.
    rho : TYPE
        DESCRIPTION.
    graph_commander : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    results = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho,
                               node_commander=node_commander,
                               graph_commander=graph_commander)
    return results[1:]


#%% Graph Commander Set up
country_names = ['C1', 'C2', 'C3', 'C4']
country_cent = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
countries = {}
for country_name, xy_cent in zip(country_names, country_cent):
    # TODO: Make this more interesting
    g = util.random_2d_grid_graph(500, 0.2, normalvariate, args=(0, 0.4), 
                                  xy_cent=xy_cent) 

    mapping = {node: country_name+'_'+str(node) for node in g}
    nx.relabel_nodes(g, mapping, copy=False)

    countries[country_name] = {"tolerance_in": 0.2,
                               "tolerance_out": 0.2,
                               "G": g,
                               "infected": None,
                               "closed_borders": None}
    
G = nx.compose_all([countries[key]['G'] for key in countries])
# Adding intra connections to sub graphs
sub_graphs = [countries[key]['G'] for key in countries]
for pair in it.combinations(sub_graphs, 2):
    util.add_euclidian_edges(pair, 0.4, G=G)
nx.draw(G, pos=util.layout_2d(G), node_size=3)


#%%
rho = 0.001
prob_trans = 0.2

#%% Run scanario 
graph_commander = [countries, [G.copy()]]
args = (G.copy(), prob_trans, rho, graph_commander)
results = multiRun(singleRun, args)
    
#%% Calculate Mean and standard deviation of results

mean_results = results.mean(axis=0)
std_results = results.std(axis=0)    

#%% Plotting SIR-Degree Dynamics 

#%% 
"""
nx_kwargs = {'node_size':5}
full_data = EoN.discrete_SIR(g, args=(prob_trans,), rho=rho, 
                             return_full_data=True)
ani = full_data.animate(node_size=5, pos=layout_2d(g), width=0.125)

ani.save('demo_animationWithoutCmder.mp4', fps=5)
#%%
nx_kwargs = {'node_size':5}
full_data = EoN.discrete_SIR(g, args=(prob_trans,), rho=rho,
                             node_commander=nodeCommander,
                             return_full_data=True)
ani = full_data.animate(node_size=5, pos=layout_2d(g), width=0.125)

ani.save('demo_animationWithCmder.mp4', fps=5)
"""