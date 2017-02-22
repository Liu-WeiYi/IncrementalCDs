# coding: utf-8

import sys, os, time, re
from glob import glob

def DEMON(filename,overlap_rate = 0.1):
    # 功能:
    #   LPA 社团发现算法的Wrapper
    # 输入: 
    #   filename --- 需要进行社团发现的网络名称 
    # 输出:
    #   <输出到文件> filename.com --- 社团发现的结果
    os.system("./DEMON %s %s"%(filename,overlap_rate)) # --- 此为最简单的方案 ^_^



# JUST FOR TEST
# filename = "./data/CollegeMsg/2004-10"
# DEMON(filename)

# file_dir = "./data/Sx-superuser/"
# if __name__ == "__main__":
#     t = []
#     files = [_ for _ in glob(os.path.join(file_dir, '*')) if re.search('^\d{4}-\d{2}$', _.split('/')[-1])]
#     for i in files:
#         start = time.time()
#         DEMON(i)
#         t.append(time.time() - start)
#     for _ in t:
#         print(_)