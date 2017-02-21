Input: Com_result, file1, file2, Vc, accum_threshold, mean_threshold
Output: a new graph


Initialise an empty list route

foreach each node in {Vc} do
    next_target <= FindSameCom(Com_result, file1, file2)

    FindSameCom help find all the neighbors of node that in the same 
    commnities. If node is a newly-add node, we keep all the neighbors
    Com_result is the community result of file1

    Initialise
    accum = 0
    nround = 1

    while accum <= accum_threshold do

        foreach each n in neighbors do
            Find:
                EntropyList <= CalculateEntropy(node, n)
                n* <= find the neighbor-node that max(EntropyList)
                minEntropy = min(EntropyList)

        if nround < 2 or minEntropy <= mean_threshold do
            update nround += 1
            update accum += max_entropy
            update route <= edges between node and all its neighbors
            update node to n*
            update neighbors:
                if n* is not unique in file2:
                    only the neighbors that have same commnities
                elif n* is a unique in file2:
                    all neighbors of n*

        else:
            END the loop
    END

Initialise a new networkx nx;
nx.nodes() <= all nodes that appear in route
nx.edges() <= egdes in route

return nx
nx is the new network 

END

