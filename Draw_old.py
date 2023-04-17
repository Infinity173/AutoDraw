from PIL import Image
from PIL import ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import Read_PSSE

# 画布大小与线条厚度
width = 1200
height = 1200
thick = 4

# 绘制母线函数
def draw_bus(canva,x,y,width):
    draw = ImageDraw.Draw(canva)
    x_left = x-int(width/2)
    x_right = x+int(width/2)
    draw.line((x_left,y,x_right,y),width=thick,fill='black')

# 绘制负荷函数
def draw_load(canva,x,y,height):
    draw = ImageDraw.Draw(canva)
    if height>0:
        draw.line((x,y,x,y+height),width=thick,fill='black')
        draw.polygon((x-5,y+height,x,y+10+height,x+5,y+height),'black','black')
    elif height<0:
        draw.line((x,y,x,y+height),width=thick,fill='black')
        draw.polygon((x-5,y+height,x,y-10+height,x+5,y+height),'black','black')

# 绘制发电机函数
def draw_generator(canva,x,y,height):
    draw = ImageDraw.Draw(canva)
    if height>0:
        draw.line((x,y,x,y+height),width=thick,fill='black')
        draw.arc((x-15,y+height,x+15,y+height+30),0,360,width=thick,fill='black')
        draw.arc((x-12,y+height+15-6,x,y+height+15+6),180,0,width=thick,fill='black')
        draw.arc((x,y+height+15-6,x+12,y+height+15+6),0,180,width=thick,fill='black')
    elif height<0:
        draw.line((x,y,x,y+height),width=thick,fill='black')
        draw.arc((x-15,y+height-30,x+15,y+height),0,360,width=thick,fill='black')
        draw.arc((x-12,y+height-15-6,x,y+height-15+6),180,0,width=thick,fill='black')
        draw.arc((x,y+height-15-6,x+12,y+height-15+6),0,180,width=thick,fill='black')

# 绘制变压器函数        
def draw_transformer(canva,x,y):
    draw = ImageDraw.Draw(canva)
    # 变压器圆心纵坐标分别为y-12、y+12
    draw.arc((x-20,y-12-20,x+20,y-12+20),0,360,width=thick,fill='black')
    draw.arc((x-20,y+12-20,x+20,y+12+20),0,360,width=thick,fill='black')
    # 变压器的长度为64

# 读取节点坐标数据
def read_data(path):
    row_data = pd.read_excel(path,header=None)
    data = row_data.values
    data_x = data[:,0]
    data_y = data[:,1]
    data_x = np.asarray(data_x)
    data_y = np.asarray(data_y)
    data_x_int = []
    data_y_int = []
    data_new =[]
    for x in data_x:
        x = float(x-np.min(data_x))/(np.max(data_x)-np.min(data_x))
        x = int(x*1000+100)
        data_x_int.append(x)
    for y in data_y:
        y = float(y-np.min(data_y))/(np.max(data_y)-np.min(data_y))
        y = int(y*1000+100)
        data_y_int.append(y)

    l = len(data)
    i = 0
    while i<l:
        row_data = (data_x_int[i],data_y_int[i])
        data_new.append(row_data)
        i = i+1
    return data_new

if __name__ == '__main__':
    array = np.ndarray((height,width,3),np.uint8)
    array[:, :, :] = 255
    canva = Image.fromarray(array)
    draw = ImageDraw.Draw(canva)

    # 读取节点坐标位置
    data = read_data('data/data_39.xls')
    for data_i in data:
        draw_bus(canva,data_i[0],data_i[1],40)
    
    # 读取拓扑关系数据
    row_data = pd.read_excel('data/topology_data_39.xls',header=None)
    topology_data = row_data.values
    topo_list = []
    for topo_i in topology_data:
        topo_xy = (topo_i[0],topo_i[1])
        topo_list.append(topo_xy)
    for topo in topo_list:
        x1 = data[topo[0]-1][0]
        y1 = data[topo[0]-1][1]
        x2 = data[topo[1]-1][0]
        y2 = data[topo[1]-1][1]
        draw.line((x1,y1,x2,y2),width=3,fill='black')

    path = 'PSSE/ieee39.raw'
    load_data,generator_data,branch_data,transformer_data = Read_PSSE.readRaw(path)
    load_list,generator_list,branch_list,transformer_list = Read_PSSE.string2int(load_data,generator_data,branch_data,transformer_data)
    for load in load_list:
        x = data[load[0]-1][0]
        y = data[load[0]-1][1]
        draw_load(canva,x,y,-40)
    
    for generator in generator_list:
        x = data[generator[0]-1][0]
        y = data[generator[0]-1][1]
        draw_generator(canva,x,y,40)

    arr = np.array(canva)
    image = np.array(arr,np.uint8)
    image = cv2.flip(image, 0)
    # canva.show()
    plt.imshow(image)
    plt.show()