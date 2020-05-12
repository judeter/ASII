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
import matplotlib
import random
import itertools as it
import Utilities as util
import pandas as pd

random.seed(10)


# %% Function definitions

def singleRun(graph, prob_trans, rho, node_commander):
    results = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho, 
                               node_commander=node_commander)
    return results[1:]


#%% Scanrio Parameters
graph_size = 999
max_connection_dist = 1.0/np.sqrt(graph_size)*2
g = util.random_2d_grid_graph(graph_size, max_connection_dist, random.random)
print(nx.info(g))
plt.figure()
nx.draw(g, pos=util.layout_2d(g), node_size=5)
# low rho and prob_trans leads to high uncertanty
rho = 0.03
prob_trans = 0.8

#%%
results_dict = {}

dist = (0.0, 0.25, 0.5, 0.75, 1.0)
#                  D      C
rules_options = [dist, dist,  # S
                 (1,), (0,),  # I
                 (1,), (0,)]  # R If disconected then reconnect

rule_label = 1
tot_num_of_runs = len(list(it.product(*rules_options)))

for rule_list in it.product(*rules_options):
    # convert flattened rule table to a decimal number
    #rule_key = int("".join(str(x) for x in rule_list), 2)
    rule_key = rule_label
    rule_label += 1
    # Reshape flat rule into 2d rule table
    rule_arr = np.reshape(np.array(rule_list), newshape=(3, 2))
    print('Evaluating Rule: ', rule_key, '/', tot_num_of_runs)
    node_commander = util.nodeCommandGennerator(util.nodeCommanderRuleFollower, 
                                                (rule_arr,))
    args = (g, prob_trans, rho, node_commander)
    results = util.multiRun(singleRun, args, N=20)
    results_dict[rule_key] = {'results': results, 'rule': rule_arr}
  
#%% Post process

all_results = {}
for key in results_dict:
    mean_stats = util.getStats(results_dict[key]['results'], graph_size)
    mean_stats['key'] = key
    for stat in mean_stats:
        if stat not in all_results:
            all_results[stat] = []
        all_results[stat].append(mean_stats[stat])
for stat in all_results:
    all_results[stat] = np.array(all_results[stat])
    
#%%
results_df = pd.DataFrame(all_results)
results_df.sort_values(['I max', 'D min'], ascending=[True,False], inplace=True)

top_num = 5
bot_num = 5
plt.figure()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}

matplotlib.rc('font', **font)

plt.errorbar(results_df['I max'][:top_num], results_df['D min'][:top_num], 
             xerr=results_df['I std'][:top_num], 
             yerr=results_df['D std'][:top_num], 
             fmt='g*', label = 'Optimal Strategies')

plt.errorbar(results_df['I max'][top_num:-bot_num], 
             results_df['D min'][top_num:-bot_num], 
             xerr=results_df['I std'][top_num:-bot_num], 
             yerr=results_df['D std'][top_num:-bot_num], 
             fmt='ko', label = 'Intermediate Strategies')

plt.errorbar(results_df['I max'][-bot_num:], results_df['D min'][-bot_num:], 
             xerr=results_df['I std'][-bot_num:], 
             yerr=results_df['D std'][-bot_num:], 
             fmt='r+', label='Sub-Optimal Strategies')

plt.xlabel('Peak Percentage of Infected Population')
plt.ylabel('Minimum Average Node Degree')
plt.legend()

#%%
with open('nodeStragyRangins.txt', mode='w') as f:
    f.writelines('key : rank : rule \n')
    top_rule_count = np.zeros((3, 2))
    print('------- Top ranked rules -------')
    print('key : rank : rule')
    for rank, key in enumerate(results_df['key'][:top_num]):
        print(key, ' : ', rank, ' : ', results_dict[key]['rule'][0][:])
        f.write("{:4d}:{:6d}:{} \n".format(key,rank,
                                        results_dict[key]['rule'][0][:]))
        top_rule_count += results_dict[key]['rule']
    print('Sum:')
    print(top_rule_count[0][:])


    print('------- Mid ranked rules -------')
    top_rule_count = np.zeros((3, 2))
    print('key : rank : rule')
    for rank, key in enumerate(results_df['key'][top_num:-bot_num]):
        print(key, ' : ',bot_num+rank,' : ',results_dict[key]['rule'][0][:])
        f.write("{:4d}:{:6d}:{} \n".format(key,rank,
                                 results_dict[key]['rule'][0][:]))
        top_rule_count += results_dict[key]['rule']        
    print('Sum:')
    print(top_rule_count[0][:])


    print('------- Bottom ranked rules -------')
    print('key : rank : rule')
    bot_rule_count = np.zeros((3, 2))
    for rank, key in enumerate(results_df['key'][-bot_num:]):
        print(key, ' : ',len(results_df)-rank,' : ',results_dict[key]['rule'][0][:])
        f.write("{:4d}:{:6d}:{} \n".format(key,rank,
                                        results_dict[key]['rule'][0][:]))
        bot_rule_count += results_dict[key]['rule']
    print(bot_rule_count[0][:])

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
               labels=[str(results_dict[base_rule_key]['rule'][0][:]),
                       str(results_dict[midd_rule_key]['rule'][0][:]),
                       str(results_dict[best_rule_key]['rule'][0][:])])




