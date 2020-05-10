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
import pandas as pd

# Set random seed for reproducable results
random.seed(10)


# %% Function definitions
def singleRun(graph, prob_trans, rho, graph_commander):
    """
    single run generates result from single run of the discreet SIR model. Runs
    are inherently probablistic so it is nessisary to do mutiple runs.

    """
    results = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho,
                               graph_commander=graph_commander)
    # Dont return time, statistics on time variable are usless
    return results[1:]


#%% Graph Commander Set up
country_names = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
country_cent = list(it.product((-1.0, 0.0, 1.0), (-1.0, 0.0, 1.0)))
graph_size = 111
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
print(nx.info(G))
nx.draw(G, pos=util.layout_2d(G), node_size=3)

graph_commander = [countries, [G.copy()]]

# want less than 9 initialy infected individuals
rho = 3/(graph_size*9)
prob_trans = 0.8

#%% Run without quarenteen scanario 

node_commander = util.nodeCommandGennerator(util.quarentineNode,
                                            args=(0.0, 0.0))
key = 1
results_dict = {}

rules = list(it.product(*2*[(0.01, 0.03, 0.05, 0.07, 1.0)]))

for num, tol_set in enumerate(rules):
    print('Evaluating:', num+1, '/', len(rules))
    for c in graph_commander[0]:
        graph_commander[0][c]['tolerance_in'] = tol_set[0]
        graph_commander[0][c]['tolerance_out'] = tol_set[1]

    args = (G.copy(), prob_trans, rho, graph_commander)
    results = util.multiRun(singleRun, args, 10)
    
    results_dict[key] = {'results': results, 'rule': tol_set}

    key += 1

#%% Post process

all_results = {}
all_results['tol in'] = []
all_results['tol out'] = []
for key in results_dict:
    mean_stats = util.getStats(results_dict[key]['results'], graph_size*9)
    mean_stats['key'] = key
    for stat in mean_stats:
        if stat not in all_results:
            all_results[stat] = []
        all_results[stat].append(mean_stats[stat])
    all_results['tol in'].append(results_dict[key]['rule'][0])
    all_results['tol out'].append(results_dict[key]['rule'][1])
for stat in all_results:
    all_results[stat] = np.array(all_results[stat])
    
#%%
results_df = pd.DataFrame(all_results)
results_df.sort_values('I max', ascending=True, inplace=True)

plt.figure()
plt.errorbar(results_df['tol in'], results_df['I max'], 
             xerr=None, yerr=results_df['I std'], 
             fmt='o', label = 'Internal Tolerance')

plt.errorbar(results_df['tol out'], results_df['I max'], 
             xerr=None, yerr=results_df['I std'], 
             fmt='+', label = 'External Tolerance')
plt.legend()
plt.xlabel('Tolerance level (percent infected)')
plt.ylabel('Peak percentage of infected population')

#%%
base_rule_key = results_df['key'].iloc[-1]
midd_rule_key = results_df['key'].iloc[len(results_df)//2]
best_rule_key = results_df['key'].iloc[0]
base_results = util.combineResults(results_dict[base_rule_key]['results'])
best_results = util.combineResults(results_dict[best_rule_key]['results'])   
midd_results = util.combineResults(results_dict[midd_rule_key]['results'])   
                                            
plot_data = [(base_results.mean(axis=0), base_results.mean(axis=0)),
             (midd_results.mean(axis=0), midd_results.mean(axis=0)),
             (best_results.mean(axis=0), best_results.mean(axis=0))]
util.plot_SIRD(plot_data, linestyles=["-", "--", "-."],
               labels=[str(results_dict[base_rule_key]['rule']),
                       str(results_dict[midd_rule_key]['rule']),
                       str(results_dict[best_rule_key]['rule'])])
