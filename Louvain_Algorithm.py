# coding: utf-8

import sys, os, time, re
from glob import glob

def Louvain(filename):
    # 功能:
    #   Louvain 社团发现算法的Wrapper
    # 输入: 
    #   filename --- 需要进行社团发现的网络名称 
    # 输出:
    #   <输出到文件> filename.com --- 社团发现的结果
    os.system("./Louvain %s"%(filename)) # --- 此为最简单的方案 ^_^



# JUST FOR TEST
#filename = "2004-04"
#Louvain(filename)

file_dir = "./data/Email_EU_daily/"
if __name__ == "__main__":
    t = []
    files = [_ for _ in glob(os.path.join(file_dir, '*')) if re.search('^\d{4}-\d{2}-\d{2}$', _.split('/')[-1])]
    for i in files:
        start = time.time()
        Louvain(i)
        t.append(time.time() - start)
    for _ in t:
        print(_)