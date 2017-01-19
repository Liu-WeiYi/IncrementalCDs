//
// Created by weiyiliu on 12/30/16.
//

#include "Label_Propagation.h"

/**
 * @brief LPA方法的构造函数，直接进行 社团划分
 * @param net --- 传入的网络（加权有向网络）
 */
template <class Node_T, class Weight_T>
LPA<Node_T,Weight_T>::LPA(network<Node_T, Weight_T> net, bool WeightedFlag) {

    // 读入当前网络
    this->graph = net;
    // 读入所有点
    std::set<Node_T> nodes = this->graph.nodes();
    // 读取当前网络的所有边信息
//    std::map<Node_T,std::vector<std::map<Node_T,Weight_T>>> edge_info = this->graph.edges();
    // 给定最初的标签信息
    std::set<std::string> init_label_list;

    // 初始化每一个点的标签, 并存入标签列表中
    std::map<Node_T,std::string> node_label;
    for ( auto node_it=nodes.begin(); node_it!=nodes.end(); node_it++ ){
        Node_T node = *node_it;
        std::string label = node; // 保证这里node必须为String类型！
        node_label[node] = label;
        init_label_list.insert(label);
    }

    // 程序开始
    int count = 0; // 初始化循环的次数。。。
    bool  stop_flag = false; // 初始化停止条件

    while (stop_flag == false){
        count++ ;
        // 1. 找出影响当前节点最大的节点
        for (auto node_it=nodes.begin(); node_it!=nodes.end(); node_it++) {

            // 1.1 对每一个节点，更新标签信息
            Node_T src = *node_it;
            // 取出当前点的所有邻居
            std::set<Node_T> neighbors = this->graph.neighbors(src);
            // 首先需要判断当前点是否为孤立点
            // 如果是孤立点的话，后面就不需要进行计算了
            bool soloNodeFlag = false;
            if (neighbors.size() == 0){
                soloNodeFlag = true;
                node_label[src] = node_label[src]; // 孤立点的社团就是它自己
            }

            if (!soloNodeFlag) {
                // 处理带权重的网络
                if (WeightedFlag == true) {
                    // 初始化最大的权重
                    Weight_T maxWeight = (Weight_T) 0;
                    // 初始化 存储与当前节点之间权重最大的点的邻居
                    Node_T maxWeightNeighbor;
                    // 对每个邻居
                    for (auto neighbor_it = neighbors.begin(); neighbor_it != neighbors.end(); neighbor_it++) {
                        // 取出当前邻居
                        Node_T neighbor_dst = *neighbor_it;
                        // 用他们之间的权重判断对该节点src影响最大的邻居
                        Weight_T currentWeight = this->graph.get_weight(neighbor_dst, src);
                        if (currentWeight > maxWeight) {
                            maxWeight = currentWeight;
                            maxWeightNeighbor = neighbor_dst;
                        }
                    }
                    // 1.2 更新当前节点的label信息
                    node_label[src] = node_label[maxWeightNeighbor];
                }

                // 处理不带权重的网络
                if (WeightedFlag == false) {
                    // 初始化节点对应的标签信息
                    std::vector<std::string> labels;
                    std::set<std::string> unique_labels;
                    // 对每一个邻居
                    for (auto n_it : neighbors) {
                        // 取出该邻居的标签信息
                        std::string label = node_label[n_it];
                        // 存储当前节点对应的标签
                        labels.push_back(label);
                        unique_labels.insert(label);
                    }
                    if (unique_labels.size() == neighbors.size()) {
                        // 表示当前节点的每一个邻居的标签都不一样
                        // 则将第二个邻居的标签赋值给当前节点
                        if (labels.size() == 1){
                            node_label[src] = labels[0];
                        }
                        else {
                            node_label[src] = labels[1];
                        }
                    }
                    else {
                        // 如果不相等，就一定表示有重复的节点
                        // 初始化标签的最大个数
                        int maxLabelNumber = 0;
                        std::string currentLabel;
                        for (auto element : unique_labels) {
                            int number = (int) std::count(labels.begin(), labels.end(), element);
                            if (number > maxLabelNumber) {
                                currentLabel = element;
                                maxLabelNumber = number;
                            }
                        }
                        node_label[src] = currentLabel;
                    }
                }
            }
        }

        // 2. 获取当前所有节点的列表信息
        std::set<std::string> current_label_list;
        for (auto node_it = nodes.begin(); node_it != nodes.end(); node_it++){
            Node_T node = *node_it;
            current_label_list.insert(node_label[node]);
        }

        // 3. 判断当前的label和上一次的label信息是否相同
        if (current_label_list != init_label_list){
            init_label_list = current_label_list;
            //count += 1;
        } else if (current_label_list == init_label_list) {
            stop_flag = true;
            std::cout << "LPA total iteration time: " << count << std::endl;
        }

        // 4. 防止意外发生...
        // 当重复次数>1000次的时候，就停止计算
        if (count > 1000) {stop_flag = true;}
    }

    // 输出每一个节点的标签信息
    for (auto node_it = nodes.begin(); node_it != nodes.end(); node_it++){
        std::cout << "node "<< *node_it << ";\tlabel: " << node_label[*node_it] << std::endl;
    }

    // 将边的划分结果进行保存结果进行保存
    this->node_label_map = node_label;
}

/**
 * @brief 返回每一个节点对应的标签信息
 * @return node_label_map
 */
template <class Node_T, class Weight_T>
std::map<Node_T,std::string> LPA<Node_T,Weight_T>::label_results() {
    return this->node_label_map;
}

/**
 * @brief 返回当前节点对应的对应的标签信息
 * @return label
 */
template <class Node_T, class Weight_T>
std::string LPA<Node_T,Weight_T>::label_results(Node_T node) {
    return this->node_label_map[node];
}


template <class Node_T, class Weight_T>
std::vector<std::set<Node_T>> LPA<Node_T,Weight_T>::community() {
    std::vector<std::set<Node_T>> community; // 初始化这个社团

    std::map<std::string, std::set<Node_T>> label_2_nodes;

    // 1. 获取所有label
    for (auto label_it = this->node_label_map.begin();label_it != this->node_label_map.end(); label_it++){
        // 获取当前节点及其标签
        Node_T node = label_it->first;
        std::string label = label_it->second;

        // 判断当前label是否已经存在
        auto exit_it = label_2_nodes.find(label);
        if (exit_it != label_2_nodes.end()){
            // 表示找到了
            // 将当前节点加入map中
            label_2_nodes[label].insert(node);
        } else{
            // 表示没有找到
            // 创建当前键值
            std::set<Node_T> node_set;
            node_set.insert(node);
            label_2_nodes[label] = node_set;
        }
    }

    // 2. 获取社团
    for (auto it=label_2_nodes.begin(); it!=label_2_nodes.end(); it++){
        std::string label = it->first;
        community.push_back(label_2_nodes[label]);
    }

    return community;

}