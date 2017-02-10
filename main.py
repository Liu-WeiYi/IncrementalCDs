# coding: utf-8
from BoundarySearch import LoadNetwork as LN
from Louvain_Algorithm import Louvain
from LPA_Algorithm import LPA

# LN.LoadNetworkEntrance()

# graph_path = "./data/2004"
data_path = "./data/"

if __name__ == "__main__":
    # init
    temp = LN.FindRoute(data_path)
    files = temp.PairFile()
    temp.PairFile()

    # find com
    for i in range(len(files)):
        # input ---> two graph
        temp.FindChanges(*files[i])
        # input ---> current community
        # 1. find Communities
        file1 = files[i][0]
        file2 = files[i][1]

        if i == 0: # for the first time, graph is the file1 (2004-04)
            graph_path = file1
        # find changed graph's communities
        LPA(graph_path)

        # 2. Merge Changed Community and Original Community
        """
        NEED MERGE:
        1. Changed Graph
        2. Original Graph
        """
        merged_com = graph_path+".com"

        # find Changed Graph
        G_out = LN.LoadNetworkEntrance(temp, file1, file2, merged_com) # NEED ATTENTION!! NEED MERGED COMMUNITY RESULTS!!

        # output ---> write graph into disk
        changed_graph_path = "%sChanged_Graph"%data_path
        with open(changed_graph_path,"w+") as f:
            for e in G_out.edges():
                n1, n2 = e
                f.write(str(n1)+" "+str(n2)+"\n")

        # find the community in the influenced path
        LPA(changed_graph_path)
        changed_graph_path_com = changed_graph_path+".com"

        # load the result and merge 
        changed_com = changed_graph_path+".com"
        d = LN.MergeNewCom(temp, merged_com, file2, changed_graph_path_com)
        print(d)

        # save into file
        new_com = "%sNewoutput"%data_path
        with open(new_com, "w+") as output:
            for com in d.values():
                output.write(com+"\n")
        break





