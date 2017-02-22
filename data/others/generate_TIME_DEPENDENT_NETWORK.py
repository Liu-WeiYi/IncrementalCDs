# coding: utf-8

import pickle
import time
import networkx as nx
import matplotlib.pyplot as plt

ori_file = open("./data/Sx-superuser/sx-superuser.txt", 'r+')
all_time = set()
Time_dependent_networks = {}


count = 0

for line in ori_file.readlines():
    count += 1
    if count % 10000 == 0:
        print('processed %d lines'%count)
    # 提取所需要的时间等信息
    src, dst, utc = line.strip().split(' ')
    """
    1. 做以天为单位的
    """
    # current_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(int(utc))).split("T")[0]
    """
    2. 做以月为单位的
    """
    current_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(int(utc))).split("T")[0][:-3]
    
    # 提取"无向/无权"网络
    if current_date not in all_time:
        currentGraph = nx.Graph(name=current_date)
        currentGraph.add_edge(src, dst)
        Time_dependent_networks[current_date] = currentGraph
    else:
        currentGraph = Time_dependent_networks[current_date]
        currentGraph.add_edge(src, dst)
    # 添加时间信息
    all_time.add(current_date)

ori_file.close()

# 保存获取到的所有文件
"""
1. 以天作为单位
"""
# pickle.dump(Time_dependent_networks, open("Time_dependent_networks.pickle", 'wb'))
# pickle.dump(all_time, open("all_time.pickle", 'wb'))
"""
2. 以月作为单位
"""
pickle.dump(Time_dependent_networks, open("Time_dependent_networks_Month.pickle", 'wb'))
pickle.dump(all_time, open("all_time_Month.pickle", 'wb'))

dta = pickle.load(open("Time_dependent_networks_Month.pickle", 'rb'))
for i, j in dta.items():
    with open(i, "w+") as g:
        for e in j.edges():
            n1, n2 = e
            g.write(str(n1) + " " + str(n2) + "\n")


# 画图 同时将每一个时间段的edgeList文件存入到磁盘上
for net in sorted(all_time):
    network = Time_dependent_networks[net]
    print(network.name)
    name = network.name
    nx.draw(network)
    """
    1. 以天作为单位
    """
    # plt.savefig("all_Day/%s.png"%name)
    # with open('all_Day/%s'%name, "w+") as f:
    #     for edge in network.edges():
    #         (src, dst) = edge
    #         f.write(str(src)+" "+str(dst)+"\n")
    """
    2. 以月作为单位
    """
    plt.savefig("all_Month/%s.png"%name)
    with open('all_Month/%s'%name, "w+") as f:
        for edge in network.edges():
            (src, dst) = edge
            f.write(str(src)+" "+str(dst)+"\n")
    plt.clf()

# # 存储每一个网络的节点大小，画图展示一下
# Number = []
# X = []
# Count = 0

# for net in sorted(all_time):
#     X.append(Count+4)
#     Number.append(len(Time_dependent_networks[net].nodes()))
#     Count += 1

# plt.plot(X, Number)
# plt.show()
