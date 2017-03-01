#include <iostream>
#include <vector>
#include <set>
#include <map>
#include "networks.h"
#include "IncrementalGraphsProcess.h"
#include "edge_list_parser.h"



network<std::string,double> set_layer_1(){
    std::cout << "layer1 △-△ 网络" << std::endl;
    network<std::string,double> layer;
    layer.setName("Layer1");

    std::vector<std::string> node_list = {"A","B","C","D","E","F"};
    layer.add_nodes_from(node_list);
    layer.add_edge("A","B",1.0, false);
    layer.add_edge("A","C",0.2, false);
    layer.add_edge("B","C",0.3, false);
    layer.add_edge("C","D",0.2, false);
    layer.add_edge("D","E",0.7, false);
    layer.add_edge("D","F",0.6, false);
    layer.add_edge("E","F",0.7, false);

    return layer;
};

network<std::string,double> set_layer_2(){
    std::cout << "layer2 ⊠-⊠ 网络" << std::endl;
    network<std::string,double> layer;
    layer.setName("Layer2");

    std::vector<std::string> node_list = {"A","B","C","D","E","F","G","H"};
    layer.add_nodes_from(node_list);
    layer.add_edge("A","B",1.0, false);
    layer.add_edge("A","C",1.0, false);
    layer.add_edge("A","D",1.0, false);
    layer.add_edge("B","C",1.0, false);
    layer.add_edge("B","D",1.0, false);
    layer.add_edge("C","D",1.0, false);
    layer.add_edge("D","E",0.1, false);
    layer.add_edge("E","F",1.0, false);
    layer.add_edge("E","G",1.0, false);
    layer.add_edge("E","H",1.0, false);
    layer.add_edge("F","G",1.0, false);
    layer.add_edge("F","H",1.0, false);
    layer.add_edge("G","H",1.0, false);

    return layer;
};

void layer_info(network<std::string,double> layer) {
    std::cout << "Network name: " << layer.Name() << std::endl;

    std::set<std::string> node_list = layer.nodes();
    std::map<std::string, std::vector<std::map<std::string,double>>> edge_list = layer.edges();

    std::cout << "Nodes: ";
    for (auto it = node_list.begin(); it!= node_list.end(); it++) {std::cout << *it << " ";}
    std::cout << std::endl;

    std::cout << "Node/Edge Information:" << "\n";
    for (auto Node_it = node_list.begin();Node_it != node_list.end(); Node_it++){
        // 输出点信息
        std::string src = *Node_it;
        std::cout << "\tNode: " << src;
        std::cout << "\n";
        // 输出当前点的边信息
        std::vector<std::map<std::string,double>> current_edge_info = edge_list[src];
        std::cout << "\tEdges: ";
        for (int i = 0; i < current_edge_info.size(); ++i) {
            // 对每一条边
            std::map<std::string,double> dst_weight = current_edge_info[i];
            for (auto dst_it = dst_weight.begin(); dst_it != dst_weight.end();dst_it++){
                // 迭代输出当前边的源节点、目的节点、以及权重
                std::cout << "\t" << src << "---" << dst_it->first << "\t weight: " << dst_it->second << ";\t";
            }
        }
        std::cout << "\n";
        // 输出当前点的邻居信息
        std::cout << "\tNeighbors: "<< "\t";
        std::set<std::string> neighbors = layer.neighbors(src);
        for (auto it = neighbors.begin();it!=neighbors.end();it++){
            std::cout << *it << " ";
        }
        std::cout << "\n\t----------" << std::endl;
    }
    std::cout << "--------- 测试给定两个点，输出权重的函数 ---------" << std::endl;
    std::set<std::string> nodes = layer.nodes();
    for (auto node_it = nodes.begin(); node_it != nodes.end(); node_it++){
        std::string src = *node_it;
        std::set<std::string> neighbors = layer.neighbors(src);
        for (auto neighbor_it=neighbors.begin(); neighbor_it != neighbors.end();neighbor_it++){
            std::string dst = *neighbor_it;
            double weight = layer.get_weight(src,dst);
            std:: cout << src << "---" << dst << ": " << weight << "\t";
        }
    }
    std::cout << "\n--------- --------- --------- --------- ---------\n" << std::endl;

}

