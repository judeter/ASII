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
from Utilities import random_2d_grid_graph, layout_2d

seed(10)


# %% Function definitions

def singleRunCmderFalse(graph, prob_trans, rho):
    no_node_cmd = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho)
    return no_node_cmd[1:]


def singleRunCmderTrue(graph, prob_trans, rho, node_commander):
    yes_node_cmd = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho,
                                    node_commander=nodeCommander)
    return yes_node_cmd[1:]


def combineResults(results):
    """
    Take a list of numpy arrays. Each numpy array should have an equal number 
    of collumns, with variying numbers of rows. The results are combined into
    a single numpy array with dimention {num_runs,num_output,max_output_len}.
    
    Parameters
    ----------
    results : list of list or arrays
        The results from various runs of multiRun are stored in a list, called 
        results.

    Returns
    -------
    combined_arr : numpy array
        single numpy array with dimention {num_runs,num_output,max_output_len}.

    """
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
cmder_true_results = multiRun(singleRunCmderTrue, args=args)
#%% Run scanario without Node Comander
args = (g.copy(), prob_trans, rho)
cmder_false_results = multiRun(singleRunCmderFalse, args=args)    
#%% Calculate Mean and standard deviation of results

cmder_false_mean = cmder_false_results.mean(axis=0)
cmder_true_mean = cmder_true_results.mean(axis=0)    
cmder_false_std = cmder_false_results.std(axis=0)
cmder_true_std = cmder_true_results.std(axis=0)    

#%% Plotting SIR-Degree Dynamics 
fig, axarr = plt.subplots(nrows=4, ncols=1, sharex=True)

axarr[0].set_title('Susceptible')
axarr[0].plot(cmder_false_mean[0], '-g', label='no commander')
axarr[0].plot(cmder_true_mean[0], '--g', label='yes commander')

axarr[1].set_title('Infected')
axarr[1].plot(cmder_false_mean[1], '-r', label='no commander')
upper_95pct = cmder_false_mean[1]+cmder_false_std[1] 
lower_95pct = cmder_false_mean[1]-cmder_false_std[1]
x = np.arange(len(cmder_false_std[1]))
axarr[1].fill_between(x, upper_95pct, lower_95pct, color='r', alpha=0.1)

axarr[1].fill_between(x, upper_95pct, lower_95pct, color='r', alpha=0.1)
axarr[1].plot(cmder_true_mean[1], '--r', label='yes commander')
upper_95pct = cmder_true_mean[1]+cmder_true_std[1] 
lower_95pct = cmder_true_mean[1]-cmder_true_std[1]
x = np.arange(len(cmder_true_std[1]))
axarr[1].fill_between(x, upper_95pct, lower_95pct, color='r', alpha=0.1)

axarr[2].set_title('Recovered')
axarr[2].plot(cmder_false_mean[2], '-k', label='no commander')
axarr[2].plot(cmder_true_mean[2], '--k', label='yes commander')

axarr[3].set_title('Average Degree')
axarr[3].plot(cmder_false_mean[3], '-k', label='no commander')
axarr[3].plot(cmder_true_mean[3], '--k', label='yes commander')


plt.legend()
#%% 
nx_kwargs = {'node_size':5}
full_data = EoN.discrete_SIR(g, args=(prob_trans,), rho=rho, 
                             return_full_data=True)
ani = full_data.animate(node_size=5, pos=layout_2d(g), width=0.125)

ani.save('demo_animation.mp4', fps=5)
#%%
nx_kwargs = {'node_size':5}
full_data = EoN.discrete_SIR(g, args=(prob_trans,), rho=rho,
                             node_commander=nodeCommander,
                             return_full_data=True)
ani = full_data.animate(node_size=5, pos=layout_2d(g), width=0.125)

ani.save('demo_animation.mp4', fps=5)