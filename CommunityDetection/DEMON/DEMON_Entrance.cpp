#include <iostream>
#include "IncrementalGraphsProcess.h"
#include <fstream>
#include "edge_list_parser.h"
using namespace std;

#define SHOW_DEBUG false



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

void showCommunities(std::vector<std::set<std::string>> community){
    std::cout << "\n ------ ------ ------ ------ ------\n";
    std::cout << "\nCommunity Output:\n";

    for (int i = 0; i < community.size(); ++i) {
        std::set<std::string> currentCom = community[i];
        std::cout << "com_"<< i << ":\t";
        for (std::string node : currentCom){std::cout << node << " ";}
        std::cout << std::endl;
    }
}

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



int main(int argc, char *argv[]){

    if (argc < 2 | argc > 3){
        cout << "Usage: edge.list overlap_rate [-w]"
                "\n\tedge.list    ---> Edge_List File"
                "\n\toverlap_rate ---> overlap_rate ∈ [0,1]"
                "\n\t-w           ---> optional: weight flag" << endl;
        exit(EXIT_FAILURE);
    }
    else {
        // 获取需要读入的文件名
        string filename = argv[1];
        // 指定社团的重叠率
        double overlap_rate = atof(argv[2]);
        if (overlap_rate > 1 | overlap_rate < 0) {
            cout << "overlap_rate shoud between [0,1]." << endl;
            exit(EXIT_FAILURE);
        }
        // 指定当前读入的网络是否有权重
        bool weightedFlag = false;
        if (argv[3] == "-w") {
            weightedFlag = true;
        }
        cout << "\nprocessing file: " << filename << "\tweighted: " << weightedFlag << endl;

        /// 1. 生成edge文件
        std::map<int, vector<string>> edge_file = edge_list_parser(filename,filename);
        /// 2. 构成网络
        network<std::string,double> layer = createLayer(edge_file, filename);
        /// 3. 调用DEMON算法
        // -------------------------------------------------------------------------------- //
        // 3.1. 创建当前网络
        GraphProcess<std::string,double> graphProcess;
        graphProcess.setGraph(layer);
        // 3.2. 初始化更新轮数
        int iteration = 0;
        // 3.3. 初始化该GP
        graphProcess.InitLabels(iteration);
        // 3.4. 局部更新
        std::set<std::string> nodes = graphProcess.nodes();
        iteration += 1;
        for (auto currentNode : nodes){
            if (SHOW_DEBUG) {
                cout << "current node is:\t" << currentNode << endl;
            }
            // DEMON PART I --- get EgoMinusEgo Network
            network<std::string, double> currentEgoMinusEgo = graphProcess.EgoMinusEgoNetwork(currentNode);
            if (SHOW_DEBUG) {
                layer_info(currentEgoMinusEgo);
            }
            // DEMON PART II --- using LPA to get node and its neighbors label information
            LPA<std::string, double> lpa(currentEgoMinusEgo);
            std::map<std::string, std::string> node_label_map = lpa.label_results(); // 用 MAP 映射存储每一个点对应的标签信息
            graphProcess.update_label_list(node_label_map,iteration); // 更新当前 iteration 下的每一个节点的标签信息
        }
        if (SHOW_DEBUG) {
            cout << "\n\n ---------------------------------------------\n";
            show_Graph_process_Per_iteration_label_info(graphProcess);
            show_Graph_process_Per_iteration_label_info(graphProcess, iteration);
        }

        /// 4. 根据label的标签信息合并社团结果，并输出
        /** 注意:
         * 对于DEMON算法，只会有两次 iteration (= 0 & =1)
         * iteration = 0 --- 初始化当前网络
         * iteration = 1 --- 对每一个节点进行LPA之后的结果
         */
        std::vector<std::set<std::string>> communities = graphProcess.CurrentIterationCommunities(1, overlap_rate);
        showCommunities(communities);

        /// 5.  输出社团结果于文件中
        string output_filename = filename+".com";
        ofstream fout(output_filename);
        for (int i=0; i<communities.size(); i++){
            for (auto node: communities[i]){
                fout << node << " ";
            }
            fout << "\n";
        }
        fout.close();
    }
    return 0;
}