void showMultilayer_info(MultiNetwork<std::string, double> multilayerNetwork){
    /// 1. 输出当前多网络的每一个网络的名称
    for (int i = 0; i < multilayerNetwork.layers().size(); ++i) {
        network<std::string,double> currentLayer = multilayerNetwork.layers()[i];
        std::cout << "current layer is: " << currentLayer.Name() << ";\t";
    }
    /// 2. 输出当前多网络的所有节点
    std::set<std::string> nodes = multilayerNetwork.nodes();
    std::cout << "all nodes: " << "\t";
    for (auto node_it = nodes.begin();node_it!=nodes.end();node_it++){
        std::cout<< *node_it << " ";
    }
    std::cout << std::endl;

    /// 3. 输出当前多网络的所有节点的CN和GN信息
    std::cout << "All Nodes' CN and GN information: \n";
    for (auto node_it = nodes.begin(); node_it != nodes.end(); node_it++){
        std::cout << "\t current Node: " << *node_it << "\n";
        std::vector<std::set<std::string>> CN_GN = multilayerNetwork.CN_GN()[*node_it];
        std::set<std::string> CN = CN_GN[0];
        std::set<std::string> GN = CN_GN[1];

        std::cout << "\t\t CN Information: ";
        for (auto CN_it = CN.begin(); CN_it!=CN.end();CN_it++){
            std::cout << *CN_it << " ";
        }
        std::cout << "\n";
        std::cout << "\t\t GN Information: ";
        for (auto GN_it = GN.begin(); GN_it!=GN.end();GN_it++){
            std::cout << *GN_it << " ";
        }
        std::cout << "\n";

        std::cout << "\t\t Overlap Rate: " << multilayerNetwork.overlap_rate(*node_it) << "\n";

        std::cout << "\t----------\n";
    }
    std::cout << std::endl;

}

void show_Graph_process_Per_iteration_label_info(GraphProcess<std::string, double> graphProcess, int iteration = 0){
    std::cout << "\n------ ------ ------ ------ ------\n";
    std::cout<< "\nCurrent Iteration: " << iteration << std::endl;

    std::set<std::string> nodes;
    nodes = graphProcess.nodes();

    for (auto node_it = nodes.begin();node_it!=nodes.end();node_it++){
        std::string currentNode = *node_it;
        std::cout << "current Node: " << currentNode << "\t" << "Labels: ";

        /// 设置当前需要返回的轮数
        //int iteration = 0;

        std::set<std::string> currentLabels = graphProcess.label_list(currentNode,iteration);
        for (auto label_it=currentLabels.begin(); label_it!=currentLabels.end();label_it++){
                std::cout << *label_it << " ";
        }
        std::cout<<std::endl;
    }
}

void show_Graph_process_Per_iteration_communities(std::vector<std::set<std::string>> community){
    std::cout << "\n ------ ------ ------ ------ ------\n";
    std::cout << "\nCommunity Output:\n";

    for (int i = 0; i < community.size(); ++i) {
        std::set<std::string> currentCom = community[i];
        std::cout << "com_"<< i << ":\t";
        for (std::string node : currentCom){std::cout << node << " ";}
        std::cout << std::endl;
    }
}
/**
network<std::string,double> createLayer(std::map<int, vector<string>> edge_file, std::string name){
    network<std::string,double> network;
    network.setName(name);
    set<string> node_list_tmp;
    for (auto iter : edge_file){
        vector<string> edge = iter.second;
        string src = edge[0];
        string dst = edge[1];
        node_list_tmp.insert(src);
        node_list_tmp.insert(dst);
        // 构建网络的边
        network.add_edge(src, dst, 1.0, false);
    }

    // 将set 转换成 vector
    std::vector<std::string> node_list;
    for (auto node:node_list_tmp){
        if (node_list_tmp.find(node)!= node_list_tmp.end()){
            node_list.push_back(node);
        }
    }

    // 构建 网络 的点
    network.add_nodes_from(node_list);

    return  network;
};
*/














