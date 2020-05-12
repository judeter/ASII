# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:56:00 2020

@author: cathe
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import topdown_buildinggraphs_TE as td
import random

# Had to add simulation.py to my path, pip install wouldn't work properly
import sys
sys.path.insert(1, "C:\\Users\\cathe\\PycharmProjects\\Mathematics-of-Epidemics-on-Networks")
import EoN as sim

#global_coefficient = 0.3
global_population = 1000
#countries = td.build_countries_dictionary(global_population, 0.1, 0.1)
#G = td.get_composed_graph(nx.Graph(), countries, global_coefficient)
#
#init_infected = 0.01
#r_naught = 0.15
#
#
#t, S, I, infected = sim.basic_discrete_SIS(G, r_naught, rho=init_infected,
#                                           tmax=1000,
#                                           graph_commander=countries)

#t, S, I, R, D, infected = sim.discrete_SIR(G, args=(r_naught, ),
#                                              rho=init_infected,
#                                              graph_commander=[countries,
#                                                               [G.copy()]])
def save_runs_SIS(r_naught):
    init_infected = 0.01
    eps = 0.3
    #tolerance=0.99
    count = 0
    for tolerance in np.arange(0.1, 1.0, 0.1):
        countries = td.build_countries_dictionary(global_population,
                                                  tolerance, tolerance)
        G = td.get_composed_graph(nx.Graph(), countries, eps)
        for run in range(10):
            t, S, I, infected = sim.basic_discrete_SIS(G, r_naught, rho=init_infected,
                                                       tmax=1000,
                                                       graph_commander=countries)
            sample = get_infected_sample(infected)
            int_rnaught = int(r_naught*100)
            np.savetxt('Data/TEdata/tolerance_rnaught{}/MX_{}_{}.csv'.format(int_rnaught,
                       count, run), sample, delimiter=',', fmt='%d')
            print("Finished run {} with tolerance {}".format(run, tolerance))
        count += 1


def get_infected_sample(infected):
    indiv_pops = np.asarray(list(infected.values())).T
    global_pop = np.mean(indiv_pops, axis=1, keepdims=True)
    samples = 3
    sample = indiv_pops[:, np.random.choice(indiv_pops.shape[1], samples,
                                            replace=False)]
    return np.concatenate((np.round(global_pop), sample), axis=1)


def plot_timeseries(indiv_pops_hightol, indiv_pops_lowtol):
    def get_stats(indiv_pops):
        mean = np.mean(indiv_pops, axis=1)
        ci = 1.96 * np.std(indiv_pops, axis=1)/mean_hightol
        return mean, ci
    mean_hightol, ci_hightol = get_stats(indiv_pops_hightol)
    mean_lowtol, ci_lowtol = get_stats(indiv_pops_lowtol)

    plt.plot(mean_hightol, color='lightblue')
    plt.fill_between(range(1000), mean_hightol-ci_hightol,
                     mean_hightol + ci_hightol, color='blue')
    plt.plot(mean_lowtol, color='orange')
    plt.fill_between(range(1000), mean_lowtol-ci_lowtol,
                     mean_lowtol + ci_lowtol, color='red')
    plt.legend(['Mean (τ=0.9)', 'Mean (τ=0.1)', '95% CI (τ=0.9)',
                '95% CI (τ=0.1)'])
    plt.ylabel('Individuals infected in a single country')
    plt.xlabel('Time')
    plt.title('10 countries')
    ax = plt.gca()
    ax.set_facecolor((0.94, 0.94, 0.94))


def save_runs():
    init_infected = 0.05
    r_naught = 0.4
    #eps = 0.4
    tolerance=0.99
    count = 0
    for eps in np.arange(0.1, 1.1, 0.1):
        countries = td.build_countries_dictionary(tolerance, tolerance)
        G = td.get_composed_graph(nx.Graph(), countries, eps)
        for run in range(10):
            _, _, _, _, _, infected = sim.discrete_SIR(G, args=(r_naught, ),
                                                       rho=init_infected,
                                                       graph_commander=[countries,
                                                                      [G.copy()]])
            sample = get_infected_sample()
            np.savetxt('Data/TEdata/epsilon_hightol/MX_{}_{}.csv'.format(count,
                       run), sample,
                       delimiter=',')
        count += 1


def make_pos():
    node_pos = {}
    for c in countries:
        c_G = countries[c]["G"]
        for node in c_G.nodes:
            x_range = countries[c]["x_range"]
            y_range = countries[c]["y_range"]
            node_pos[node] = (random.uniform(x_range[0], x_range[1]),
                              random.uniform(y_range[0], y_range[1]))
    return node_pos


def plot_animation(save=False):
    positions = make_pos()
    full_data, checkpoints = sim.discrete_SIR(G, args=(0.3,), rho=0.05,
                                              return_full_data=True,
                                              graph_commander=[countries,
                                                               [G.copy()]])
    ani = full_data.animate(ts_plots=['I', 'SIR'],
                            node_size=250,
                            pos=positions)
#    for graph in checkpoints:
#        plt.figure()
#        nx.draw(graph, pos=positions)
    if save:
        ani.save('SIR_topdown.mp4', fps=5, extra_args=['-vcodec', 'libx264'])


def plot_graph_alone():
    t, S, I, R, D = sim.discrete_SIR(G, args=(r_naught,), rho=init_infected,
                                     graph_commander=[countries, [G.copy()]])
    # Plot
    plt.figure(figsize=(20, 8))
    ax1 = plt.gca()
    plt.rcParams.update({'font.size': 25})
    plt.plot(t, S, color='green', lw=3, label='S')
    plt.plot(t, I, color='red', lw=3, label='I')
    plt.plot(t, R, color='blue', lw=3, label='R')
    plt.legend()
    plt.ylabel('Number of nodes')
    ax2 = plt.twinx(ax1)
    plt.plot(t, D, color='black', lw=3, label='Degree')
    plt.ylabel('Average ')
    plt.title('SIR model with {:.0f}% initially infected and $R_0$ = {}'
              .format(init_infected*100, r_naught))
    plt.grid()
    plt.legend()
    plt.show()
