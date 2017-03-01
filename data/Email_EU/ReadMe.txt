网址:
http://snap.stanford.edu/data/email-Eu-core.html

Dataset information

The network was generated using email data from a large European research institution. 
We have anonymized information about all 
    incoming and outgoing email between members of the research institution. 
The e-mails only represent communication between institution members (the core), 
and the dataset does not contain incoming messages from or outgoing messages to the rest of the world. 
A directed edge (u, v, t) means that person u sent an e-mail to person v at time t. 
A separate edge is created for each recipient of the e-mail. 
We also have four sub-networks corresponding to the communication between members of four different departments at the institution. 
Node IDs in the sub-networks do not correspond to the same node ID in the entire network.

说明:
1. 该数据集合（共5个）是欧洲一个大型研究机构的邮件数据.
2. 该数据集合的作用是 在时间t时人A向人B发了一封邮件。
        2.1 Nodes: 网络的 节点 代表的是 人, 
        2.2 Edges: 网络的 边   代表的是 人和人之间的邮件。
                   那么就会形成 人src → 人dst 的一条"有向"边。 
3. 数据的形式: (u,v,t):
        3.1 u --- src
        3.2 v --- dst
        3.3 t --- 当前src 和 dst 之间产生连边时的时间戳(UNIX TimeStamp)
4. 注意的是，这些数据集合之间由于ID不一致，所以并不通用！

5个数据集合的介绍
1. email-Eu-core
    Nodes	986
    Temporal Edges	332334
    Edges in static graph	24929
    Time span	803 days
2. email-Eu-core-Dept1
    Nodes	309
    Temporal Edges	61046
    Edges in static graph	3031
    Time span	803 days
3. email-Eu-core-Dept2
    Nodes	162
    Temporal Edges	46772
    Edges in static graph	1772
    Time span	803 days
4. email-Eu-core-Dept3
    Nodes	89
    Temporal Edges	12216
    Edges in static graph	1506
    Time span	802 days
5. email-Eu-core-Dept4
    Nodes	142
    Temporal Edges	48141
    Edges in static graph	1375
    Time span	803 days

数据分析:
840 32 45308752
--> 表示人840 在 时间45308752 时联系了人32
--> 采用python中命令可以将UTC时间戳转换成当地时间:
    <值得注意一点，这里的时间格式并非标准UTC格式，因为这个数据秒数从0开始，表示从1970年1月1日，这个不大可能！>
    <不过，我们照样可以采用下面的转换，因为就算年份不对，但至少时间上的差距是一样的>
    ------------------------------------------------------------------
    In [1]: import time
    In [2]: time.strftime('%Y-%m-%dT%H:%M:%S',time.gmtime(1082444944))
    ------------------------------------------------------------------
    Out[2]: '1971-06-09T09:45:52' (表示1971年06月09日 09点45分52秒)
