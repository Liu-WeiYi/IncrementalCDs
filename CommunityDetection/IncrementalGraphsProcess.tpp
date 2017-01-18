//
// Created by weiyiliu on 12/29/16.
//

#include <cmath>
#include "IncrementalGraphsProcess.h"

/**
 * 返回当前需要处理网络的所有节点
 * @return node_list
 */
template <class Node_T, class Weight_T>
std::set<Node_T> GraphProcess<Node_T,Weight_T>::nodes() {
    return this->Graph.nodes();
}



/**
 * 设置需要处理的网络
 * @param g
 */
template <class Node_T, class Weight_T>
void GraphProcess<Node_T,Weight_T>::setGraph(network<Node_T, Weight_T> g) {
    this->Graph = g;
}

/**
 * @brief 初始化当前网络中的所有节点的标签信息
 * @param iteration --- 第0次迭代
 */
template <class Node_T, class Weight_T>
void GraphProcess<Node_T,Weight_T>::InitLabels(int iteration) {
    std::set<Node_T> node_list = this->Graph.nodes();
    for (auto node_it = node_list.begin(); node_it != node_list.end(); node_it++){
        // 对于每一个节点
        Node_T node = *node_it;
        //构建当前节点的标签集合
        std::map<int, std::set<std::string>> current_node_label_set;
        current_node_label_set[iteration].insert(node);
        //更新图中当前节点的标签信息
        this->Node_Label_Info[node]=current_node_label_set;
    }
}

/**
 * 返回当前节点的标签列表信息
 * @param node      --- 当前节点
 * @param iteration --- 当前迭代轮数
 * @return
 */
template <class Node_T, class Weight_T>
std::set<std::string> GraphProcess<Node_T,Weight_T>::label_list(Node_T node, int iteration) {
    return this->Node_Label_Info[node][iteration];
}

/**
 * 设置当前的重叠率
 * @param overlapRate
 */
template <class Node_T, class Weight_T>
void GraphProcess<Node_T,Weight_T>::set_overlap_rate(double overlapRate) {
    this->overlapRate = overlapRate;
}

/**
 * @brief 给出当前层下的社团信息
 * @details 在DEMON算法中, 最后一步判断社团该不该合并的时候，采用的是两两社团进行比较
 *          而这存在一个问题，因为他是每一个节点都对应了一堆社团，所以假设网络中的节点个数为N的话，社团的个数就至少≥N.
 *          因此两两比较的时间会很慢！因为这样会导致时间复杂度至少为: O(N*N)
 *          所以在这里我更倾向于用节点的LABEL当节点的标签信息，并比较哪些标签信息会在一起
 *          这里首先构建标签→标签的映射 label_2_label, 我分两步走:
 *          1(外层). 提取所有节点的标签信息
 *              2(内层). 根据第1步生成的节点的标签信息, 对 label_2_label 中的每一个标签信息(即 label_2_label 的 KEY)
 *                      --> 1. 判断当前标签信息 和 KEY的标签信息的重叠率
 *                      --> 2. 如果都不重叠，则将该标签信息加入
 *          综上所述，由于从节点A-->节点N(共|N|个节点), 每次迭代的规律有
 *
 *          节点: A, B, C, D, ... ,   N
 *               |  |  |  |   ...    |
 *          查找: 0, 1, 2, 3, ... , |N|-1
 *
 *          因此我的方法的时间复杂度为O(0+1+2+...+|N|-1)=O(0.5*N*(N-1))
 *
 * @param itertaion --- 当前更新的轮数
 * @param RATE      --- 期望重叠的概率
 *
 */
