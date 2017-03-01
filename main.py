# coding: utf-8
import time
from LPA_Algorithm import LPA
from DEMON_Algorithm import DEMON
from Louvain_Algorithm import Louvain
from BoundarySearch import LoadNetwork as LN


data_path = "./data/Email_EU_daily/"

if __name__ == "__main__":
    # init
    temp = LN.FindRoute(data_path)
    files = temp.PairFile()
    BS_time_l = []
    Method_time_l = []
    # find com
    for i in range(len(files)):
        # input ---> two graph
        # temp.FindChanges(*files[i])
        # input ---> current community
        # 1. find Communities
        file1 = files[i][0]
        file2 = files[i][1]

        graph_path = file1

        if i == 0: # for the first time, graph is the file1 (2004-04)
            # find changed graph's communities
            # LPA(graph_path)
            DEMON(graph_path)
            # Louvain(graph_path)

        # 2. Merge Changed Community and Original Community
        """
        NEED MERGE:
        1. Changed Graph
        2. Original Graph
        """
        merged_com = graph_path+".com"

        # find Changed Graph
        G_out, BS_time = LN.LoadNetworkEntrance(temp, file1, file2, merged_com) # NEED ATTENTION!! NEED MERGED COMMUNITY RESULTS!!
        BS_time_l.append(BS_time)

        # output ---> write graph into disk
        changed_graph_path = file2 + "_changed"
        with open(changed_graph_path, "w+") as f:
            for e in G_out.edges():
                n1, n2 = e
                f.write(str(n1) + " " + str(n2) + "\n")

        # find the community in the influenced path
        method_start = time.time()
        
        # LPA(changed_graph_path)
        DEMON(changed_graph_path)
        # Louvain(changed_graph_path)

        Method_time_l.append(time.time() - method_start)
        
        changed_graph_path_com = changed_graph_path+".com"

        # load the result and merge 
        changed_com = changed_graph_path + ".com"
        d = LN.MergeNewCom(temp, merged_com, file2, changed_graph_path_com)

        # save into file
        new_com = file2 + '.com'
        with open(new_com, "w+") as output:
            for com in d.values():
                output.write(com + "\n")

    print("Boundary Search time: ", BS_time_l)
    print("\nCommunity Detection time: ", Method_time_l)





