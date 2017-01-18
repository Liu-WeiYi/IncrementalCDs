/**
 * purpose : 实现 单网络 network 模板类 & 多网络 MultiNetwork 模板类
 * @file graph.h
 * @brief 实现网络图的定义
 * Details.
 * 1. 实现单网络
 * 2. 实现多网络
 *
 * @author Liu Weiyi
 * @email weiyiliu@us.ibm.com
 * @version 1.0.0.0
 * @date 2016.12.25
 *----------------------------------------------------------------------------*
 *  Change History :                                                          *
 *  <Date>     | <Version> | <Author>       | <Description>                   *
 *----------------------------------------------------------------------------*
 *  2016/12/26 | 1.0.0.0   | Liu Weiyi      | Create file                     *
 *----------------------------------------------------------------------------*
 * */

#ifndef INCREMENTALMUTIPLEXDEMON_NETWORKS_H
#define INCREMENTALMUTIPLEXDEMON_NETWORKS_H

#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <string>

template <class Node_T, class Weight_T>
class network{
    /**
     * @brief network类 --- 有向加权网络
     * @author weiyiliu@us.ibm.com
     * @date 2016.12.26
     *
     * @param std::vector<Node_T> node_list               --- 节点 列表
     * @param std::map<Node_T,                                      // src
     *                 std::vector<                                 // 对应的边列表
     *                            std::map<Node_T,Weight_T>>        // dst, weight
     *                > edge_list                         --- 边列表
     *
     * @details
     *  1. 实现添加、删除 节点和边
     *
     * @example
     *  1. 创建网络
     *  network<std::string,double> layer
     *  2. 设置该网络名称
     *  layer.setName("Layer1");
     *  3. 添加节点
     *  layer.add_nodes_from(node_list);
     *  4. 添加边
     *  layer.add_edge("A","B",1.0, false); --- 添加无向边
     *  layer.add_edge("B","C",0.8, true);  --- 添加有向边
     *  5. 获取当前点的邻居关系
     *  layer.neighbor("A");
     *  6. 给出两个点, 判断这两个点之间的权重 如果这两个点之间没有连接，则权重为0!
     *  layer.get_weight("A","B");
     *
     */
private:
    /// 当前网络名称
    std::string name;
    /// 节点列表
    std::set<Node_T> node_list;
    /// 边, 采用当前节点像其它点的映射（为了查找速度快！）
    std::map<Node_T, std::vector<std::map<Node_T,Weight_T>>> edge_list;

public:
    /// 设置/获取当前网络的名称
    void setName(std::string);
    std::string Name();

    ///------------------------------------------------
    /// 操作节点
    ///  ------------------------------------------------
    void add_nodes_from(std::vector<Node_T> node_list);
    const std::set<Node_T> nodes();

    /// ------------------------------------------------
    ///  操作边
    /// ------------------------------------------------
    void add_edge(Node_T,Node_T,Weight_T,bool);
    const std::map<Node_T,std::vector<std::map<Node_T,Weight_T>>> edges();
    const std::vector<std::map<Node_T,Weight_T>> current_edges(Node_T);

    /// ------------------------------------------------
    ///  获取给定节点的邻居
    /// ------------------------------------------------
    std::set<Node_T> neighbors(Node_T);
    Weight_T get_weight(Node_T, Node_T);
};

template <class Node_T, class Weight_T>
class MultiNetwork{
    /**
     * @brief network类 --- 有向加权网络
     * @author weiyiliu@us.ibm.com
     * @date 2016.12.26
     *
     * @param std::vector<network>     layer_list         --- 所有层 列表
     * @param std::map<Node_T,
     *                  std::vector<             // vector[0] = CN
     *                      std::set<Node_T>>>   // vector[1] = GN
     *                                 neighbors          --- 当前网络中每一个节点的CN和GN信息
     * @param network<Node_T,Weight_T> mergedNetwork      --- 融合网络
     *
     * @details
     *  1. 实现存储所有网络的网络列表
     *
     * @example
     *  1. 存储所有层网络
     *  std::vector<network> layer_list;
     *
     */
private:
    std::vector<network<Node_T,Weight_T>>            layer_list;                    // 层列表
    std::map<Node_T,std::vector<std::set<Node_T>>>   neighbors;                     // 邻居关系
    std::set<Node_T>                                 node_list;                     // 所有的节点
    std::map<Node_T,double>                          node_overlap_rate;             // 每一个节点的overlap rate
    network<Node_T,Weight_T>                         Directed_Weighted_MergedGraph; // 由该多网络生成的Merged Network

    /// 获取该多网络的所有节点
    void __all_nodes();
    /// 获取每一个节点的 Central_Neighbors 和 Global_Neighbors
    void __get_CN_GN_Neighbors();


public:
    /// 创建该多网络
    MultiNetwork(std::vector<network<Node_T,Weight_T>> layers);
    /// 获取该多网络的所有网络
    std::vector<network<Node_T,Weight_T>> layers();
    /// 获取该多网络的所有节点集合
    std::set<Node_T> nodes();
    /// 获取该多网络的邻居关系
    std::map<Node_T,std::vector<std::set<Node_T>>> CN_GN();
    /// 获取每一个节点与之对应的Overlap Rate
    double overlap_rate(Node_T);
    /// 获取当前多网络的融合网络
    network<Node_T,Weight_T> merging_all_layers();



};


#include "networks.tpp"

#endif //INCREMENTALMUTIPLEXDEMON_NETWORKS_H
