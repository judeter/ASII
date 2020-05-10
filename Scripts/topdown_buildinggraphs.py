# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 17:28:45 2020

@author: cathe
"""
import networkx as nx
import math
import random


def build_countries_dictionary(global_population):
    def build_country_dictionary():
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
        return {"USA": single_country(0.18, 0.4, 0.2, 0, 4, 6, 10), # .5 .4
                "China": single_country(0.75, 0.8, 0.3, 6, 10, 0, 4), # .5 .5
                "Italy": single_country(0.10, 0.4, 0.3, 0, 4, 0, 4), # .5 .2
                "UK": single_country(0.05, 0.5, 0.2, 6, 10, 6, 10)} #.5 .3
    countries = build_country_dictionary()
    node_counter = 0
    for country in countries:
        G = nx.Graph()
        percentage = countries[country]["percentage"]
        number_of_nodes = math.floor(global_population*percentage)
        node_ids = list(range(node_counter, node_counter + number_of_nodes))
        G.add_nodes_from(node_ids)
        avg_edges_per_person = 3  # TO-DO come up with a better average
        for edges in range(number_of_nodes*avg_edges_per_person):
            u, v = random.sample(node_ids, 2)
            G.add_edge(u, v)
        # update dictionary
        countries[country]["G"] = G

        # increment node_counter
        node_counter += number_of_nodes
    return countries


def get_composed_graph(G, countries):
    for country in countries:
        G = nx.compose(G, countries[country]["G"])
    # Add random edges between countries
    connections = 0.5  # TO-DO come up with a better estimate
    for edges in range(int(len(G.nodes)*connections)):
        places = random.sample(list(countries.keys()), 2)
        u = random.choice(list((countries[places[0]]["G"]).nodes))
        v = random.choice(list((countries[places[1]]["G"]).nodes))
        G.add_edge(u, v)
    return G
