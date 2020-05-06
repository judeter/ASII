# -*- coding: utf-8 -*-
"""
Author: Justin Deterding

Description:

"""
#%%
def add_euclidian_edges(g, max_connection_dist, G=None):
    from itertools import combinations, product
    import numpy as np
        
    edges = []
    if G:
        assert len(g)==2
        iterable = product(*g)
    else:
        iterable = combinations(g, 2)
    
    for n1, n2 in iterable:
        if G:
            x1, y1 = g[0].nodes(data='pos')[n1]
        else:
            x1, y1 = g.nodes(data='pos')[n1] 
        if G:
            x2, y2 = g[1].nodes(data='pos')[n2]
        else:
            x2, y2 = g.nodes(data='pos')[n2] 
        
        dist = np.sqrt((x1-x2)**2+(y1-y2)**2)

        if dist <= max_connection_dist:
            edges.append((n1, n2))
    
    for edge in edges: 
        if G:
            G.add_edge(*edge)
        else:
            g.add_edge(*edge)
    

#%%
def random_2d_grid_graph(num_nodes, max_connection_dist, position_generator, 
                         args=(), xy_cent=(0, 0)):
    # IMPORTS
    import numpy as np
    import networkx as nx
    
    nodes = list(range(num_nodes))
    # Assign node cordinates random uniform
    node_cordinates = []    
    while len(node_cordinates) < num_nodes:
        cord = (position_generator(*args)+xy_cent[0], 
                position_generator(*args)+xy_cent[1]) 
        if cord not in node_cordinates:
            node_cordinates.append(cord)

    g = nx.Graph()
    for node, pos in zip(nodes, node_cordinates):
        g.add_node(node, pos=pos)   
        
    add_euclidian_edges(g,max_connection_dist)
        
    return g

# %%
def layout_2d(G, position_data_key='pos'):
    return {node: pos for node, pos in G.nodes(data=position_data_key)}

#%%
def multiRun(single_run_function, function_args, N=10):
    results = [single_run_function(*function_args) for i in range(N)]
    return combineResults(results)


def combineResults(results):
    """
    Take a list of numpy arrays. Each numpy array should have an equal number 
    of collumns, with variying numbers of rows. The results are combined into
    a single numpy array with dimention {num_runs,num_output,max_output_len}.
    
    Parameters
    ----------
    results : list of list or arrays
        The results from various runs of multiRun are stored in a list, called 
        results.

    Returns
    -------
    combined_arr : numpy array
        single numpy array with dimention {num_runs,num_output,max_output_len}.

    """
    import numpy as np
    
    max_len_run = max([len(run[0]) for run in results])
    
    combined_arr = np.array([np.pad(run, ((0, 0), 
                                         (0, max_len_run-len(run[0]))), 
                                    mode='edge') 
                             for run in results])
    
    return combined_arr

#%% Infected checker


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
    import random
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
        if rule_set[node_state_idx][edge_state_idx] > random.random():
            if edge_state_idx == 1:
                disconnect_nodes.append(node)
            else:
                connect_nodes.append(node)
        else:
            pass  # do nothing
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
    import numpy as np
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


#%%
def plot_SIRD(mean_and_std_list, plot_confidence_interval=True, fontsize=24,
              linestyle_list = ['solid']):
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, axarr = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(4,8))

    for mean_and_std, linestyle in zip(mean_and_std_list, linestyle_list):
        mean, std = mean_and_std
        axarr[0].set_title('Mean Susceptible', fontsize=fontsize)
        axarr[0].plot(mean[0], color='green', linestyle=linestyle)
        
        axarr[1].set_title('Mean Infected', fontsize=fontsize)
        axarr[1].plot(mean[1], color='red', linestyle=linestyle)
        upper_95pct = mean[1]+std[1] 
        lower_95pct = mean[1]-std[1]
        x = np.arange(len(std[1]))
        axarr[1].fill_between(x, upper_95pct, lower_95pct, color='red', 
                              alpha=0.1)
        
        axarr[2].set_title('Mean Recovered', fontsize=fontsize)
        axarr[2].plot(mean[2], color='gray', linestyle=linestyle)
        
        axarr[3].set_title('Mean Average Node Degree', fontsize=fontsize)
        axarr[3].plot(mean[3], color='black', linestyle=linestyle)
    
    plt.tight_layout()
    return fig

    
#%%

def single_country(percentage, tolerance_in, tolerance_out, 
                   min_x, max_x, min_y, max_y,
                   graph=None, infected=None, closed_borders=None):
    return {"percentage": percentage,
            "tolerance_in": tolerance_in,
            "tolerance_out": tolerance_out,
            "G": graph,
            "infected": infected,
            "x_range": [min_x, max_x],
            "y_range": [min_y, max_y],
            "closed_borders": closed_borders}


def build_country_dictionary():
    return {"USA": single_country(0.18, 0.2, 0.4, 0, 4, 6, 10),
            "China": single_country(0.75, 0.4, 0.5, 6, 10, 0, 4),
            "Italy": single_country(0.033, 0.2, 0.2, 0, 4, 0, 4),
            "UK": single_country(0.037, 0.2, 0.3, 6, 10, 6, 10)}


def build_countries_dictionary(global_population, countries):
    """
    
    Parameters
    ----------
    global_population : int
        Total number of nodes in the simulation.
    countries : dict of country dictionaries
        A dictionary of countries each with their own corisponding dictionary
        of parameters.

    Returns
    -------
    countries : TYPE
        DESCRIPTION.

    """

    import random
    import math
    import networkx as nx
    
    node_counter = 0
    for country in countries:
        G = nx.Graph()
        percentage = countries[country]["percentage"]
        number_of_nodes = math.floor(global_population*percentage)
        # all nodes must have distinctive id for graph mergin process
        node_ids = list(range(node_counter, node_counter + number_of_nodes))
        G.add_nodes_from(node_ids)
        avg_edges_per_person = 4  # TO-DO come up with a better average
        for edges in range(number_of_nodes*avg_edges_per_person):
            u, v = random.sample(node_ids, 2)
            G.add_edge(u, v)
        # update dictionary
        countries[country]["G"] = G

        # increment node_counter
        node_counter += number_of_nodes
    return countries


def get_composed_graph(countries):
    import networkx as nx
    import random
    G = nx.Graph()
    for country in countries:
        # Add all of the graphs for each contry into one graph
        G = nx.compose(G, countries[country]["G"])
    # Add random edges between countries
    avg_edges_global = 3  # TO-DO come up with a better estimate
    for edges in range(len(G.nodes)*avg_edges_global):
        places = random.sample(list(countries.keys()), 2)
        u = random.choice(list((countries[places[0]]["G"]).nodes))
        v = random.choice(list((countries[places[1]]["G"]).nodes))
        G.add_edge(u, v)
    return G
