import networkx as nx

def LoadNetwork(file):
    '''
    load the network
    '''
    file_name = file.split('/')[-1]
    network = open(file, encoding='utf-8').readlines()
    network = [list(map(int, _.split())) for _ in network]
    l_edges = [tuple(_) for _ in network]
    l_nodes = list(set(sum(network, [])))
    # add edges
    G = nx.Graph(day = file_name)
    G.add_nodes_from(l_nodes)
    G.add_edges_from(l_edges)
    return(G)

file1 = '/Users/pengfeiwang/Desktop/IncrementalCDs/BoundarySearch/2004-04-20'
file2 = '/Users/pengfeiwang/Desktop/IncrementalCDs/BoundarySearch/2004-04'
G1 = LoadNetwork(file1)
G2 = LoadNetwork(file2)

# get the new nodes
new_nodes = list(set(G2.nodes()).difference(set(G1.nodes())))

# get the first layer
layer_1 = [G1.neighbors(_) for _ in new_nodes]

# find the largest entropy

