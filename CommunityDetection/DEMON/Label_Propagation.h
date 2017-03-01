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
 * @date 2016.12.30
 *----------------------------------------------------------------------------*
 *  Change History :                                                          *
 *  <Date>     | <Version> | <Author>       | <Description>                   *
 *----------------------------------------------------------------------------*
 *  2016/12/30 | 1.0.0.0   | Liu Weiyi      | Create file                     *
 *----------------------------------------------------------------------------*
 * */

#ifndef INCREMENTALMUTIPLEXDEMON_LABEL_PROPAGATION_H
#define INCREMENTALMUTIPLEXDEMON_LABEL_PROPAGATION_H

#include "networks.h"

template <class Node_T, class Weight_T>
class LPA{
    /**
     * @brief 标签传播算法 Label Propagation Algorithm --- LPA
     * @author weiyiliu@us.ibm.com
     * @date 2016.12.30
     *
     * @param network<Node_T,Weight_T> graph                  --- 需要进行社团发现的有向加权网络
     * @param std::map<Node_T,std::string> node_label_map     --- 每个点对应的标签
     *
     * @example
     *  1. 进行社团发现
     *  LPA<std::string,double> lpa(Directed_Weighted_MergedGraph);
     *  2. 输出社团信息
     *  std::vector<std::set<std::string>> communities = lpa.community();
     *
     */
private:
    // 需要进行社团发现的网络
    network<Node_T,Weight_T> graph;
    // 每一个节点对应的label
    std::map<Node_T,std::string> node_label_map;

public:
    /// 直接在构造函数中就可以进行社团发现了！
    LPA(network<Node_T,Weight_T> net,bool WeightedFlag = true);
    /// 获取每一个节点的标签信息
    std::map<Node_T,std::string> label_results();
    /// 获取当前节点的标签信息
    std::string label_results(Node_T);
    /// 当前网络的社团信息
    std::vector<std::set<Node_T>> community();
};

#include "Label_Propagation.tpp"
#endif //INCREMENTALMUTIPLEXDEMON_LABEL_PROPAGATION_H
