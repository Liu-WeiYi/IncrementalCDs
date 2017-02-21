Input: Vc, accum_threshold, mean_threshold
Output: route


foreach each node in {Vc} do
    node <= FindSameCom()
    FindSameCom help find all the neighbors of node that in the same commnities

    Initialise
    an empty list route
    accum = 0
    nround = 1

    while accum <= accum_threshold do
    
        foreach each n in node.neighbors do
            Find:
                EntropyList <= CalculateEntropy(node, n)
                n* <= find the neighbor-node that max(EntropyList)
                minEntropy = min(EntropyList)

        if nround < 2 or minEntropy <= mean_threshold do
            update nround += 1
            update accum += max_entropy
            update route <= tuple(node, n*)
            update node to n*
        else:
            END the loop
    END

Initialise a new networkx nx;
nx.nodes() <= all nodes that appear in route
nx.edges() <= egdes in route

return nx
nx is the new network 

END

