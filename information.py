import numpy as np
import os

# 信息量计算
q = lambda x: -x*np.log2(x) if np.abs(x)>0.00001 else 0

##############################################
# Deal with normalized mutual information about nonoverlaping community
# coms1: approx com
# coms2: regular com

def nmi_non_olp(coms1, coms2):
    """
    基于标准方法计算两个非重叠社团的归一化互信息量，用于对比两个社团集合的相似程度
    :param coms1: 社团1集合
    :param coms2: 社团2集合
    :return: 归一化互信息值
    """
    # 各社团元素集合
    q = lambda x: -x*np.log2(x) if np.abs(x)>0.00001 else 0
    coms1_nodes = set()
    coms2_nodes = set()
    for com in coms1:
        coms1_nodes.update(com)
    for com in coms2:
        coms2_nodes.update(com)
    # 获取各个社团集合的总规模
    coms1_nodes_num = len(coms1_nodes)
    coms2_nodes_num = len(coms2_nodes)
    cross_nodes_num = len(coms1_nodes & coms2_nodes)
    # 计算 mutual information
    _H_C1 = 0.0
    _H_C2 = 0.0
    _H_C1_C2 = 0.0
    # calculate H(community1)
    for com in coms1:
        _p = len(com) / coms1_nodes_num
        _H_C1 += q(_p)
    # calculate H(community2)
    for com in coms2:
        _p = len(com) / coms2_nodes_num
        _H_C2 += q(_p)
    # calculate H(community1, community2)
    for com1 in coms1:
        for com2 in coms2:
            _n_com_1_2 = len(set(com1) & set(com2))
            if _n_com_1_2 is not 0:
                _p = _n_com_1_2 / cross_nodes_num
                _H_C1_C2 += q(_p)    
    _MI_2 = _H_C1 + _H_C2 - _H_C1_C2
    if abs(_H_C1 + _H_C2) < 0.0001:
        return 0.0
    else:
        return 2 * _MI_2 / (_H_C1 + _H_C2)


def LoadCommunityFile(com_file):
    '''Load the communities result'''
    # input: community detection file
    # output: dictionary, key is nodes, value is community
    com_content = open(com_file, encoding='utf-8').readlines()
    com_content = [list(map(int, _.split())) for _ in com_content]
    com_content = [_ for _ in com_content if _ != []]
    return com_content


def calc_info(file1, file2):
    coms1 = LoadCommunityFile(file1)
    coms2 = LoadCommunityFile(file2)
    print(nmi_non_olp(coms1, coms2))

if __name__ == "__main__":
    os.chdir('./data/Sx-stackoverflow/')
    approx_files = [_ for _ in os.listdir() if "_approx_merge_" in _]
    approx_files = approx_files[-3:]
    regular_files = [_ for _ in os.listdir() if "_regular_merge_" in _]
    regular_files = regular_files[-3:]
    zipped = list(zip(approx_files, regular_files))
    for i in zipped:
        calc_info(*i)