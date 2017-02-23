#!/usr/bin/env python3.5
# coding: utf-8
import sys
import time
import itertools
import networkx as nx
from copy import deepcopy
from functools import wraps
from LPA_Algorithm import LPA
from BoundarySearch.LoadNetwork import *

def timeit(f):
    @wraps(f)
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        t = te - ts
        print('%r (%r, %r) %2.2f sec' %(f.__name__, args, kw, t))
        # print('%2.2f sec' %t)
        return t
    return timed

def FindSuperHub(file):
    G = nx.Graph()
    with open(file, "r+") as f:
        for line in f.readlines():
            n1, n2 = line.strip().split()
            G.add_edge(n1, n2)
    # G = FindRoute.LoadNetworkFile(file)
    nodes = G.nodes()
    adict = dict()
    adict = {_: len(G.neighbors(_)) for _ in nodes}
    adict_sort = sorted(adict.items(), key = lambda x: x[1], reverse = True)
    keys, values = zip(*adict_sort)
    sh = nodes[:3]
    return(G, sh)

@timeit
def NbrNetwork(G, r_node):
    '''
    Input: network, remove_node
    Output: new network
    '''
    nbrs = G.neighbors(r_node)
    nbrs_edges_p = set(list(itertools.permutations(nbrs, 2)))
    if nbrs_edges_p == {}:
        print("Something wrong with the superhub")
        sys.exit()
    all_edges = set(G.edges())
    nbrs_edges_t = list(all_edges & nbrs_edges_p)

    nG = nx.Graph()
    nG.add_nodes_from(nbrs)
    nG.add_edges_from(nbrs_edges_t)
    return(nG)

def save2local(G, output_name):
    with open(output_name, "w+") as g:
        for e in G.edges():
            n1, n2 = e
            g.write(str(n1) + " " + str(n2) + "\n")


# @timeit
def community_detection(file):
    LPA(file)


if __name__ == "__main__":
    file = './data/Sx-stackoverflow/2013-01'
    # 2016-02
    # 2008-12
    # 2013-01
    output_name = './data/Sx-stackoverflow/output.com'
    G, sh = FindSuperHub(file)
    bs_t, algo_t, regular, ld = [], [], [], []
    for i in sh:
        dp = i
        
        # for direct CD or approx BS
        # nG = NbrNetwork(G, dp)
        # save2local(nG, output_name)
        # print("For the Boundary Search: " ,end = "  ")
        # bs_t.append(community_detection(output_name))
        # print("For the algo directly:" ,end = "  ")
        # algo_t.append(community_detection(file))
    # [print(_) for _ in bs_t]
    # [print(_) for _ in algo_t]

        # for regular BS
        cccc = G
        temp = FindRoute('./data/Sx-stackoverflow/')
        community_detection(file)
        Changed_com_path = file + ".com"
        
        file1 = file
        cccc.remove_node(i)
        file2_name = file + "_c"
        with open(file2_name, "w+") as f:
            for e in cccc.edges():
                n1, n2 = e
                f.write(str(n1) + " " + str(n2) + "\n")

        file2 = file2_name     
        output, t = LoadNetworkEntrance(temp, file1, file2, Changed_com_path)

        output_path = file + "_new"
        with open(output_path, "w+") as f:
            for e in output.edges():
                n1, n2 = e
                f.write(str(n1) + " " + str(n2) + "\n")

        start = time.time()
        community_detection(output_path)
        ld.append(time.time()-start)
        regular.append(t)
    [print(_) for _ in regular]
    [print(_) for _ in ld]
