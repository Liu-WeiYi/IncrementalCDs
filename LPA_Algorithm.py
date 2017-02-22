# coding: utf-8

import sys, os
import re, time
from glob import glob

def LPA(filename):
    # 功能:
    #   LPA 社团发现算法的Wrapper
    # 输入: 
    #   filename --- 需要进行社团发现的网络名称 
    # 输出:
    #   <输出到文件> filename.com --- 社团发现的结果
    os.system("./LPA %s"%filename) # --- 此为最简单的方案 ^_^



# JUST FOR TEST
# filename = "2004-04"
# LPA(filename)

# file_dir = "./data/Sx-superuser/"
# if __name__ == "__main__":
#     t = []
#     files = [_ for _ in glob(os.path.join(file_dir, '*')) if re.search('^\d{4}-\d{2}$', _.split('/')[-1])]
#     for i in files:
#         start = time.time()
#         LPA(i)
#         t.append(time.time() - start)
#     for _ in t:
#         print(_)