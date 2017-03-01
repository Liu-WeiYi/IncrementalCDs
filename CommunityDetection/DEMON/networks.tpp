//
// Created by weiyiliu on 12/26/16.
//

#include "networks.h"

// ------------------------------------------------------------------------
// network类 的实现
// ------------------------------------------------------------------------
/**
 * @brief 设置当前网络名称
 * @param name
 */
template <class Node_T, class Weight_T>
void network<Node_T,Weight_T>::setName(std::string name) {
    this->name = name;
}
/**
 * @brief 返回当前网络的名称
 * @return name
 */
template <class Node_T, class Weight_T>
std::string network<Node_T,Weight_T>::Name() {
    return this->name;
}
/**
 * @brief 设置当前网络的节点列表
 * @param node_list
 */
template <class Node_T, class Weight_T>
void network<Node_T,Weight_T>::add_nodes_from(std::vector<Node_T> node_list) {
    // 遍历该节点列表，添加节点
    for (int i = 0; i < node_list.size(); ++i) {
        this->node_list.insert(node_list[i]);
    }
}
/**
 * @brief 返回当前网络的节点列表
 * @return node_list
 */
template <class Node_T, class Weight_T>
const std::set<Node_T> network<Node_T,Weight_T>::nodes() {
    return this->node_list;
}
/**
 * @brief 添加边
 * @param src         --- 源节点
 * @param dst         --- 目的节点
 * @param weight      --- 权重
 * @param direct_flag --- 该条边是否为有向边 其中 false 代表无向边
 */
template <class Node_T, class Weight_T>
void network<Node_T,Weight_T>::add_edge(Node_T src, Node_T dst, Weight_T weight, bool direct_flag) {
    // 首先构成目的节点及其权重的map
    std::map<Node_T,Weight_T> dst_weight;
    dst_weight[dst] = weight;

    // 之后判断当前源节点是否在edge_list中
    auto it = this->edge_list.find(src);

    if (it != this->edge_list.end()){
        // 表明当前点已存在于EdgeList当中了
        // 因此下面只需要将该条边添加到该节点原有的边列表中即可
        this->edge_list[src].push_back(dst_weight);
    } else {
        // 表明当前点不存在于EdgeList中
        // 下面需要创建该节点到边列表的映射
        std::vector<std::map<Node_T,Weight_T>> src_map;
        src_map.push_back(dst_weight);
        this->edge_list[src] = src_map;
    }

    // 当前边若为无向边时，还应添加dst---src的形式
    if (direct_flag == false) {
        // 首先构成目的节点及其权重的map
        std::map<Node_T,Weight_T> src_weight;
        src_weight[src] = weight;

        // 之后判断当前源节点是否在edge_list中
        auto it = this->edge_list.find(dst);

        if (it != this->edge_list.end()){
            // 表明当前点已存在于EdgeList当中了
            // 因此下面只需要将该条边添加到该节点原有的边列表中即可
            this->edge_list[dst].push_back(src_weight);
        } else {
            // 表明当前点不存在于EdgeList中
            // 下面需要创建该节点到边列表的映射
            std::vector<std::map<Node_T,Weight_T>> dst_map;
            dst_map.push_back(src_weight);
            this->edge_list[dst] = dst_map;
        }
    }
}
/**
 * @brief 返回当前网络的所有边
 * @return edge_list
 */
template <class Node_T, class Weight_T>
const std::map<Node_T,std::vector<std::map<Node_T,Weight_T>>> network<Node_T,Weight_T>::edges() {
    return this->edge_list;
}
/**
 * @brief 返回指定的当前节点的边
 * @param node
 * @return edges
 */
template <class Node_T, class Weight_T>
const std::vector<std::map<Node_T,Weight_T>> network<Node_T,Weight_T>::current_edges(Node_T node) {
    return this->edge_list[node];
}

/**
 * @brief 给定某个点，获取这个点在当前网络中的所有邻居
 * @param node
 * @return neighbors 集合
 */
template <class Node_T, class Weight_T>
std::set<Node_T> network<Node_T,Weight_T>::neighbors(Node_T node) {
    std::set<Node_T> neighbors;
    for (int i = 0; i < this->edge_list[node].size(); ++i) {
        std::vector<std::map<Node_T,Weight_T>> currentNeighbors = edge_list[node];
        for (int j = 0; j < currentNeighbors.size(); ++j) {
            std::map<Node_T,Weight_T> neighbor_weight_map = currentNeighbors[j];
            auto it = neighbor_weight_map.begin();
            neighbors.insert(it->first);
        }
    }
    return neighbors;
}
/**
 * @brief 根据给定的两个点，返回这两个点之间的权重
 * @param src --- 点1
 * @param dst --- 点2
 * @return weight (当返回为0的时候，表示没有找到！)
 */
