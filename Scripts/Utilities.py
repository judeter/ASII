# -*- coding: utf-8 -*-
"""
Author: Justin Deterding

Description:

"""
#%%
def random_2d_grid_graph(num_nodes=100, grid_size=(-50,50), weighted=False, 
                         max_connection_dist=10):
    # IMPORTS
    from random import randint
    import numpy as np
    import networkx as nx
    
    # Assertions and warnings
    assert abs(grid_size[0])*abs(grid_size[1]) > num_nodes

    # Assign node cordinates random uniform
    node_cordinates = []    
    while len(node_cordinates) < num_nodes:
        cord = (randint(*grid_size), randint(*grid_size)) 
        if cord not in node_cordinates:
            node_cordinates.append(cord)
    
    edges = []
    weights = []
    for inx, from_cord in enumerate(node_cordinates):
        for to_cord in node_cordinates[inx+1:]:
            
            dist = np.sqrt((from_cord[0]-to_cord[0])**2+
                           (from_cord[1]-to_cord[1])**2)
            
            if dist <= max_connection_dist:
                edges.append((from_cord, to_cord))
                if weighted:
                    weights.append(dist)
    
    g = nx.Graph()
    for node in node_cordinates:
        g.add_node(node)
        
    if weighted:
        for edge, weight in zip(edges, weights): 
            g.add_edge(*edge, weight=weight)
    else:
        for edge in edges: 
            g.add_edge(*edge)
        
    return g

# %%
def layout_2d(G):
    return {node: node for node in G.nodes}


