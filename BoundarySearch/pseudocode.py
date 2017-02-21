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
                n* <= max{CalculateEntropy(node, n)}
                n** <= min{CalculateEntropy(node, n)}
        if nround < 2 or n** <= mean_threshold do
            update nround += 1
            update accum += CalculateEntropy(node, n*)
            update route <= tuple(node, n*)
            update node to n*
    return route