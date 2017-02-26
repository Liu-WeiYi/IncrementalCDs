#!/usr/bin/env python3.5
# coding: utf-8
import sys
import time
import itertools
from functools import reduce
import networkx as nx
from copy import deepcopy
from functools import wraps
from LPA_Algorithm import LPA
from BoundarySearch.LoadNetwork import FindRoute



def LoadNetworkEntrance(temp, G1, G2, Changed_com_path):
    """
    Entrance Func
    Return Changed Graph
    """
    com_map = temp.LoadCommunityFile(Changed_com_path)
    start = time.time()
    output = temp.Route(com_map, G1, G2)
    t = time.time() - start
    return output, t


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
            G.add_edge(int(n1), int(n2))
    nodes = G.nodes()
    adict = dict()
    adict = {_: len(G.neighbors(_)) for _ in nodes}
    adict_sort = sorted(adict.items(), key = lambda x: x[1], reverse = True)
    keys, values = zip(*adict_sort)
    sh = keys[:3]
    return(G, sh)

# @timeit
def NbrNetwork(G, r_node):
    '''
    Input: network, remove_node
    Output: new network
    '''
    nbrs = G.neighbors(r_node)
    nbrs = [_ for _ in nbrs if _ != r_node]
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

@timeit
def community_detection_calc(file):
    LPA(file)

def community_detection(file):
    LPA(file)

def LoadCommunityFile(com_file):
    '''Load the communities result'''
    # input: community detection file
    # output: dictionary, key is nodes, value is community
    com_content = open(com_file, encoding='utf-8').readlines()
    com_content = [list(map(int, _.split())) for _ in com_content]
    com_content = [_ for _ in com_content if _ != []]
    return com_content

if __name__ == "__main__":
    file = './data/Sx-stackoverflow/2016-02'
    # 2008-12
    # 2013-01
    # 2016-02
    G, sh = FindSuperHub(file)


    # for regular BS
    # community_detection(file)   # only do once for each file
    cd_t, algo_t, bs_t = [], [], []

    for num, i in enumerate(sh):
        print("Now it is", i)

        # for direct CD or approx BS
        output_name = file + '_approx_' + str(num + 1)
        start = time.time()
        nG = NbrNetwork(G, i)
        bs_t.append((time.time() - start))
        save2local(nG, output_name)
        cd_t.append(community_detection_calc(output_name))
        # algo_t.append(community_detection_calc(file))

        naive_com = LoadCommunityFile((file + '.com'))
        partial_com = LoadCommunityFile((output_name + '.com'))
        for _ in naive_com:
            if i in _:
                _.remove(i)
        partial_node = set(reduce(lambda x, y: x + y, partial_com))
        naive_com = list(map(lambda x: list(set(x) - set(partial_node)), naive_com))
        naive_com = naive_com + partial_com
        merge_output = file + "_approx_merge_" + str(num + 1)
        with open(merge_output, "w+") as fff:
            for com in naive_com:
                com = str(com).replace('[', '').replace(']','').replace(',','')
                fff.write(com + "\n")

    print("Approx CD time: ")
    [print(_) for _ in cd_t]
    print("Approx BS time: ")
    [print(_) for _ in bs_t]
    # print("Naive Algo time: ")
    # [print(_) for _ in algo_t]



    # # for regular BS
    # regular, cd = [], []
    # for num, i in enumerate(sh):
    #     print("Now it is", i, "Numbers:", len(G.neighbors(i)))
    #     temp = FindRoute('./data/Sx-stackoverflow/')

    #     Changed_com_path = file + ".com"
    #     G1 = G.copy()
    #     cccc = G.copy()
    #     cccc.remove_node(i)
    #     G2 = cccc     

    #     output, t = LoadNetworkEntrance(temp, G1, G2, Changed_com_path)
    #     regular.append(t)

    #     output_path = file + "_regular_" + str(num + 1)
    #     save2local(output, output_path)
    #     community_detection(output_path)
        
    #     # merge the community
    #     naive_com = LoadCommunityFile((file + '.com'))
    #     partial_com = LoadCommunityFile((output_path + '.com'))
    #     # naive_com = [_.remove(i) for _ in naive_com if i in _]
    #     for _ in naive_com:
    #         if i in _:
    #             _.remove(i)
    #     partial_node = set(reduce(lambda x, y: x + y, partial_com))
    #     naive_com = list(map(lambda x: list(set(x) - set(partial_node)), naive_com))
    #     naive_com = naive_com + partial_com
    #     merge_output = file + "_regular_merge_" + str(num + 1)
    #     with open(merge_output, "w+") as fff:
    #         for com in naive_com:
    #             com = str(com).replace('[', '').replace(']','').replace(',','')
    #             fff.write(com + "\n")


    #     # cd.append(community_detection_calc(output_path))
    # print("Regular BS")
    # [print(_) for _ in regular]
    # # print("Regular CD")
    # # [print(_) for _ in cd]

