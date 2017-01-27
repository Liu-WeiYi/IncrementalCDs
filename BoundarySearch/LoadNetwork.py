#!/usr/bin/env python3.5

import os
from math import log
from glob import glob
import networkx as nx
import numpy as np
from functools import *
from scipy.special import comb


class Inc(object):
    def __init__(self, file_dir):
        self.file_dir = file_dir
        self.accum = 0
        self.threshold = 0.4
    
    def PairFile(self):
        '''Pair the files from day to day'''
        files = glob(os.path.join(self.file_dir, '200*'))
        paired_list = list(zip(*[files[_:] for _ in range(2)]))
        return paired_list
    
    def LoadNetwork(self, file):
        '''Construct the network'''
        file_name = file.split('/')[-1]
        network = open(file, encoding='utf-8').readlines()
        network = [list(map(int, _.split())) for _ in network]
        l_edges = [tuple(_) for _ in network]
        l_nodes = list(set(sum(network, [])))
        G = nx.Graph(day=file_name)
        G.add_nodes_from(l_nodes)
        G.add_edges_from(l_edges)
        return G
    
    def LoadCom(self, com_file):
        '''Load the communities result'''
        com_content = open(com_file, encoding='utf-8').readlines()
        com_content = [list(map(int, _.split())) for _ in com_content]
        com_nums = range(1, len(com_content) + 1)
        com_map = {i: com_num for com_num, com in zip(com_nums, com_content) for i in com}
        return com_map
    
    def FindChanges(self, file1, file2):
        '''Find all the changes btn two networks'''
        self.G1 = self.LoadNetwork(file1)
        self.G2 = self.LoadNetwork(file2)
        G1_node = set(self.G1.nodes())
        G2_node = set(self.G2.nodes())
        G1_edge = set(self.G1.edges())
        self.G2_edge = set(self.G2.edges())
        add_nodes = list(G2_node - G1_node)
        del_nodes = list(G1_node - G2_node)
        c_nodes = add_nodes + del_nodes
        add_edges = list(self.G2_edge - G1_edge)
        del_edges = list(G1_edge - self.G2_edge)
        all_changes = {}
        # all_changes.update({_: self.G2.neighbors(_) for _ in add_nodes})
        all_changes.update({_: [__ for __ in self.G2.neighbors(_) if __ in G1_node] for _ in add_nodes})
        del_ndoes_influence = {_: self.G1.neighbors(_) for _ in del_nodes}
        all_changes.update({i: [k for k in j if k in G2_node] for i, j in del_ndoes_influence.items()})
        if add_edges:
            add_nodes_links = [(_, __) for _ in add_nodes for __ in self.G2.neighbors(_)]
            # add_edges = [_ for _ in add_edges if _ not in add_nodes_links and tuple(reversed(_)) not in add_nodes_links]
            add_edges = list(set(add_edges) - set(add_nodes_links) - set(tuple(reversed(i)) for i in add_nodes_links))
            try:
                add_edges_n = [_[__] for _ in add_edges for __ in range(2)]
                add_edges_n = list(set(add_edges_n))
                add_edges_n_nei = {_: self.G2.neighbors(_) for _ in add_edges_n}
                all_changes.update({i: [k for k in j if k not in add_nodes] for i, j in add_edges_n_nei.items()})
            except:
                pass
        if del_edges:
            del_nodes_links = [(_, __) for _ in del_nodes for __ in self.G1.neighbors(_)]
            # del_edges = [_ for _ in del_edges if _ not in del_nodes_links and tuple(reversed(_)) not in del_nodes_links]
            del_edges = list(set(del_edges) - set(del_nodes_links) - set(tuple(reversed(i)) for i in del_nodes_links))
            try:
                del_edges_n = [_[__] for _ in del_edges for __ in range(2)]
                del_edges_n = list(set(del_edges_n))
                all_changes.update({_: [__ for __ in temp.G2.neighbors(_) if __ not in add_nodes] for _ in del_edges_n})
            except:
                pass
        all_changes = {i:j for i,j in all_changes.items() if j != []}
        return all_changes, c_nodes
    
    def FindSameCom(self, Com_result, file1, file2):
        '''check whether the changes'''
        # input
        # output {1: [2, 3], 2: [3, 4]}
        com_map = self.LoadCom(Com_result)
        all_changes, c_nodes = self.FindChanges(file1, file2)
        layer = {}
        layer.update({i: j for i, j in all_changes.items() if i in c_nodes})
        layer.update({i: [k for k in j if com_map[i] == com_map[k]] for i, j in all_changes.items() if i not in c_nodes})
        return layer
    
    def CalculateEntropy(self, node_a, node_b):
        '''Calculate the entropy between two nodes'''
        # input (4, 1)
        degree_a = len(self.G2.neighbors(node_a))
        degree_b = len(self.G2.neighbors(node_b))
        degree_tot = len(self.G2_edge)
        print(degree_a, degree_b, degree_tot)
        denom = comb(degree_tot, degree_a)
        num = comb(degree_tot - degree_a, degree_b)  # maybe result in 0
        p_ab = 1 - num / denom
        influence = -log(p_ab)   # ValueError: math domain error
        return influence
    
    def CalculateEntropyPath(self, pair_input):
        '''Calculate the '''
        # input [(4, 1), (4, 3)]
        while self.accum <= self.threshold:
            result = []
            route = []
            result = [self.CalculateEntropy(*i) for i in pair_input]
            min_index = np.argmin(result)
            route.append(pair_input[min_index])
            self.accum += result[min_index]
            pair_input = [(pair_input[min_index][1], i) for i in self.G2.neighbors(pair_input[min_index][1])]
            return route
    
    def Route(self, Com_result, file1, file2):
        '''Find the best route'''
        layer = self.FindSameCom(Com_result, file1, file2)
        pair = [[(x, k) for k in y] for x, y in layer.items()]
        for i in pair:
            self.CalculateEntropyPath(i)

if __name__ == "__main__":
    temp = Inc('/Users/pengfeiwang/Desktop/test/test/')
    files = temp.PairFile()
    print(files)
    temp.FindChanges(files[0][0], files[0][1])
    temp.Route('/Users/pengfeiwang/Desktop/IncrementalCDs/data/2004-04.com.txt' ,files[0][0], files[0][1])


# os.chdir('/Users/pengfeiwang/Desktop/IncrementalCDs/data/')