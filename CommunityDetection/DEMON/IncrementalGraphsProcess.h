/**
 * purpose : 实现 网络增量算法
 * @file IncrementalGraphsProcess.h
 * @brief 多网络 → 融合后的 有向加权网络 增量算法
 * Details.
 * #################################################################################
 * 1. 初始化:     对每一个点，赋予该点一个独一无二的标签信息（一个点具有一个标签）
 *
 * 2. 局部更新:   对每一个点，局部更新该点 及其 邻居 的标签信息
 *                        更新方式： 1. △Q                 --- modularity maximum
 *                                 2. Label Propargation  --- DEMON related
 *                                 ...
 *
 * 3. 重复第2步，直至 标签信息 达到稳定 --- Louvain Related! (Demon will pass this step)
 *
 * 4. 标签融合:   对每一组具有相同标签的节点，给一个新的标签用来代表
 *
 * 5. 节点融合:   根据第4步结论，将具有相同标签的节点簇融合成为一个节点，并最终生成一个新的网络
 *
 * 6. 重复第2步~第6步，直至所有节点被融合成一个节点为止
 * #################################################################################
 *
 * @author Liu Weiyi
 * @email weiyiliu@us.ibm.com
 * @version 1.0.0.0
 * @date 2016.12.29
 *----------------------------------------------------------------------------*
 *  Change History :                                                          *
 *  <Date>     | <Version> | <Author>       | <Description>                   *
 *----------------------------------------------------------------------------*
 *  2016/12/20 | 1.0.0.0   | Liu Weiyi      | Create file                     *
 *----------------------------------------------------------------------------*
 * */

#ifndef INCREMENTALMUTIPLEXDEMON_INCREMENTALGRAPHSPROCESS_H
#define INCREMENTALMUTIPLEXDEMON_INCREMENTALGRAPHSPROCESS_H

#include "networks.h"
#include "Label_Propagation.h"

template <class Node_T, class Weight_T>
class GraphProcess{
    /**
     * @brief network类 --- 有向加权网络
     * @author weiyiliu@us.ibm.com
     * @date 2016.12.29
     *
     * @param network<Node_T,Weight_T>      Graph              --- 传入的有向加权网络
     *
     * @param std::map<Node_T,       // 对于每一个节点
     *             std::map<int,     // 第 int 轮的标签
     *                  std::set<   //  当前节点 NODE_T 在 该轮 的标签
     *                       std::string>>> Node_label_Info   --- 每一个节点的标签列表
     *
     * @param double                        overlapRate       --- 重叠率
     *
     * @details --- 见开头
     *
     * @example
     *  1. 初始化该加权网络
     *  GraphProcess<std::string,double> graph(Directed_Weighted_Network);
     *  2. 初始化该加权网络中每一个节点的标签信息
     *  graph.InitLabels()
     *
     *
     */

private:
    network<Node_T,Weight_T> Graph;
    std::map<Node_T,std::map<int, std::set<std::string>>> Node_Label_Info;
    double overlapRate=1;


public:
    /// 输出一些graph所需的信息
    std::set<Node_T> nodes();

    /// 读入该加权有向网络
    void setGraph(network<Node_T,Weight_T>);

    /// 初始化每一个点的Label信息
    void InitLabels(int);
    /// 给定第ITERATION轮, 输出当前轮下的每一个点的 Label 信息
    std::set<std::string> label_list(Node_T,int);

    /// 设置当前overlap rate
    void set_overlap_rate(double);

    /// 局部更新 --- 表明下面的所有函数的接受值都应该只是一个点
    /// 1. DEMON Related
    network<Node_T,Weight_T> EgoMinusEgoNetwork(Node_T);
    /// 2. 根据社团发现的最优化函数所得出的当前点的社团信息, 更新节点标签信息
    /// 其中,
    /// std::map<Node_T,std::string> 表示根据当前社团发现的最优化函数，所得当前节点及其邻居们的标签信息
    /// int 当前迭代进行的轮数
    /// 主要更新的变量 --- Node_label_Info
    void update_label_list(std::map<Node_T,std::string>,int);

    /// 社团输出 ---
    /// 根据节点的标签，输出当前社团信息
    /// int --- 当前层
    std::vector<std::set<Node_T>> CurrentIterationCommunities(int,double);


};

#include "IncrementalGraphsProcess.tpp"

#endif //INCREMENTALMUTIPLEXDEMON_INCREMENTALGRAPHSPROCESS_H