template <class Node_T, class Weight_T>
Weight_T network<Node_T,Weight_T>::get_weight(Node_T src, Node_T dst) {
    Weight_T weight = (Weight_T)0; // 设置初始值就是0哈

    std::vector<std::map<Node_T,Weight_T>> dst_info_list = this->edge_list[src];
    for (int i = 0; i < dst_info_list.size(); ++i) {
        std::map<Node_T,Weight_T> dst_info_map = dst_info_list[i];
        auto dst_it = dst_info_map.begin();
        if (dst_it->first == dst) {
            weight = dst_it->second;
            break;
        }
    }
    return weight;

}


// ------------------------------------------------------------------------
// MultiNetwork类 的实现
// ------------------------------------------------------------------------

template <class Node_T, class Weight_T>
MultiNetwork<Node_T,Weight_T>::MultiNetwork(std::vector<network<Node_T, Weight_T>> layers) {
    // 获取初始化每一个网络
    this->layer_list = layers;
    // 获取当前多网络中的所有节点
    this->__all_nodes();
    // 获取当前多网络中的每一个节点的GN和CN
    // 同时获取这些点的Overlap Rate
    this->__get_CN_GN_Neighbors();
}


/**
 * @brief 获取当前多网络下的每一个网络
 * @return layer_list
 */
template <class Node_T, class Weight_T>
std::vector<network<Node_T,Weight_T>> MultiNetwork<Node_T,Weight_T>::layers() {
    return this->layer_list;
}
/**
 * @brief 构建当前多网络中的所有节点集合
 */
template <class Node_T, class Weight_T>
void MultiNetwork<Node_T,Weight_T>::__all_nodes() {
    for (int i = 0; i < this->layer_list.size(); ++i) {
        network<Node_T, Weight_T> currentLayer = layer_list[i];
        std::set<Node_T>          currentNodes = currentLayer.nodes();
        for (auto node_it = currentNodes.begin(); node_it != currentNodes.end(); node_it++) {
            this->node_list.insert(*node_it);
        }
    }
}
template <class Node_T, class Weight_T>
std::set<Node_T> MultiNetwork<Node_T,Weight_T>::nodes() {
    return  this->node_list;
}


/**
 * @brief 构建当前网络中的每一个节点的CN和GN邻居关系, 同时获得所有点的Overlap_Rate
 */
template <class Node_T, class Weight_T>
void MultiNetwork<Node_T,Weight_T>::__get_CN_GN_Neighbors() {

    for (auto node_it=this->node_list.begin(); node_it!=this->node_list.end(); node_it++){
        // 取出当前节点
        Node_T node = *node_it;
        // 初始化当前节点在所有网络中的邻居、GN、CN
        std::vector<Node_T> rawNeighbor;
        std::set<Node_T>    GN;
        std::set<Node_T>    CN;

        // 获取当前节点的GN
        for (int i = 0; i < this->layer_list.size(); ++i) {
            // 对于每一个网络
            network<Node_T, Weight_T> currentLayer = layer_list[i];
            // 取出当前网络下该节点的所有邻居
            std::set<Node_T> neighbors = currentLayer.neighbors(node);
            // 放入rawNeighbor和GN中
            for (auto it = neighbors.begin(); it != neighbors.end(); it++) {
                rawNeighbor.push_back(*it);
                GN.insert(*it);
            }
        }

        // 根据上一步找出的rawNeighbor和GN，找出当前节点的CN关系
        for (auto it = GN.begin(); it!=GN.end(); it++){
            Node_T CN_Neighbor = *it;
            int num = std::count(rawNeighbor.begin(),rawNeighbor.end(),CN_Neighbor);
            if (num == this->layer_list.size()){
                CN.insert(CN_Neighbor);
            }
        }

        // 生成当前节点的CN和GN关系，并存储在neighbor信息中
        std::vector<std::set<Node_T>> CN_GN;
        CN_GN.push_back(CN);
        CN_GN.push_back(GN);
        this->neighbors[node] = CN_GN;

        /// 获取当前节点的Overlap Rate
        this->node_overlap_rate[node] = (double)CN.size()/(double)GN.size();
    }
}
/**
 * 获取所有节点的CN和GN信息
 * @return neighbors
 */
template <class Node_T, class Weight_T>
std::map<Node_T,std::vector<std::set<Node_T>>> MultiNetwork<Node_T,Weight_T>::CN_GN() {
    return this->neighbors;
}
/**
 * @brief 获取当前节点的Overlap Rate
 * @param node
 * @return overlap rate
 */