//int main() {
//
//    std::string filename = "2004-04";
//
//    std::map<int, vector<string>> edge_file = edge_list_parser(filename,filename);
//
//    std::cout << "\n---------------- 1. 构造网络 ----------------" << std::endl;
//    network<std::string,double> layer = createLayer(edge_file, filename);
//
////
////
////    std::cout << "\n---------------- 1. 构造单网络 ----------------" << std::endl;
////
////    network<std::string,double> layer = set_layer_1();
////    //layer_info(layer1);
////
////    network<std::string,double> layer2 = set_layer_2();
////    //layer_info(layer2);
////
//    std::cout << "测试LPA算法...\n";
//    LPA<std::string,double> lpa1(layer, false);
//    std::vector<std::set<std::string>> communities = lpa1.community();
//    show_Graph_process_Per_iteration_communities(communities);
//////    show_community_result(lpa1.community());
//////    std::cout << "\n";
//////    LPA<std::string,double> lpa2(layer2);
//////    show_community_result(lpa2.community());
////
////
////    std::cout << "\n---------------- 2. 构造多网络 ----------------" << std::endl;
////    std::vector<network<std::string,double>> layers;
////    layers.push_back(layer);
////    layers.push_back(layer1);
////    layers.push_back(layer2);
////
////    MultiNetwork<std::string,double> multilayerNetwork(layers);
////    showMultilayer_info(multilayerNetwork);
////
////    std::cout << "\n---------------- 3. 获取 有向 加权的融合网络 ----------------" << std::endl;
////    network<std::string,double> Directed_Weighted_MergedGraph = multilayerNetwork.merging_all_layers();
////    layer_info(Directed_Weighted_MergedGraph);
////
//////    std::cout << "测试LPA算法...\n";
//////    LPA<std::string,double> lpa_merged(Directed_Weighted_MergedGraph);
//////    std::vector<std::set<std::string>> community = lpa_merged.community();
//////    show_community_result(community);
////
////
////    std::cout << "\n---------------- 4. Incremental Graph Process ----------------" << std::endl;
////    /// 1. 创建当前网络
////    GraphProcess<std::string,double> graphProcess;
////    graphProcess.setGraph(Directed_Weighted_MergedGraph);
////
////    /// 2. 初始化更新轮数
////    int iteration = 0;
////
////    /// 3. 初始化该GP
////    graphProcess.InitLabels(iteration);
////
////    /// 4. 局部更新
////    std::set<std::string> nodes = graphProcess.nodes();
////    iteration += 1;
////    /// 对每一个节点，有：
////    for (auto it = nodes.begin(); it!= nodes.end(); it++){
////        std::string currentNode = *it;
////        std::cout << "\ncurrent Node: " << currentNode << std::endl;
////        //std::cout << "\t---> DEMON Related <---\n";
////        // DEMON...
////        // 3.1 获取每一个节点的EgoMinusEgo
////        //std::cout << "\t------> 1. EgoMinusEgo \n";
////        network<std::string,double> currentEgoMinusEgo = graphProcess.EgoMinusEgoNetwork(currentNode);
////        //layer_info(currentEgoMinusEgo);
////        //std::cout << "\t------------------------------\n";
////        // 3.2 更新当前点及其邻居的标签信息
////        LPA<std::string,double> lpa(currentEgoMinusEgo);
////        std::map<std::string, std::string> node_label_map = lpa.label_results();
////        graphProcess.update_label_list(node_label_map,iteration);
////    }
////    // 测试标签结果~
//////    show_Graph_process_Per_iteration_label_info(graphProcess, 0);
//////    show_Graph_process_Per_iteration_label_info(graphProcess, 1);
////
////    /// 5. 输出社团信息
////    double overlap_rate;
////    std:: cout << "please input expected overlap rate:\t";
////    std:: cin >> overlap_rate;
////    std::vector<std::set<std::string>> community = graphProcess.CurrentIterationCommunities(10,overlap_rate);
////    show_Graph_process_Per_iteration_communities(community);
//
//    std::cout << "\n\nALl Down!" << std::endl;
//    return 0;
//
//}

