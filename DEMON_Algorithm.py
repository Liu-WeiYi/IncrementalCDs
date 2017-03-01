# coding: utf-8

import sys, os, time

def DEMON(filename,overlap_rate = 0.1):
    # 功能:
    #   LPA 社团发现算法的Wrapper
    # 输入: 
    #   filename --- 需要进行社团发现的网络名称 
    # 输出:
    #   <输出到文件> filename.com --- 社团发现的结果
    os.system("./DEMON %s %s"%(filename,overlap_rate)) # --- 此为最简单的方案 ^_^



# JUST FOR TEST
filename = "./data/CollegeMsg/2004-10"
DEMON(filename)

# if __name__ == "__main__":
#     t = []
#     for i in range(4,11):
#         if i ==10:
#             filename = "./data/CollegeMsg/2004-10"
#         else:
#             filename = "./data/CollegeMsg/2004-0" + str(i)
#         start = time.time()
#         DEMON(filename)
#         t.append(time.time() - start)
#     for _ in t:
#         print(_)