# coding: utf-8

import scipy.io as sio  
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 

filename = 'Datasets/CollegeMsg'

number = []
changeAvg = []
increaseAvg = []

with open(filename,'r+') as file:
    for line in file.readlines():
        tmp = line.strip().split()
        number.append(float(tmp[0]))
        changeAvg.append(float(tmp[1]))
        increaseAvg.append(float(tmp[2]))
        

fig = plt.figure(filename)
ax = fig.add_subplot(111,projection='3d')

for i in range(len(number)):
    ax.scatter(number[i],changeAvg[i],increaseAvg[i])
    
ax.set_xlabel("Time Stamp")
ax.set_ylabel("Change Avg")
ax.set_zlabel("Increse Avg")

plt.savefig("%s.pdf"%filename)
plt.savefig("%s.png"%filename)
plt.show()