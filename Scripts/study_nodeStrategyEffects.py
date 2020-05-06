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
from itertools import product
from Utilities import random_2d_grid_graph, layout_2d, multiRun, plot_SIRD

seed(10)


# %% Function definitions

def singleRun(graph, prob_trans, rho, node_commander):
    results = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho, 
                               node_commander=node_commander)
    return results[1:]


#%%
def nodeCommanderRuleFollower(neighbors, connected_neighbors, 
                              susceptible_neighbors, infected_neighbors, 
                              rule_set):
    """
    Rule set form
      | D  | C
    -----------
    S|
    I|
    R|

    """
    disconnect_nodes = []
    connect_nodes = []
    for node in neighbors:
        # determine collumn index based on edge state
        if node in connected_neighbors:
            edge_state_idx = 1
        else:
            edge_state_idx = 0
        #determine row index based on node state
        if node in susceptible_neighbors: 
            node_state_idx = 0    
        elif node in infected_neighbors:
            node_state_idx = 1
        else:
            node_state_idx = 2
        
        # if rule is true then switch state of edge
        if rule_set[node_state_idx][edge_state_idx]:
            if edge_state_idx == 1:
                disconnect_nodes.append(node)
            else:
                connect_nodes.append(node)
        else:
            pass #do nothing
    return connect_nodes, disconnect_nodes

              
#%%            
def nodeCommandGennerator(nodeCommander, args):
    """This is a hack, args should be an argument in the EoN function."""
    nc = lambda n, c_n, s_n, i_n: nodeCommander(n, c_n, s_n, i_n, *args)
    return nc


#%%
def test_ruleCommander():
    """ Series of simple test to check functionality"""
    neighbors = {1, 2, 3, 4, 5, 6}
    connected_neighbors = {1, 2, 3}
    susceptible_neighbors = {2, 3}
    infected_neighbors = {1}
    # disconnect all no matter what
    rule_set_1 = [[0, 1],
                  [0, 1],
                  [0, 1]]
    cn, dn = nodeCommanderRuleFollower(neighbors, connected_neighbors,
                                       susceptible_neighbors,
                                       infected_neighbors,
                                       rule_set_1)    
    assert list(connected_neighbors) == dn 
    assert [] == cn
    # flip current connections
    rule_set_2 = [[1, 1],
                  [1, 1],
                  [1, 1]]    
    cn, dn = nodeCommanderRuleFollower(neighbors, connected_neighbors,
                                       susceptible_neighbors,
                                       infected_neighbors,
                                       rule_set_2)
    assert list(connected_neighbors) == dn
    assert list(neighbors.difference(connected_neighbors)) == cn
#%%    
def getStats(results, graph_size=1):
    mean = results.mean(axis=0)
    std = results.std(axis=0)
    
    mean_stats = {}
    
    mean_stats['I max'] = np.max(mean[1])/graph_size 
    mean_stats['I std'] = std[1][np.argmax(mean[1])]/graph_size 
    
    mean_stats['D min'] = np.min(mean[3])
    mean_stats['D std'] = std[3][np.argmin(mean[1])]
    
    mean_stats['S end'] = mean[0][-1]/graph_size
    mean_stats['S std'] = std[0][-1]/graph_size
    
    return mean_stats
                  
     
#%% Scanrio Parameters

#g = nx.configuration_model([randint(1, 15) for i in range(999)])
g = random_2d_grid_graph(1000,0.1,rand)
print(nx.info(g))
rho = 0.001
prob_trans = 0.2

rule_set_generator = product((0, 1), (0, 1),
                             (0, 1), (0, 1),
                             (0, 1), (0, 1),)
results_dict = {}
for rule_list in rule_set_generator:
    # convert flattened rule table to a decimal number
    rule_key = int("".join(str(x) for x in rule_list), 2)
    # Reshape flat rule into 2d rule table
    rule_arr = np.reshape(np.array(rule_list), newshape=(3, 2))
    print('Evaluating Rule #:', rule_key)
    node_commander = nodeCommandGennerator(nodeCommanderRuleFollower, 
                                           (rule_arr,))
    args = (g.copy(), prob_trans, rho, node_commander)
    results = multiRun(singleRun, args)
    results_dict[rule_key]={'results': results, 'rule': rule_arr}
  
#%% Post process

all_results = {}
for key in results_dict:
    mean_stats = getStats(results_dict[key]['results'],1000)
    mean_stats['key'] = key
    for stat in mean_stats:
        if stat not in all_results:
            all_results[stat] = []
        all_results[stat].append(mean_stats[stat])
for stat in all_results:
    all_results[stat] = np.array(all_results[stat])
    

plt.plot(all_results['I max'], all_results['D min'], 'o')
plt.xlabel('Peak percentage of infected population')
plt.ylabel('Minimum average node degree')

from pandas import DataFrame as df

results_df = df(all_results)

results_df = results_df.sort_values(['I max','D min'],ascending=[True,False])
top_group = results_df[(results_df['I max'] < 0.04) & 
                       (results_df['D min'] > 20.0)]


