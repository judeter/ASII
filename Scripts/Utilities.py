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
    
    nodes = list(range(num_nodes))
    # Assign node cordinates random uniform
    node_cordinates = []    
    while len(node_cordinates) < num_nodes:
        cord = (randint(*grid_size), randint(*grid_size)) 
        if cord not in node_cordinates:
            node_cordinates.append(cord)
    
    edges = []
    if weighted:
        weights = []
    for from_node, from_cord in enumerate(node_cordinates):
        for inx, to_cord in enumerate(node_cordinates[from_node+1:]):
            to_node = from_node+inx+1
            
            dist = np.sqrt((from_cord[0]-to_cord[0])**2+
                           (from_cord[1]-to_cord[1])**2)
            
            if dist <= max_connection_dist:
                edges.append((from_node, to_node))
                if weighted:
                    weights.append(dist)
    
    g = nx.Graph()
    for node, pos in zip(nodes, node_cordinates):
        g.add_node(node, pos=pos)
        
    if weighted:
        for edge, weight, pos in zip(edges, weights): 
            g.add_edge(*edge, weight=weight)
    else:
        for edge in edges: 
            g.add_edge(*edge)
        
    return g

# %%
def layout_2d(G, position_data_key='pos'):
    return {node: pos for node, pos in G.nodes(data=position_data_key)}


