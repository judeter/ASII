# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 17:28:45 2020

@author: cathe
"""
import networkx as nx
import math
import random

def build_countries_dictionary(global_population, tolerance_in=0.2,
                               tolerance_out=0.2):
    def build_country_dictionary():
        number_of_countries = 10
        def single_country(percentage, tolerance_in, tolerance_out,
                           x_range=(1, 1), y_range=(1, 1),
                           graph=None, infected=None, closed_borders=None):
            return {"percentage": percentage,
                    "tolerance_in": tolerance_in,
                    "tolerance_out": tolerance_out,
                    "G": graph,
                    "infected": infected,
                    "x_range": x_range,
                    "y_range": y_range,
                    "closed_borders": closed_borders}
        countries = ['C{}'.format(i) for i in range(number_of_countries)]
        countries_dict = {}
        for country in countries:
                countries_dict[country] = single_country(1/number_of_countries,
                              tolerance_in, tolerance_out)
        return countries_dict
    countries = build_country_dictionary()
    node_counter = 0
    for country in countries:
        G = nx.Graph()
        percentage = countries[country]["percentage"]
        number_of_nodes = math.floor(global_population*percentage)
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


def get_composed_graph(G, countries, global_coupling):
    for country in countries:
        G = nx.compose(G, countries[country]["G"])
    # Add random edges between countries
    for edges in range(int(len(G.nodes)*global_coupling)):
        places = random.sample(list(countries.keys()), 2)
        u = random.choice(list((countries[places[0]]["G"]).nodes))
        v = random.choice(list((countries[places[1]]["G"]).nodes))
        G.add_edge(u, v)
    return G


#countries = build_countries_dictionary(1000)
#G = get_composed_graph(nx.Graph(), countries, 0.3)
