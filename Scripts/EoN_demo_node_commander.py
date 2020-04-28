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


# %% Function definitions

def singleRunCmderFalse(graph, prob_trans, rho):
    no_node_cmd = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho)
    return no_node_cmd[1:]


def singleRunCmderTrue(graph, prob_trans, rho, node_commander):
    yes_node_cmd = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho,
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


def multiRun(single_run, args, N=10):
    results = [single_run(*args) for i in range(N)]
    return combineResults(results)


def nodeCommander(neighbors, connected_neighbors, susceptible_neighbors, 
                  infected_neighbors):
    from random import sample
    if len(infected_neighbors) > 0:    
        return [], sample(connected_neighbors, len(connected_neighbors)//2)
    else:
        return [], []


#%% Scanrio Parameters

g = nx.grid_2d_graph(100, 100)
rho = 0.05
prob_trans = 0.6

#%% Run scanario with Node Comander
args = (g.copy(), prob_trans, rho, nodeCommander)
cmber_true_results = multiRun(singleRunCmderTrue, args=args)
#%% Run scanario without Node Comander
args = (g.copy(), prob_trans, rho)
cmber_false_results = multiRun(singleRunCmderFalse, args=args)    
#%% Calculate Mean and standard deviation of results

cmber_false_mean = cmber_false_results.mean(axis=0)
cmber_true_mean = cmber_true_results.mean(axis=0)    
cmber_false_std = cmber_false_results.std(axis=0)
cmber_true_std = cmber_true_results.std(axis=0)    

#%% Plotting    
fig, axarr = plt.subplots(nrows=3, ncols=1, sharex=True)

axarr[0].set_title('Susceptible')
axarr[0].plot(cmber_false_mean[0], '-g', label='no commander')
axarr[0].plot(cmber_true_mean[0], '--g', label='yes commander')

axarr[1].set_title('Infected')
axarr[1].plot(cmber_false_mean[1], '-r', label='no commander')
upper_95pct = cmber_false_mean[1]+cmber_false_std[1] 
lower_95pct = cmber_false_mean[1]-cmber_false_std[1]
x = np.arange(len(cmber_false_std[1]))
axarr[1].fill_between(x, upper_95pct, lower_95pct, color='r', alpha=0.1)

axarr[1].fill_between(x, upper_95pct, lower_95pct, color='r', alpha=0.1)
axarr[1].plot(cmber_true_mean[1], '--r', label='yes commander')
upper_95pct = cmber_true_mean[1]+cmber_true_std[1] 
lower_95pct = cmber_true_mean[1]-cmber_true_std[1]
x = np.arange(len(cmber_true_std[1]))
axarr[1].fill_between(x, upper_95pct, lower_95pct, color='r', alpha=0.1)

axarr[2].set_title('Recovered')
axarr[2].plot(cmber_false_mean[2], '-k', label='no commander')
axarr[2].plot(cmber_true_mean[2], '--k', label='yes commander')

plt.legend()
