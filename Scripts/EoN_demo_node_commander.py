# -*- coding: utf-8 -*-
"""
Author: Justin Deterding

Description:
    This script is ment to illistrate the the ussage of the node commander.
"""

# %% Imports
import EoN
import networkx as nx
from matplotlib import pyplot as plt


# %% Function definitions

def singleRunCmderFalse():
    G = nx.grid_2d_graph(100, 100)
    no_node_cmd = EoN.discrete_SIR(G, args=(0.4,), rho=0.05)
    return no_node_cmd[1:]


def singleRunCmderTrue():
    G = nx.grid_2d_graph(100, 100)
    yes_node_cmd = EoN.discrete_SIR(G, args=(0.4,), rho=0.05,
                                    node_commander=nodeCommander)
    return yes_node_cmd[1:]


def combineResults(results):
    import numpy as np
    
    max_len_run = max([len(run[0]) for run in results])
    
    combined_arr = np.array([np.pad(run, ((0, 0), 
                                         (0, max_len_run-len(run[0]))), 
                                    mode='edge') 
                             for run in results])
    
    return combined_arr


def multiRun(single_run, N=10):
    results = [single_run() for i in range(N)]
    return combineResults(results)


def nodeCommander(neighbors, connected_neighbors, susceptible_neighbors, 
                  infected_neighbors):
    from random import sample
    if len(infected_neighbors) > 0:    
        return [], sample(connected_neighbors, len(connected_neighbors)//2)
    else:
        return [], []


#%% Run scanario with Node Comander

cmber_true_results = multiRun(singleRunCmderTrue)
#%% Run scanario without Node Comander

cmber_false_results = multiRun(singleRunCmderFalse)    
#%% Calculate Mean of results

cmber_false_mean = cmber_false_results.mean(axis=0)
cmber_true_mean = cmber_true_results.mean(axis=0)    

#%% Plotting    
fig, axarr = plt.subplots(nrows=3, ncols=1, sharex=True)

axarr[0].set_title('Susceptible')
axarr[0].plot(cmber_false_mean[0], '-g', label='no commander')
axarr[0].plot(cmber_true_mean[0], '--g', label='yes commander')

axarr[1].set_title('Infected')
axarr[1].plot(cmber_false_mean[1], '-r', label='no commander')
axarr[1].plot(cmber_true_mean[1], '--r', label='yes commander')

axarr[2].set_title('Recovered')
axarr[2].plot(cmber_false_mean[2], '-k', label='no commander')
axarr[2].plot(cmber_true_mean[2], '--k', label='yes commander')

plt.legend()
