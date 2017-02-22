#!/usr/bin/env python
#coding:utf-8
"""
  Author: weiyi   --<weiyiliu@us.ibm.com>
  Author: pengfei --<>
  Purpose: Do Validation For our IncrementalCDs
  Created: 02/15/17
"""

import pickle
import networkx as nx 
import time, pickle
import sys
import random
import copy
from LPA_Algorithm import LPA

from BoundarySearch import LoadNetwork as LN

DebugFlag = True

########################################################################
class Validation:
    """
    Do validation
    
    提供的接口函数
    1. CreateGraph() 
    --- 将磁盘中的EdgeList文件转换成Networkx的图
    Usage: CreateGraph(graph_path)

    2. CompareTwoGraph() 
    --- 输入两张图，输出这两张图的不同的 节点占比 以及 边占比
    Usage: CompareTwoGraph(g1,g2)
    
    3. PartialChange() --- 给定一张图以及需要变化的部分（默认给定变换的节点占比），输出变化后的图
    Usage: PartialChange(base_graph, change_rate)
    """

    #----------------------------------------------------------------------
    def __init__(self):
        pass

    #----------------------------------------------------------------------
    def CreateGraph(self,graph_path):
        """
        Purpose: Get Edge_list file in the disk, and transfer it into networkx like graph
        Input: graph_path
        Output: graph
        """
        graph = nx.Graph(name=graph_path)
        with open(graph_path,'r+') as f:
            for line in f.readlines():
                try:
                    n1, n2 = line.strip().split(" ")
                except:
                    continue
                graph.add_node(int(n1))
                graph.add_node(int(n2))
                graph.add_edge(int(n1),int(n2))
        return graph

    #----------------------------------------------------------------------
    def CompareTwoGraph(self,g1,g2):
        """
        Purpose: Compare the Node Change Rate and Edge Change Rate for two graphs
        Input: 
            g1 --- Graph1
            g2 --- Graph2
        Output:
            Node_Change_Rate, Edge_Change_Rate
        """
        nodes1 = g1.nodes()
        nodes2 = g2.nodes()
        edges1 = g1.edges()
        edges2 = g2.edges()

        # node change rate
        changed_nodes = set(nodes2).union(set(nodes1))-set(nodes1).intersection(set(nodes2))
        Node_Change_Rate = len(changed_nodes)/len(nodes1)

        # edge change rate
        changed_edges = set(edges2).union(set(edges1))-set(edges1).intersection(set(edges2))
        Edge_Change_Rate = len(changed_edges)/len(edges1)

        print(len(changed_edges))

        return Node_Change_Rate, Edge_Change_Rate

    #----------------------------------------------------------------------
    def PartialChange(self,base_graph, change_rate):
        """
        Purpose: Input base_graph and change_rate, and change the nodes' behavior in the graph based on change_rate
                 In addition, there are three behaviors for a node: Del / Add Connection / Del Connection
                 For each changed node, we randomly choose one behavior 
        Input:
            base_graph --- the base graph wait for changing
            change_rate --- how many partial part in the graph we need change
        Output: changed_graph
        """
        if change_rate > 1:
            print("change rate is greater than 1!")
            sys.exit()

        # init
        nodes = base_graph.nodes()
        changed_node_size = int(len(nodes)*change_rate)
        if changed_node_size == 0: # guarantee that at least one node will change
            changed_node_size = 1
        changed_graph = copy.deepcopy(base_graph)

        # select changed nodes
        changed_node_list = random.sample(nodes,changed_node_size)
        if DebugFlag is True:
            print("Size: ",len(changed_node_list),end = "  ")

        for node in changed_node_list:
            # for each node, change the behavior of it
            # 1. select changed nodes' activity
            """
            del nodes --- flag = 1
            add connection --- flag = 2
            del connection --- flag = 3
            """
            change_activity_flag = random.randint(1,3)
            # change_activity_flag = 1
            #if DebugFlag is True:
                #print(change_activity_flag, end = " ")
            # 2. change node behavior based on the specific flag
            if change_activity_flag == 1:
                changed_graph = self.__del_node(changed_graph,node)
            elif change_activity_flag == 2:
                changed_graph = self.__add_connection(changed_graph,node,changed_node_list)
            elif change_activity_flag == 3:
                changed_graph = self.__del_connection(changed_graph,node,changed_node_list)
        
        return changed_graph
        
    #----------------------------------------------------------------------
    def __del_node(self,graph, node):
        """
        Purpose: Del the specific node and its edges in the graph
        Input: 
            graph
            node
        Output: changed_graph
        """
        changed_graph = copy.deepcopy(graph)
        edges = [edge for edge in changed_graph.edges() if node in edge]
        changed_graph.remove_node(node)
        #changed_graph.remove_edges_from(edges) --- remove node will also remove the edges
        return changed_graph

    #----------------------------------------------------------------------
    def __add_connection(self,graph,node,changed_node_list):
        """
        Purpose: Add an connection from node to another node in changed_node_list
                 otherwise, remove this node
        Input:
            graph
            node
            changed_node_list --- all nodes need to be changed
        Output: changed_graph
        """
        changed_graph = copy.deepcopy(graph)
        protential_nodes_for_connect = list(set(changed_node_list)-set([node]))
        add_flag = True
        while add_flag is True:
            if len(protential_nodes_for_connect) != 0:
                another_node = random.sample(protential_nodes_for_connect,1)[0]
                if another_node not in changed_graph.neighbors(node):
                    changed_graph.add_edge(node,another_node)
                    add_flag = False
                else:
                    protential_nodes_for_connect = list(set(protential_nodes_for_connect)-set([another_node]))
            else: # --- in the otherwise branch
                add_flag = False
                changed_graph.remove_node(node)
        return changed_graph

    #----------------------------------------------------------------------
    def __del_connection(self,graph,node,changed_node_list):
        """
        Purpose: Del an connection from node to another node in the changed_node_list it these two node have an edge, 
                 otherwise, Del the connection from random node in the graph
        Input:
            graph
            node
            changed_node_list --- all nodes need to be changed
        Output: changed_graph
        """
        changed_graph = copy.deepcopy(graph)
        protential_nodes_for_connect = list(set(changed_node_list)-set([node]))
        del_flag = True
        while del_flag is True:
            if len(protential_nodes_for_connect) != 0:
                another_node = random.sample(protential_nodes_for_connect,1)[0]
                if another_node in changed_graph.neighbors(node):
                    changed_graph.remove_edge(node,another_node)
                    del_flag = False
                else:
                    protential_nodes_for_connect = list(set(protential_nodes_for_connect)-set([another_node]))
            else: # --- in the otherwise branch
                del_flag = False
                edge_list = [edge for edge in changed_graph.edges() if node in edge]
                try: 
                    remove_edge = random.sample(edge_list,1)[0]
                    changed_graph.remove_edge(*remove_edge)
                except: 
                    """如果出现孤立节点，则直接将该孤立节点删掉"""
                    changed_graph.remove_node(node)
        return changed_graph