template <class Node_T, class Weight_T>
double MultiNetwork<Node_T,Weight_T>::overlap_rate(Node_T node) {
    return this->node_overlap_rate[node];
}
/**
 * @brief 获取当前多网络的 📮有向加权融合网络
 * @details 每条边"e=src---dst"的权重 We = O(src,dst)+f(e)
 *
 *          其中:
 *             + O(src,dst)  --->  0.5*(Overlap_rate(src) + Overlap_rate(dst));
 *             + f(e):       --->  为当前边的函数, 可以有以下几种求取形式, 且e_l表示在第l层下该边e的权重:
 *                           -------> 1. f1(e) = mean[ ∑weight(e_l) ] ; --- 所有层的边权重之和的平均
 *                           -------> 2. f2(e) = max[ weight(e_l) ] ;   --- 最大的权重
 *
 *          p.s. f(e) 的两种方法存在的问题:
 *                           ---> 对于f1(e): 可能会把最显著的权重忽略掉！
 *                                          但是却能反应 两节点之间的平均连接情况, 去除可能存在的噪音
 *                           ---> 对于f2(e): 会忽略边的连接次数！
 *                                          但是却能反应 两节点之间的最大的连接情况, 与f1(e)正好相反!
 *
 *          p.s. We 中间的符号应该为 + 号，而非 * 号. 因为*号会导致在权重丢失的情况
 *                           ---> 比如 对于 "G" 和 "H" 两个节点，
 *                                -------> 如果: Overlap_rate(G) = 0; Overlap_rate(H) = 0;
 *                                -------> 那么: O(G,H) = 0
 *                                -------> 导致: We = 0
 *                                -------> 这与本身之间不存在连接的两点就无法区分了!
 *
 * @return Directed_Weighted_MergedGraph
 */
template <class Node_T, class Weight_T>
network<Node_T,Weight_T> MultiNetwork<Node_T,Weight_T>::merging_all_layers() {
    // 0. 给定该融合网络的名称
    this->Directed_Weighted_MergedGraph.setName("Directed Weighted MergedGraph");
    //1. 先添加这个网络的所有节点(历史遗留问题。。。graph中的点是Vector形式的！)
    std::vector<Node_T> nodes;
    for (auto node_it = this->node_list.begin(); node_it != this->node_list.end(); node_it++){
        nodes.push_back(*node_it);
    }
    this->Directed_Weighted_MergedGraph.add_nodes_from(nodes);

    // 2. 对每条边，更新这条边的Weight信息
    for (int i = 0; i < nodes.size(); ++i) {
        // 2.0 获取当前 源节点
        Node_T src = nodes[i];
        std::vector<std::set<Node_T>> CN_GN_info = this->neighbors[src];

        // 2.1 获取当前节点在多网络中的所有邻居关系
        std::set<Node_T> GN = CN_GN_info[1];
        // 2.2 对于每一条连边
        for (auto dst_it = GN.begin(); dst_it != GN.end(); dst_it++){
            // 2.2.0 获取当前目的节点
            Node_T dst = *dst_it;
            // 2.2.1 获取源节点和目的节点的Overlap Rate --- 计算 O(src,dst)
            double src_overlap_rate = this->node_overlap_rate[src];
            double dst_overlap_rate = this->node_overlap_rate[dst];
            double O_src_dst = 0.5*(src_overlap_rate + dst_overlap_rate);
            // 2.2.2 获取源节点和目的节点在每一个网络下的权重之和 --- 计算f1(e)
            double total_weight = 0.0; // 初始化总权重
            int count = 0;            // 用来记录当前边出现的次数
            for (int j = 0; j < this->layer_list.size(); ++j) {
                // 取出当前网络
                network<Node_T,Weight_T> currentLayer = layer_list[j];
                // 提取该条边在当前网络下的权重
                double currentWeight = currentLayer.get_weight(src,dst);
                total_weight += currentWeight;
                if (currentWeight != 0){ count += 1; } // 当前网络中存在这条边，则次数加1
            }
            // 计算 f1(e)
            double f_1_e;
            if (count != 0){ f_1_e = total_weight/count; }else{ f_1_e = 0.0 ;}

            // 2.3 计算当前源节点src和目的节点dst之间的weight --- 计算We
            double We = O_src_dst+f_1_e;

            // 2.4 计算当前边的权重，并将这条边添加至融合网络中
            if (count != 0){ // count = 0 表示在多网络中都没有这条边呢!
                // 由于每一层的网络都是有向的，因此这里direct_flag = true 恒成立!
                this->Directed_Weighted_MergedGraph.add_edge(src,dst,We,true);
            }
        }
    }

    return this->Directed_Weighted_MergedGraph;
}