template <class Node_T, class Weight_T>
std::vector<std::set<Node_T>> GraphProcess<Node_T,Weight_T>::CurrentIterationCommunities(int itertaion,double RATE) {

    // 初始化
    std::map<std::set<std::string>, std::set<Node_T>> label_2_label; // 1. 构建 label_2_label
    std::vector<std::set<Node_T>> communities; // 2. communities
    this->set_overlap_rate(RATE);

    // 1. 构建 label_2_label
    for (auto it=this->Node_Label_Info.begin(); it!=this->Node_Label_Info.end(); it++) {
        //取出当前节点
        Node_T currentNode = it->first;
        // 取出当前节点在当前iteration轮中的标签集合
        std::set<std::string> current_labels = it->second[itertaion];

        // 对当前标签进行排序
//        std::sort(current_labels.begin(),current_labels.end()); ---> SORT函数不能对STRING进行排序！真奇怪！

        // 设定当前节点的标签是否被找到的FLAG
        bool exited_flag = false; // 默认没有找到
        // 循环看看呗。。。
        for (auto label_find = label_2_label.begin(); label_find != label_2_label.end(); label_find++){
            std::set<std::string> exit_labels = label_find->first;
            std::set<std::string> overlap_labels;
            // 求交集
            std::set_intersection(current_labels.begin(),current_labels.end(),
                                  exit_labels.begin(),exit_labels.end(),
                                  std::inserter(overlap_labels,overlap_labels.begin()));
            // 求重叠率
            double overlap = (double)overlap_labels.size()/std::max(exit_labels.size(),current_labels.size());
            //当重叠率大于设定门限时，将该节点加入社团中
            if (overlap > this->overlapRate) {
                label_2_label[exit_labels].insert(currentNode);
                exited_flag = true; // 设置该标签为找到了呢
            }
        }
        // 循环了一圈，表示屁都没有找到。。。
        if (exited_flag == false){
            //将当前节点加入label_2_label中
            label_2_label[current_labels].insert(currentNode);
        }
    }

    // 2. 放入社团
    for (auto com_it=label_2_label.begin();com_it!=label_2_label.end();com_it++){
        std::set<Node_T> currentCom = com_it->second;
        communities.push_back(currentCom);
    }
    return communities;
}




//====================================================================================
/// 和DEMON有关的算法
//====================================================================================
/**
 * 获取当前节点的 EgoMinusEgo 网络
 * @param 当前节点 node
 * @return 当前节点所构成的 有向加权的 EgoMinusEgo 网络--- 返回一个Network对象
 */
template <class Node_T, class Weight_T>
network<Node_T,Weight_T> GraphProcess<Node_T,Weight_T>::EgoMinusEgoNetwork(Node_T node) {

    // 0. 创建当前EgoMinusEgo网络
    network<Node_T,Weight_T> EgoMinusEgo;
    EgoMinusEgo.setName("EgoMinusEgo");

    // 1. 获取当前网络的邻居列表
    std::set<Node_T> neighbors = this->Graph.neighbors(node);

    // 2. 添加EgoMinusEgo网络的节点 --- 历史遗留问题。。。将set转换成vector
    std::vector<Node_T> neighbors_vector;
    for (auto it = neighbors.begin(); it!=neighbors.end(); it++){ neighbors_vector.push_back(*it);}
    EgoMinusEgo.add_nodes_from(neighbors_vector);

    for (auto neighbor_it = neighbors.begin(); neighbor_it!=neighbors.end(); neighbor_it++){
        // 取出当前节点, 作为源节点
        Node_T neighbor_src = *neighbor_it;
        // 取出当前节点所对应的所有边
        std::vector<std::map<Node_T,Weight_T>> edges = this->Graph.current_edges(neighbor_src);
        // 遍历每一个源节点对应的边
        for (int i = 0; i < edges.size(); ++i) {
            std::map<Node_T,Weight_T> dst_weight_map = edges[i];
            auto map_it = dst_weight_map.begin();
            // 取出目的节点
            Node_T dst = map_it->first;
            // 取出源节点和目标节点之间的权重
            Weight_T weight = map_it->second;
            //除去源节点以及不在neighbor中的节点们
            if (dst != node){
                auto dst_it = neighbors.find(dst);
                if (dst_it != neighbors.end()) {
                    // 表明找到了当前节点
    // 3. 添加边关系
                    EgoMinusEgo.add_edge(neighbor_src,dst,weight, true);
                }
            }
        }
    }
    return EgoMinusEgo;
}

/**
 * @brief 更新当前节点的 label 信息
 * @param node_label_map  --- 当前节点及其周围点的标签信息
 * @param iteration  --- 当前更新的轮数
 */
template <class Node_T, class Weight_T>
void GraphProcess<Node_T,Weight_T>::update_label_list(std::map<Node_T, std::string> node_label_map, int iteration) {
    //this->Node_Label_Info[node][iteration].insert(node_label_map[node]);
    for (auto node_it = node_label_map.begin(); node_it!=node_label_map.end(); node_it++){
        // 取出当前节点 及其 标签
        Node_T currentNode = node_it->first;
        std::string label = node_it->second;
        // 更新当前节点的标签信息
        this->Node_Label_Info[currentNode][iteration].insert(label);
    }
}