#----------------------------------------------------------------------
def test_graph_change(files,val):
    """
    Purpose: find graph Change for two graph
    """
    for i in files:
        file1, file2 = i
        g1 = val.CreateGraph(file1)
        g2 = val.CreateGraph(file2)
        n_rate, e_rate = val.CompareTwoGraph(g1,g2)
        print(file1,"---", file2,":\t", n_rate,"; ",e_rate)

#----------------------------------------------------------------------
def test_partial_change(val):
    """
    Purpose: test Partial Change func
    """
    base_graph = nx.random_graphs.barabasi_albert_graph(10000,2)

    # save save localfile
    record = {}
    temp = LN.FindRoute('./')
    base_graph_path = './base_dta'
    with open(base_graph_path, "w+") as f:
        for e in base_graph.edges():
            n1, n2 = e
            f.write(str(n1) + " " + str(n2) + "\n")
    LPA(base_graph_path)
    Changed_com_path = base_graph_path+".com"

    for i in range(0,101,1):
        change_rate = i/1000
        print("change_rate: ",change_rate,end = '\t')
        PCstart = time.time()
        change_graph = val.PartialChange(base_graph, change_rate)
        print("\nPC time: ", time.time() - PCstart)

        # ---------------------------------------------------------
        # calculate all kinds of time
        IOstart = time.time()
        change_graph_path = './change_dta'
        with open(change_graph_path, "w+") as g:
            for e in change_graph.edges():
                n1, n2 = e
                g.write(str(n1) + " " + str(n2) + "\n")
        # print("IO time:", time.time() - IOstart)
        G_out,BStime = LN.LoadNetworkEntrance(temp, base_graph_path, change_graph_path, Changed_com_path)
        # print("BS time:", BStime)
        record[change_rate] = BStime
        # ---------------------------------------------------------

        n_rate, e_rate = val.CompareTwoGraph(base_graph,change_graph)
        if DebugFlag is True:
            print("\t","NodeRate %.3f"%n_rate,"  ","EdgeRate %.3f"%e_rate)
    pickle.dump(record, open('./dict.pkl', 'wb'))

if __name__ == '__main__':

    data_path = "./data/Sx-superuser/"

    # init
    temp = LN.FindRoute(data_path)
    files = temp.PairFile()
    val = Validation()
    
    # test func
    # 1. test graph change func
    test_graph_change(files,val)

    # 2. test partial change
    test_partial_change(val)

