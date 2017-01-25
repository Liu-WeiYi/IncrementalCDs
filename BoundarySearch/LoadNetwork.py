#!/usr/bin/env python3.5

import os
import glob
from math import log
import networkx as nx
from functools import *
from scipy.special import comb

# class Inc(object):
#     def __init__(self, file_dir):
#         self.file_dir = file_dir
#         self.route = []
#         self.accum = 0

def PairFile(file_dir):
    '''Pair the files from day to day'''
    files = glob.glob(os.path.join(file_dir, '200*'))
    paired_list = list(zip(*[files[_:] for _ in range(2)]))
    return(paired_list)

def LoadNetwork(file):
    '''Construct the network'''
    file_name = file.split('/')[-1]
    network = open(file, encoding = 'utf-8').readlines()
    network = [list(map(int, _.split())) for _ in network]
    l_edges = [tuple(_) for _ in network]
    l_nodes = list(set(sum(network, [])))
    G = nx.Graph(day = file_name)
    G.add_nodes_from(l_nodes)
    G.add_edges_from(l_edges)
    return(G)

def LoadCom(com_file):
    '''Load the communities result'''
    com_content = open(com_file, encoding = 'utf-8').readlines()
    com_content = [list(map(int, _.split())) for _ in com_content]
    com_nums = range(1, len(com_content)+1)
    com_map = {i: com_num for com_num, com in zip(com_nums, com_content) for i in com}
    return(com_map)

def FindChanges(file1, file2):
    '''Find all the changes btn two networks'''
    G1 = LoadNetwork(file1)
    G2 = LoadNetwork(file2)
    G1_node = set(G1.nodes())
    G2_node = set(G2.nodes())
    G1_edge = set(G1.edges())
    G2_edge = set(G2.edges())
    add_nodes = list(G2_node - G1_node)
    del_nodes = list(G1_node - G2_node)
    c_nodes = add_nodes + del_nodes
    add_edges = list(G2_edge - G1_edge)
    del_edges = list(G1_edge - G2_edge)
    all_changes = {}
    all_changes.update({_: G2.neighbors(_) for _ in add_nodes})
    del_ndoes_influence = {_: G1.neighbors(_) for _ in del_nodes}
    all_changes.update({i: [k for k in j if k in G2_node] for i, j in del_ndoes_influence.items()})
    if add_edges:
        add_nodes_links = [(_, __) for _ in add_nodes for __ in G2.neighbors(_)]
        add_edges = [_ for _ in add_edges if _ not in add_nodes_links and tuple(reversed(_)) not in add_nodes_links]
        try:
            add_edges_n = [_[__] for _ in add_edges for __ in range(2)]
            add_edges_n_nei = {_: G2.neighbors(_) for _ in add_edges_n}
            all_changes.update({i: [k for k in j if k not in add_nodes] for i, j in add_edges_n_nei.items()})
        except: pass
    if del_edges:
        del_nodes_links = [(_, __) for _ in del_nodes for __ in G1.neighbors(_)]
        del_edges = [_ for _ in del_edges if _ not in del_nodes_links and tuple(reversed(_)) not in del_nodes_links]
        try:
            del_edges_n = [_[__] for _ in del_edges for __ in range(2)]
            all_changes.update({_: G2.neighbors(_) for _ in del_edges_n})
        except: pass
    return(all_changes, c_nodes)

def FindSameCom(Com_result, changed_ele):
    '''check whether the changes'''
    # input
    # output {1: [2, 3], 2: [3, 4]}
    com_map = LoadCom(Com_result)
    all_changes, c_nodes = FindChanges(file1, file2)
    layer = {i: [k for k in j if com_map[i] == com_map[k]] 
                for i, j in all_changes.items() if i not in c_nodes}
    return(layer)

def CalculateEntropy(node_a, node_b):
    '''Calculate the entropy between two nodes'''
    # input (4, 1)
    degree_a = G2.neighbors(node_a)
    degree_b = G2.neighbors(node_b)
    denom = comb(G2_edge, degree_a)
    num = comb(G2_edge - degree_a, degree_b)
    p_ab = 1 - num/denom
    influence = -log(p_ab)

def CalculateEntropyPath(pair_input):
    '''Calculate the '''
    # input [(4, 1), (4, 3)]
    result = []
    result = [CalculateEntropy(*i) for i in pair_input]
    min_index = np.argmin(result)
    route.append(pair_input[min_index])
    accum += result[min_index]
    pair_input = [(pair_input[min_index][1], i for i in G2.neighbors(pair_input[min_index][1]))]
    if accum <= threshold:
        CalculateEntropyPath(pair_input2)
    else:
        break

def Route(layer):
    pair = FindSameCom()
    pair = [[(x, k) for k in y] for x, y in layer.items()]
    for i in pair:
        CalculateEntropyPath(i)
        



# os.chdir('/Users/pengfeiwang/Desktop/IncrementalCDs/data/')
os.chdir('/Users/pengfeiwang/Desktop/test/add_links')
# com_map = LoadCom('./2004-04.com')
file1 = './2004-04-20'
file2 = './2004-04-21'
# file1 = './2004-04'
# file2 = './2004-05'
FindChanges(file1, file2)
