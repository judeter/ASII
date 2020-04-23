# -*- coding: utf-8 -*-
"""
Author: Justin Deterding

Description:

"""

# %% Imports
import EoN
import networkx as nx
from matplotlib import pyplot as plt


# %% def Single runs
# For low infection rates ~ 0.4 we see curve flattening
# For larger graphs this seems to disapear
def single_run_cmder_false():
    G = nx.grid_2d_graph(100, 100)
    no_node_cmd = EoN.discrete_SIR(G, args=(0.4,), rho=0.05)
    return no_node_cmd[1:]

def single_run_cmder_true():
    G = nx.grid_2d_graph(100, 100)
    print(nx.info(G))
    yes_node_cmd = EoN.discrete_SIR(G, args=(0.4,), rho=0.05,
                                    node_commander=node_commander)
    print(nx.info(G))
    return yes_node_cmd[1:]


# %%
def combine_results(results):
    import numpy as np
    
    max_len_run = max([len(run[0]) for run in results])
    
    combined_arr = np.array([np.pad(run, ((0, 0), 
                                         (0, max_len_run-len(run[0]))), 
                                    mode='edge') 
                             for run in results])
    
    return combined_arr

# %%
def multi_run(single_run, N=10):
    results = [single_run() for i in range(N)]
    return combine_results(results)


#%%
def node_commander(neighbors, connected_neighbors, 
                   susceptible_neighbors, infected_neighbors):
    from random import sample
    if len(infected_neighbors) > 0:    
        return [], sample(connected_neighbors, len(connected_neighbors)//2)
    else:
        return [], []

#%%
if __name__ == "__main__":

    
    cmber_true_results = multi_run(single_run_cmder_true)
    
    cmber_false_results = multi_run(single_run_cmder_false)
    
#%%
    cmber_false_mean = cmber_false_results.mean(axis=0)
    cmber_true_mean = cmber_true_results.mean(axis=0)    
#%% Plotting    
    fig, axarr = plt.subplots(nrows=3, ncols=1, sharex=True)
    
    axarr[0].set_title('Susceptible')
    axarr[0].plot(cmber_false_mean[0],'-g', label='no commander')
    axarr[0].plot(cmber_true_mean[0],'--g', label='yes commander')
    
    axarr[1].set_title('Infected')
    axarr[1].plot(cmber_false_mean[1],'-r', label='no commander')
    axarr[1].plot(cmber_true_mean[1],'--r', label='yes commander')
    
    axarr[2].set_title('Recovered')
    axarr[2].plot(cmber_false_mean[2],'-k', label='no commander')
    axarr[2].plot(cmber_true_mean[2],'--k', label='yes commander')
    
    plt.legend()
