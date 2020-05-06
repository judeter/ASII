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
from random import random as rand
from Utilities import random_2d_grid_graph, layout_2d, multiRun, plot_SIRD

seed(10)


# %% Function definitions

def singleRunCmderFalse(graph, prob_trans, rho):
    no_node_cmd = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho)
    return no_node_cmd[1:]


def singleRunCmderTrue(graph, prob_trans, rho, node_commander):
    yes_node_cmd = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho,
                                    node_commander=nodeCommander)
    return yes_node_cmd[1:]


def nodeCommander(neighbors, connected_neighbors, susceptible_neighbors, 
                  infected_neighbors):
    from random import sample
    
    if len(infected_neighbors) > 0:    
        return [], sample(connected_neighbors, len(connected_neighbors)//4)
    else:
        unconnected_neighbors = neighbors.difference(connected_neighbors)
        return unconnected_neighbors, []


#%% Scanrio Parameters

#g = nx.configuration_model([randint(1, 15) for i in range(999)])
g = random_2d_grid_graph(1000,0.1,rand)
print(nx.info(g))
rho = 0.001
prob_trans = 0.2

#%% Run scanario with Node Comander
args = (g.copy(), prob_trans, rho, nodeCommander)
cmder_true_results = multiRun(singleRunCmderTrue, args)
#%% Run scanario without Node Comander
args = (g.copy(), prob_trans, rho)
cmder_false_results = multiRun(singleRunCmderFalse, args)    
#%% Calculate Mean and standard deviation of results

cmder_false_mean = cmder_false_results.mean(axis=0)
cmder_true_mean = cmder_true_results.mean(axis=0)    
cmder_false_std = cmder_false_results.std(axis=0)
cmder_true_std = cmder_true_results.std(axis=0)    

#%% Plotting SIR-Degree Dynamics 
plot_SIRD(cmder_false_mean, cmder_false_std, 
          cmder_true_mean, cmder_true_std)

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