# coding: utf-8

import sys, os

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