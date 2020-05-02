# -*- coding: utf-8 -*-
"""
Author: Justin Deterding

Description:

"""


from Utilities import random_2d_grid_graph, layout_2d
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
from random import normalvariate

fig, axarr = plt.subplots(3,3)

sigma, mu = 1.0, 0.0

N, L = np.meshgrid([100, 500, 1000],
                   [sigma/4, sigma/2, sigma])

for n, l, ax in zip(np.ravel(N), np.ravel(L), np.ravel(axarr)):
    
    G = random_2d_grid_graph(n,l,normalvariate, args=(mu, sigma))
    
    plt.sca(ax)
    
    nx.draw(G, pos=layout_2d(G), node_size=5, width=0.25)
    
    print('Connection Distance: ', l)
    print(nx.info(G))
    
    
