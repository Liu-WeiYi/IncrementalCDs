#!/usr/bin/env python3.5
# coding: utf-8
import os
import re
import time
from math import log
from glob import glob
import networkx as nx
import numpy as np
from functools import *
from scipy.special import comb


class FindRoute(object):
    def __init__(self, file_dir, mean_threshold = 0.5):
        self.file_dir = file_dir
        self.accum_threshold = 2
        # if mean_threshold too small, may result in no community in changes nodes
        self.mean_threshold = mean_threshold
    

    def PairFile(self):
        '''Pair the files in the directory'''
        files = [_ for _ in glob(os.path.join(self.file_dir, '*')) if re.search('^\d{4}-\d{2}-\d{2}$', _.split('/')[-1]) and '.com' not in _]
        paired_list = list(zip(*[files[_:] for _ in range(2)]))
        return paired_list
    

    @staticmethod
    def LoadNetworkFile(file):
        '''Construct the network'''
        # input: the file path
        # output: the network of the file
        file_name = file.split('/')[-1]
        network = open(file, encoding='utf-8').readlines()
        network = [list(map(int, _.split())) for _ in network]
        l_edges = [tuple(_) for _ in network]
        l_nodes = list(set(sum(network, [])))
        G = nx.Graph(day=file_name)
        G.add_nodes_from(l_nodes)
        G.add_edges_from(l_edges)
        return G
    

    @staticmethod
    def LoadCommunityFile(com_file):
        '''Load the communities result'''
        # input: community detection file
        # output: dictionary, key is nodes, value is community
        com_content = open(com_file, encoding='utf-8').readlines()
        com_content = [list(map(int, _.split())) for _ in com_content]
        com_content = [_ for _ in com_content if _ != []]
        com_nums = range(1, len(com_content) + 1)
        com_map = {i: com_num for com_num, com in zip(com_nums, com_content) for i in com}
        return com_map
    

    def FindChanges(self, G1, G2):
        '''Find all the changes btn two networks'''
        # Input: two networks
        #        EXAMPLE: G1 = LoadNetworkFile(file1)
        #                 G2 = LoadNetworkFile(file2)
        self.G1 = G1
        self.G2 = G2
        G1_node = set(self.G1.nodes())
        G2_node = set(self.G2.nodes())
        G1_edge = set(self.G1.edges())
        self.G2_edge = set(self.G2.edges())
        self.add_nodes = list(G2_node - G1_node)
        del_nodes = list(G1_node - G2_node)
        add_edges = list(self.G2_edge - G1_edge)
        del_edges = list(G1_edge - self.G2_edge)
        all_changes = {}
        # added and deleted nodes
        # any neighbors of newly-added nodes should be influenced
        all_changes.update({_: [__ for __ in self.G2.neighbors(_)] for _ in self.add_nodes})
        # any neighbors of deleted nodes should be influenced if the neighbors still in G2
        # we remove the del nodes and starts with its neighbors
        del_ndoes_influence = {_: self.G1.neighbors(_) for _ in del_nodes}
        del_nodes_still_nodes = [k for i, j in del_ndoes_influence.items() for k in j if k in G2_node]
        remove_new_nodes = {i: self.G2.neighbors(i) for i in del_nodes_still_nodes if i in G2_node}
        all_changes.update({i: [k for k in j if k in G1_node] for i, j in remove_new_nodes.items()})
        if add_edges:
            add_nodes_links = [(_, __) for _ in self.add_nodes for __ in self.G2.neighbors(_)]
            add_edges = list(set(add_edges) - set(add_nodes_links) - set(tuple(reversed(i)) for i in add_nodes_links))
            try:
                add_edges_n = [_[__] for _ in add_edges for __ in range(2)]
                add_edges_n = list(set(add_edges_n))
                add_edges_n_nei = {_: self.G2.neighbors(_) for _ in add_edges_n}
                all_changes.update({i: [k for k in j if k not in self.add_nodes] for i, j in add_edges_n_nei.items()})
            except:
                pass
        if del_edges:
            del_nodes_links = [(_, __) for _ in del_nodes for __ in self.G1.neighbors(_)]
            del_edges = list(set(del_edges) - set(del_nodes_links) - set(tuple(reversed(i)) for i in del_nodes_links))
            try:
                del_edges_n = [_[__] for _ in del_edges for __ in range(2)]
                del_edges_n = list(set(del_edges_n))
                all_changes.update({_: [__ for __ in self.G2.neighbors(_) if __ not in self.add_nodes] for _ in del_edges_n})
            except:
                pass
        all_changes = {i:j for i,j in all_changes.items() if j != []}
        return all_changes
    

    def FindSameCom(self, com_map, G1, G2):
        '''Check whether the changes in the same community'''
        # input: community map(the output of function LoadCommunityFile), paired networks
        # output {1: [2, 3], 2: [3, 4]}
        self.com_map = com_map
        all_changes = self.FindChanges(G1, G2)
        layer = {}
        layer.update({i: j for i, j in all_changes.items() if i in self.add_nodes})
        layer.update({i: [k for k in j if self.com_map[i] == self.com_map[k]] for i, j in all_changes.items() if i not in self.add_nodes})
        return layer
    

    def CalculateEntropy(self, node_a, node_b):
        '''Calculate the entropy between two nodes'''
        # input: the links btw two nodes (4, 1)
        # result: the information gain
        degree_a = len(self.G2.neighbors(node_a))
        degree_b = len(self.G2.neighbors(node_b))
        degree_tot = len(self.G2_edge)
        denom = comb(degree_tot, degree_b)
        num = comb(degree_tot - degree_a, degree_b) 
        p_ab = 1 - num / denom
        influence = -log(p_ab)  
        return influence


    def CalculateEntropyPath(self, pair_input):
        '''Calculate the shortest route'''
        # input [(4, 1), (4, 3)]
        accum = 0
        route = []
        nround = 1
        been_route = []
        while accum <= self.accum_threshold:
            if pair_input == []:
                return route
            been_route.append(pair_input[0][0])
            result = []
            result = [self.CalculateEntropy(*i) for i in pair_input]
            min_index = np.argmin(result)
            max_index = np.argmax(result)
            if result[min_index] < self.mean_threshold or nround < 2:
                accum += result[max_index]
                route = route + pair_input

                new_start_node = pair_input[max_index][1]
                if new_start_node not in self.add_nodes:
                    new_node_com = self.com_map[new_start_node]
                    new_neighbors = [_ for _ in self.G2.neighbors(new_start_node) if _ not in self.add_nodes and self.com_map[_] == new_node_com]
                elif new_start_node in self.add_nodes:
                    new_neighbors = [_ for _ in self.G2.neighbors(new_start_node)]
                new_neighbors = [_ for _ in new_neighbors if _ not in been_route]
                pair_input = [(new_start_node, _) for _ in new_neighbors]
                nround += 1
            else:
                break
        return route
    

    def Route(self, com_map, G1, G2):
        '''Find the best route'''
        layer = self.FindSameCom(com_map, G1, G2)
        pair = [[(x, k) for k in y] for x, y in layer.items()]
        result = []
        for i in pair:
            if i != []:
                result += self.CalculateEntropyPath(i) 
        G_out = nx.Graph(day='output_nx')
        try:
            G_out_nodes = list(set(reduce(lambda x, y: x + y, result)))
        except:
            G_out_nodes = []
        G_out.add_nodes_from(G_out_nodes)
        G_out.add_edges_from(result)
        return G_out


