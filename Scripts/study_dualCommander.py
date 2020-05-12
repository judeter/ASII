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


<<<<<<< HEAD
# %% Function definitions
def singleRun(graph, prob_trans, rho, node_commander, graph_commander):
=======
def singleRun(graph, prob_trans, rho, node_commander, graph_commander, seed):
>>>>>>> 9df3fc7850dc67ed4d94984f4a8fbff216ba9932
    """
    single run generates result from single run of the discreet SIR model. Runs
    are inherently probablistic so it is nessisary to do mutiple runs.

    """
    results = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho,
                               node_commander=node_commander, 
                               nodes_activated=False,
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

    countries[country_name] = {"G": g,
                               "infected": None,
                               "closed_borders": None}
    
G = nx.compose_all([countries[key]['G'] for key in countries])
# Adding intra connections to sub graphs
sub_graphs = [countries[key]['G'] for key in countries]
for pair in it.combinations(sub_graphs, 2):
    util.add_euclidian_edges(pair, max_connection_dist, G=G)
plt.figure()
print(nx.info(G))
nx.draw(G, pos=util.layout_2d(G), node_size=5, linewidths=0.25)
plt.vlines(0,-1,2); plt.vlines(1,-1,2)
plt.hlines(0,-1,2); plt.hlines(0,-1,2)
graph_commander = [countries]

<<<<<<< HEAD
# want less than 9 initialy infected individuals
rho = 1/(graph_size*9)
prob_trans = 0.8
=======
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

results = util.multiRun(singleRun, args)

#%% Calculate Mean and standard deviation of results

base_line_results = util.multiRun(singleRun, args)
base_line_plot_pair = (base_line_results.mean(axis=0),
                       base_line_results.std(axis=0))
util.plot_SIRD([base_line_plot_pair], graph_size, fontsize=12)
>>>>>>> 9df3fc7850dc67ed4d94984f4a8fbff216ba9932

#%% Run without quarenteen scanario 

key = 1
results_dict = {}
search_grid = [(0.01,0.03,0.05, 0.08)]+2*[(0.0, 0.25, 0.5, 0.75, 0.95)]
rules = list(it.product(*search_grid))

for num, tol_set in enumerate(rules):
    print('Evaluating:', num+1, '/', len(rules))
    node_commander = util.nodeCommandGennerator(util.quarentineNode,
                                                args=(tol_set[1], tol_set[2]))
    for c in graph_commander[0]:
        graph_commander[0][c]['tolerance_in'] = tol_set[0]
        graph_commander[0][c]['tolerance_out'] = 1.0
    
    args = (G.copy(), prob_trans, rho, node_commander, graph_commander)
    results = util.multiRun(singleRun, args, 10)
    
    results_dict[key] = {'results': results, 'rule': tol_set}

    key += 1

#%% Post process

all_results = {}
all_results['tol'] = []
all_results['cheat rate'] = []
all_results['quarenteen level'] = []
for key in results_dict:
    mean_stats = util.getStats(results_dict[key]['results'], graph_size*9)
    mean_stats['key'] = key
    for stat in mean_stats:
        if stat not in all_results:
            all_results[stat] = []
        all_results[stat].append(mean_stats[stat])
    all_results['tol'].append(results_dict[key]['rule'][0])
    all_results['cheat rate'].append(results_dict[key]['rule'][1])
    all_results['quarenteen level'].append(results_dict[key]['rule'][2])
for stat in all_results:
    all_results[stat] = np.array(all_results[stat])
    
#%%
results_df = pd.DataFrame(all_results)
center = (0.0, 11.4835)
results_df['I norm'] = ((results_df['I max']-results_df['I max'].min()) /                     
                        (results_df['I max'].max()-results_df['I max'].min()))
results_df['D norm'] = ((results_df['D min']-results_df['D min'].min()) /                     
                        (results_df['D min'].max()-results_df['D min'].min()))
                                              
results_df['radi'] = np.sqrt((1-results_df['I norm']**2)*2 + 
                             (1-results_df['D norm'])**2 )

results_df.sort_values(['I std','radi'], ascending=[True,True], inplace=True)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    f = open('dualCommanderResults.txt', mode='w')
    f.write(str(results_df))
    f.close()
    
#%%
top_tot = 50
top_rank = 10
plt.figure()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}
matplotlib.rc('font', **font)
plt.plot(results_df['I max'][:top_rank], 
         results_df['D min'][:top_rank],
         '*g', label = 'Top 10 Optimal strategies')
plt.plot(results_df['I max'][top_rank:top_tot], 
         results_df['D min'][top_rank:top_tot], 
         'ok', label = 'Sub-Optimal strategies')
plt.xlabel('Peak Percentage of Infected Population')
plt.ylabel('Minimum Average Node Degree')
plt.legend()


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
