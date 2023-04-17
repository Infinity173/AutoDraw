import matplotlib.pyplot as plt
import numpy as np
import os
import re
import random

max_posx=1000
max_posy=1000
max_length = 200
min_length = 100
bus_Number = 14

def readRaw(path):#path为raw文件所在路径
    f = open(path, encoding='utf-8')
    contents = f.readlines()
    f.close()
    flage = False
    list = []
    for content in contents:
        if (bool(re.search("BEGIN BRANCH DATA", content))):
            flage = True
        if (bool(re.search("END OF BRANCH DATA", content))):
            flage = False
        if flage:
            list.append(content)
    list.pop(0)
    return list

def string2int(list):
    id_list = []
    for x in list:
        id_row = []
        x_list = x.split(',')
        match_1 = re.search(r'\d+', x_list[0])
        match_2 = re.search(r'\d+', x_list[1])
        id_1 = int(match_1.group())
        id_2 = int(match_2.group())
        id_row.append(id_1)
        id_row.append(id_2)
        id_list.append(id_row)
    return id_list

def bus_init():
    posx = random.uniform(0, max_posx)
    posy = random.uniform(0, max_posy)  # 初始化点坐标和受力
    bus_position = (posx, posy)
    bus_angle = random.randint(0,0)
    bus_length = random.uniform(min_length,max_length)
    return bus_position,bus_angle,bus_length

if __name__ == '__main__':
    path = 'ieee14.raw'
    list = readRaw(path)
    id_list = string2int(list)
    for id in id_list:
        print(id)
    bus_position_list = []
    for i in range(bus_Number):
        bus_position,bus_angle,bus_length = bus_init()
        if bus_angle==0:
            bus_x_l = bus_position[0]-bus_length/2
            bus_x_r = bus_position[0]+bus_length/2
            bus_y = bus_position[1]
            plt.plot([bus_x_l, bus_x_r], [bus_y, bus_y])
        if bus_angle==1:
            bus_x = bus_position[0]
            bus_y_t = bus_position[1]-bus_length/2
            bus_y_b = bus_position[1]+bus_length/2
            plt.plot([bus_x, bus_x], [bus_y_t, bus_y_b])
        plt.text(bus_position[0],bus_position[1],f"{i+1}", fontsize=12, color="k")
        bus_position_list.append(bus_position)

    for id in id_list:
        x_head = bus_position_list[id[0]-1][0]
        y_head = bus_position_list[id[0]-1][1]
        x_tail = bus_position_list[id[1]-1][0]
        y_tail = bus_position_list[id[1]-1][1]
        plt.plot([x_head, x_tail], [y_head, y_tail])
    plt.show()
    # print(bus_position_list)