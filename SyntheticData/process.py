# coding: utf-8
import os
import csv

data_path = "100000_全变化/"
save_file = "100000_全变化.csv"

all_time = []
file_list = os.listdir(data_path)
for file in file_list:
    with open(data_path+file,'r+') as ff:
        tmp = []
        for line in ff.readlines():
            change,time = line.strip().split()
            tmp.append(time)
        all_time.append(tmp)

with open(save_file,'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(all_time)

print('down')






