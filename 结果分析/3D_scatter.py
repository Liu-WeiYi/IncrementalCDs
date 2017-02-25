# coding: utf-8

import scipy.io as sio  
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 

all_files_name = ['Email_EU', 'CollegeMsg', 'Sx-mathoverflow', 'Sx-superuser', 'Sx-stackoverflow']


for filename in all_files_name:
    number = []
    changeAvg = []
    increaseAvg = []

    fig = plt.figure(filename)
    with open("Datasets/%s"%filename,'r+') as file:
        for line in file.readlines():
            tmp = line.strip().split()
            number.append(float(tmp[0]))
            changeAvg.append(float(tmp[1]))
            increaseAvg.append(float(tmp[2]))

    ax = fig.add_subplot(111, projection='3d')
    # ax = plt.subplot(figure_number, projection='3d')
    ax.set_title(filename)

    for i in range(len(number)):
        if increaseAvg[i] < 0:
            c = 'w'
            m = '*'
        else:
            c = 'b'
            m = 'o'
        ax.scatter(number[i],changeAvg[i],increaseAvg[i],c=c,marker=m)

    ax.set_xlabel("Time Stamp")
    ax.set_ylabel("Change Avg")
    ax.set_zlabel("Increase Avg")
    plt.savefig("Datasets/%s.pdf"%filename)
    plt.savefig("Datasets/%s.png"%filename)


# plt.show()

