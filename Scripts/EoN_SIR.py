"""
Desctiption:
    A Demo implimentation of

"""


# Imports

import networkx as nx
import EoN
import matplotlib.pyplot as plt

def single_step_model(G, tau, gamma, infecteds, recovereds, tstep):

    data_seg = EoN.fast_SIR(G, tau, gamma, tmax=tstep,
                            initial_infecteds=infecteds,
                            initial_recovereds=recovereds,
                            return_full_data=True)
    return data_seg


def run_model():




    return




# Initilization
G = nx.configuration_model([1, 5, 10]*333)
gamma = 1.
tau = 0.3

t = []
S = []
I = []
R = []



t_seg, SIR = data_seg.summary()
t += list(t_seg)
S += list(SIR['S'])
I += list(SIR['I'])
R += list(SIR['R'])

status = data_seg.get_statuses(time=t_seg[-1])
All_nodes = set(G.nodes)
I_nodes = set([key for key in status if status[key] == 'I'])
S_nodes = set([key for key in status if status[key] == 'S'])
R_nodes = All_nodes.difference(I_nodes).difference(S_nodes)

for i in range(4):



    t_seg, SIR = data_seg.summary()
    t += list(t_seg)
    S += list(SIR['S'])
    I += list(SIR['I'])
    R += list(SIR['R'])

    status = data_seg.get_statuses(time=t_seg[-1])
    I_nodes = set([key for key in status if status[key] == 'I'])
    S_nodes = set([key for key in status if status[key] == 'S'])
    R_nodes = All_nodes.difference(I_nodes).difference(S_nodes)

    print(len(S_nodes), S[-1], sep=', ')
    print(len(I_nodes), I[-1], sep=', ')
    print(len(R_nodes), R[-1], sep=', ')

trim_inx = t.index(-1)
t = t[:trim_inx]
S = S[:trim_inx]
I = I[:trim_inx]
R = R[:trim_inx]

plt.plot(t, S)
plt.plot(t, I)
plt.plot(t, R)
plt.show()
"""""
full_data = EoN.fast_SIR(full_data.G, tau, gamma, tmax=1.0,
                         initial_infecteds=full_data.I(),
                         initial_recovereds=full_data.R(),
                         return_full_data=True)
full_data.display(-1)
plt.show()
"""