def LoadNetworkEntrance(temp, file1, file2, Changed_com_path):
    """
    Entrance Func
    Return Changed Graph
    """
    com_map = temp.LoadCommunityFile(Changed_com_path)
    G1 = temp.LoadNetworkFile(file1)
    G2 = temp.LoadNetworkFile(file2)
    start = time.time()
    output = temp.Route(com_map, G1, G2)
    t = time.time() - start
    return output, t
  

def MergeNewCom(temp, old_com, file2, changed_com):
    '''Merge the old and changed one, return the new community'''
    old_com = temp.LoadCommunityFile(old_com)
    file2 = temp.LoadNetworkFile(file2)
    # keep unchanged one and assign changed nodes new communities
    new_del = {i: j for i, j in old_com.items() if i in file2.nodes()}
    try:
        old_com_max = max(new_del.values())
    except:
        old_com_max = 0
    changed_com = temp.LoadCommunityFile(changed_com)
    changed_com_update = {i: j + old_com_max for i, j in changed_com.items()}
    new_del.update(changed_com_update)
    left_nodes = list(set(file2.nodes()) - set(new_del.keys()))
    old_com_max = max(new_del.values())
    num = len(left_nodes)
    y = range(old_com_max + 1, old_com_max + num + 1)
    new_del.update({i: j for i, j in zip(left_nodes, y)})
    d = {}
    for key, value in new_del.items():
        d.setdefault(value, []).append(key)
    d = {i: ' '.join(map(str, j)) for i,j in d.items()}
    return(d)



