# -*- coding: utf-8 -*-
"""
Author: Justin Deterding

Description:

"""
# %% Imports
import EoN
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import random
import Utilities as util
from pandas import DataFrame as df

random.seed(10)


# %% Function definitions

def singleRun(graph, prob_trans, rho, node_commander):
    results = EoN.discrete_SIR(graph, args=(prob_trans,), rho=rho, 
                               node_commander=node_commander)
    return results[1:]


#%% Scanrio Parameters
graph_size = 1000
max_connection_dist = 1.0/np.sqrt(graph_size)*2
g = util.random_2d_grid_graph(graph_size, max_connection_dist, random.random)
print(nx.info(g))
plt.figure()
nx.draw(g, pos=util.layout_2d(g), node_size=5)
# low rho and prob_trans leads to high uncertanty
rho = 10/graph_size
prob_trans = 0.2

#%% Baseline

node_commander = util.nodeCommandGennerator(util.quarentineNode, (0,0))
args = (g, prob_trans, rho, node_commander)
base_line_results = util.multiRun(singleRun, args, N=10)
base_line_plot_pair = (base_line_results.mean(axis=0),
                       base_line_results.std(axis=0))
util.plot_SIRD([base_line_plot_pair], graph_size, fontsize=12)
  
#%% strict quarenteen
strict_quarenteen_data = [base_line_plot_pair]
labels = ['base line']
for cheet_rate in [0.0, 0.25, 0.50]:
    node_commander = util.nodeCommandGennerator(util.quarentineNode, 
                                                (cheet_rate, 0.50))
    args = (g, prob_trans, rho, node_commander)
    results = util.multiRun(singleRun, args, N=10)
    strict_quarenteen_data.append((results.mean(axis=0),
                                   results.std(axis=0)))
    labels.append("{:4.2f}".format(cheet_rate))
linestyles = ['-', '--', ':', '-.']
    
util.plot_SIRD(strict_quarenteen_data, 
               linestyles=linestyles, labels=labels)

