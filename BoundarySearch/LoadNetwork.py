import os
import glob
import networkx as nx

def LoadNetwork(file):
    '''
    load the network
    '''
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

def FindNewNode(G1, G2):
    G1_node = set(G1.nodes())
    G2_node = set(G2.nodes())
    new_nodes = list(G2_node - G1_node)
    if new_nodes: 
        return(new_nodes)
    else: 
        return([])

def PairFile(input_list):
    '''
    detect the changes from day to day
    '''
    return zip(*[input_list[_:] for _ in range(2)])

def ():



# file1 = './2004-04-20'
# file2 = './2004-04'
# G1 = LoadNetwork(file1)
# G2 = LoadNetwork(file2)
# new_nodes = FindNewNode(G2, G1)


pwd = '/Users/pengfeiwang/Desktop/IncrementalCDs/BoundarySearch/'
os.chdir(pwd)

files = glob.glob(os.path.join(pwd, '200*'))
pair_files = PairFile(files)
l_new_nodes = [FindNewNode(_, __) for _, __ in pair_files]
# get the first layer
layer_1 = [[G1.neighbors(_) for _ in new_nodes] for new_nodes in l_new_nodes]
# whether neighbors in the same community

# find the largest entropy

