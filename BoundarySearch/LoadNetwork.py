#!/usr/bin/env python3.5

import os
from math import log
from glob import glob
import networkx as nx
import numpy as np
from functools import *
from scipy.special import comb


class FindRoute(object):
    def __init__(self, file_dir, mean_threshold = 0.5):
        self.file_dir = file_dir
        self.accum_threshold = 4
        self.mean_threshold = mean_threshold
    
    def PairFile(self):
        '''Pair the files in the directory from day to day'''
        files = [_ for _ in glob(os.path.join(self.file_dir, '200*')) if _.find('com') <= 0 and _.find('changed') <= 0]
        paired_list = list(zip(*[files[_:] for _ in range(2)]))
        return paired_list
    
    def LoadNetworkFile(self, file):
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
    
    def LoadCommunityFile(self, com_file):
        '''Load the communities result'''
        # input: community detection file
        # output: dictionary, key is nodes, value is community
        com_content = open(com_file, encoding='utf-8').readlines()
        com_content = [list(map(int, _.split())) for _ in com_content]
        com_content = [_ for _ in com_content if _ != []]
        com_nums = range(1, len(com_content) + 1)
        com_map = {i: com_num for com_num, com in zip(com_nums, com_content) for i in com}
        return com_map
    
    def FindChanges(self, file1, file2):
        '''Find all the changes btn two networks'''
        self.G1 = self.LoadNetworkFile(file1)
        self.G2 = self.LoadNetworkFile(file2)
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
        all_changes.update({_: [__ for __ in self.G2.neighbors(_) if __ in G1_node] for _ in self.add_nodes})
        # any neighbors of deleted nodes should be influenced if the neighbors still in G2
        # we remove the del nodes and starts with its neighbors
        del_ndoes_influence = {_: self.G1.neighbors(_) for _ in del_nodes}
        del_nodes_still_nodes = [k for i, j in del_ndoes_influence.items() for k in j if k in G2_node]
        remove_new_nodes = {i: self.G2.neighbors(i) for i in del_nodes_still_nodes if i in G2_node}
        all_changes.update({i: [k for k in j if k in G1_node] for i, j in remove_new_nodes.items()})
        # all_changes.update({i: self.G2.neighbors(i) for i in del_nodes_still_nodes if i in G2_node})
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
    
    def FindSameCom(self, Com_result, file1, file2):
        '''Check whether the changes'''
        # input: community resule file, paired file
        # output {1: [2, 3], 2: [3, 4]}
        com_map = self.LoadCommunityFile(Com_result)
        all_changes = self.FindChanges(file1, file2)
        layer = {}
        layer.update({i: j for i, j in all_changes.items() if i in self.add_nodes})
        # to be fixed
        layer.update({i: [k for k in j if com_map[i] == com_map[k]] for i, j in all_changes.items() if i not in self.add_nodes})
        return layer
    
    def CalculateEntropy(self, node_a, node_b):
        '''Calculate the entropy between two nodes'''
        # input: the links btw two nodes (4, 1)
        # result: the information gain
        degree_a = len(self.G2.neighbors(node_a))
        degree_b = len(self.G2.neighbors(node_b))
        degree_tot = len(self.G2_edge)
        denom = comb(degree_tot, degree_a)
        num = comb(degree_tot - degree_b, degree_a) 
        p_ab = 1 - num / denom
        influence = -log(p_ab)  
        return influence
    
    def CalculateEntropyPath(self, pair_input):
        '''Calculate the shortest route'''
        # input [(4, 1), (4, 3)]
        accum = 0
        route = []
        while accum <= self.accum_threshold:
            result = []
            result = [self.CalculateEntropy(*i) for i in pair_input]
            min_index = np.argmin(result)
            route.append(pair_input[min_index])
            accum += result[min_index]
            pair_input = [(pair_input[min_index][1], i) for i in self.G2.neighbors(pair_input[min_index][1])]
        # num_layers = len(route)
        # mean_information_gain = accum / num_layers
        # print("Route is", route)
        return route
    
    def Route(self, Com_result, file1, file2):
        '''Find the best route'''
        layer = self.FindSameCom(Com_result, file1, file2)
        pair = [[(x, k) for k in y] for x, y in layer.items()]
        result = []
        for i in pair:
            if i != []:
                result += self.CalculateEntropyPath(i) 
        G_out = nx.Graph(day='output_nx')
        G_out_nodes = list(set(reduce(lambda x, y: x + y, result)))
        G_out.add_nodes_from(G_out_nodes)
        G_out.add_edges_from(result)
        return(G_out)


if __name__ == "__main__":
    #os.chdir('/Users/pengfeiwang/Desktop/IncrementalCDs/')
    temp = FindRoute('./data/')
    files = temp.PairFile()
    # temp.FindChanges(*files[0])
    Com_result = './data/2004-04.com'
    # temp.FindSameCom(Com_result, *files[0])
    result = temp.Route(Com_result, *files[0])
    #print(result)

def LoadNetworkEntrance(temp, file1, file2, Changed_com_path):
    """
    Entrance Func
    Return Changed Graph
    """
    #temp = FindRoute('./data/')
    #files = temp.PairFile()
    # Com_result = './data/2004-04.com'
    Com_result = Changed_com_path
    return temp.Route(Com_result, file1, file2)
  

def MergeNewCom(temp, old_com, file2, changed_com):
    old_com = temp.LoadCommunityFile(old_com)
    file2 = temp.LoadNetworkFile(file2)
    new_del = {i: j for i, j in old_com.items() if i in file2.nodes()}
    old_com_max = max(new_del.values())
    changed_com = temp.LoadCommunityFile(changed_com)
    changed_com_update = {i: j + old_com_max for i, j in changed_com.items()}
    new_del.update(changed_com_update)
    d = {}
    for key, value in new_del.items():
        d.setdefault(value, []).append(key)
    d = {i: ' '.join(map(str, j)) for i,j in d.items()}
    return(d)



