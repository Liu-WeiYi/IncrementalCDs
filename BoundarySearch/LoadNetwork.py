#!/usr/bin/env python3.5

import os
import glob
import networkx as nx
from functools import *

# class Inc(object):
#     def __init__(self, file_dir):
#         self.file_dir = file_dir

def PairFile(file_dir):
    # detect the changes from day to day
    files = glob.glob(os.path.join(file_dir, '200*'))
    paired_list = list(zip(*[files[_:] for _ in range(2)]))
    return(paired_list)

def LoadNetwork(file):
    # load the network
    file_name = file.split('/')[-1]
    network = open(file, encoding = 'utf-8').readlines()
    network = [list(map(int, _.split())) for _ in network]
    l_edges = [tuple(_) for _ in network]
    l_nodes = list(set(sum(network, [])))
    # add edges
    G = nx.Graph(day = file_name)
    G.add_nodes_from(l_nodes)
    G.add_edges_from(l_edges)
    return(G)

def LoadCom(com_file):
    com_content = open(com_file, encoding = 'utf-8').readlines()
    com_content = [list(map(int, _.split())) for _ in com_content]
    com_nums = range(1, len(com_content)+1)
    com_map = {i: com_num for com_num, com in zip(com_nums, com_content) for i in com}
    return(com_map)

def FindChanges(file1, file2):
    G1 = LoadNetwork(file1)
    G2 = LoadNetwork(file2)
    G1_node = set(G1.nodes())
    G2_node = set(G2.nodes())
    G1_edge = set(G1.edges())
    G2_edge = set(G2.edges())
    add_nodes = list(G2_node - G1_node)
    del_nodes = list(G1_node - G2_node)
    add_edges = list(G2_edge - G1_edge)
    del_edges = list(G1_edge - G2_edge)
    add_edges_n = list(reduce(lambda x, y: x + y, add_edges))
    del_edges_n = list(reduce(lambda x, y: x + y, del_edges))
    all_changes = {}
    all_changes.update({_: G2.neighbors(_) for _ in add_nodes})
    all_changes.update({_: G1.neighbors(_) for _ in del_nodes})
    all_changes.update({_: G2.neighbors(_) for _ in add_edges_n})
    all_changes.update({_: G1.neighbors(_) for _ in del_edges_n})
    return(all_changes)
        


def CheckSameCom(Com_result, changed_ele):
    # load the Com result {com: [node1, node2], 2: [node3, node4]}
    # changed_ele {node: [node1, node2]}
    com_map = LoadCom()
    all_changes = FindChanges() # {9: [16, 17, 18, 22, 24, 10, 11, 14, 15], 10: [9, 15], 11: [9], 30: [9, 11], 15: [9, 10]}






    def CalcuEntropy(node1, node2):
        a = len(G.neighbors(node1))
        b = len(G.neighbors(node2))
        probability = 1.0 / (a*b)


    def FindMinorCommunity(C, new_nodes):
        # find the c of new nodes




        pass



# file1 = './2004-04-20'
# file2 = './2004-04'
# G1 = LoadNetwork(file1)
# G2 = LoadNetwork(file2)
# new_nodes = FindNewNode(G2, G1)


pwd = '/Users/pengfeiwang/Desktop/IncrementalCDs/BoundarySearch/'
os.chdir(pwd)

pair_files = PairFile(files)
l_new_nodes = [FindNewNode(_, __) for _, __ in pair_files]
# get the first layer
layer_1 = [[G1.neighbors(_) for _ in new_nodes] for new_nodes in l_new_nodes]
# whether neighbors in the same community

# find the largest entropy

