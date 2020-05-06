# -*- coding: utf-8 -*-
"""
Author: Justin Deterding

Description:
    Nodes in an SIR simulation can have 3 states susseptable, infected, and 
    recovered. In addition the edge between two two nodes can also have two 
    states connected or disconnected. From this we can generate a general rule 
    set seen in the figure below.
        Disconnect  Connect
    S      0/1        0/1
    I      0/1        0/1
    R      0/1        0/1
    At each step in the simulation a node looks to it neighboors and uses the 
    rule set to determine if the state of the edge should be changed (1) or do
    nothing (0).
"""
# %% Imports
import EoN
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from random import seed
from random import random as rand
from itertools import product
import Utilities as util
from pandas import DataFrame as df
seed(10)


# %% Function definitions

def singleRun(graph, prob_trans, rho, node_commander):
    results = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho, 
                               node_commander=node_commander)
    return results[1:]


#%% Scanrio Parameters
#g = nx.configuration_model([randint(1, 15) for i in range(999)])
g = util.random_2d_grid_graph(1000, 0.1, rand)
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
    node_commander = util.nodeCommandGennerator(util.nodeCommanderRuleFollower, 
                                                (rule_arr,))
    args = (g.copy(), prob_trans, rho, node_commander)
    results = util.multiRun(singleRun, args)
    results_dict[rule_key] = {'results': results, 'rule': rule_arr}
  
#%% Post process

all_results = {}
for key in results_dict:
    mean_stats = util.getStats(results_dict[key]['results'], 1000)
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

results_df = df(all_results)

results_df = results_df.sort_values(['I max','D min'],ascending=[True,False])
top_group = results_df[(results_df['I max'] < 0.04) & 
                       (results_df['D min'] > 20.0)]


