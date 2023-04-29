import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import read_psse
from utils import Improved_FR
import networkx as nx

# 展示图片函数
def cv_show(img):
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 节点坐标转换到[1200,1200]
def data_normalization(pos):
    data = []
    for item in pos.items():
        data.append([item[1][0],item[1][1]])

    data_x = [x[0] for x in data]
    data_y = [x[1] for x in data]
    data_x_int = []
    data_y_int = []
    new_data =[]
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
    while i < l:
        row_data = (data_x_int[i],data_y_int[i])
        new_data.append(row_data)
        i = i+1
    return new_data

if __name__ == '__main__':
    array = np.ndarray((1200,1200,3),np.uint8)
    array[:, :, :] = 255
    image = np.array(array,np.uint8)
    
    path = 'PSSE/ieee57.raw'
    load_data,generator_data,branch_data,transformer_data = read_psse.readRaw(path)
    load_list,generator_list,branch_list,transformer_list = read_psse.string2int(load_data,generator_data,branch_data,transformer_data)

    topology_list = []
    for branch in branch_list:
        topology_list.append(branch)
    for transformer in transformer_list:
        topology_list.append(transformer)

    # 绘制力导布局图
    G = nx.Graph()
    weighted_edges = Improved_FR.get_edge_weight(branch_list,transformer_list)
    G.add_weighted_edges_from(weighted_edges)
    weighted_nodes = Improved_FR.get_node_weight(G,load_list,generator_list) 
    bus_node = Improved_FR.Improved_FR_Layout(G,iterations=2000,weight="weight",node_degree=weighted_nodes)
    new_data = data_normalization(bus_node)
    
    for branch_topo in branch_list:
        image = cv2.line(image,(new_data[branch_topo[0]-1][0],new_data[branch_topo[0]-1][1]),(new_data[branch_topo[1]-1][0],new_data[branch_topo[1]-1][1]),(0,0,0),2,cv2.LINE_AA)

    for data in new_data:
        image = cv2.line(image,(data[0]-20,data[1]),(data[0]+20,data[1]),(255,0,0),4,cv2.LINE_AA)

    for l_index in load_list:
        image = cv2.line(image,(new_data[l_index[0]-1][0],new_data[l_index[0]-1][1]),(new_data[l_index[0]-1][0],new_data[l_index[0]-1][1]-20),(0,0,0),2,cv2.LINE_AA)
        image = cv2.rectangle(image,(new_data[l_index[0]-1][0]-5,new_data[l_index[0]-1][1]-30),(new_data[l_index[0]-1][0]+5,new_data[l_index[0]-1][1]-20),(0,255,0),2,cv2.LINE_AA)

    for g_index in generator_list:
        image = cv2.line(image,(new_data[g_index[0]-1][0],new_data[g_index[0]-1][1]),(new_data[g_index[0]-1][0],new_data[g_index[0]-1][1]+20),(0,0,0),2,cv2.LINE_AA)
        image = cv2.rectangle(image,(new_data[g_index[0]-1][0]-10,new_data[g_index[0]-1][1]+40),(new_data[g_index[0]-1][0]+10,new_data[g_index[0]-1][1]+20),(0,0,255),2,cv2.LINE_AA)
    
    for t_topo in transformer_list:
        pt1 = (new_data[t_topo[0]-1][0],new_data[t_topo[0]-1][1])
        pt2 = (new_data[t_topo[1]-1][0],new_data[t_topo[1]-1][1])
        x_tran_center = int((new_data[t_topo[0]-1][0]+new_data[t_topo[1]-1][0])/2)
        y_tran_center = int((new_data[t_topo[0]-1][1]+new_data[t_topo[1]-1][1])/2)
        width = 20
        height = 40
        image = cv2.rectangle(image,(x_tran_center-int(width/2),y_tran_center-int(height/2)),(x_tran_center+int(width/2),y_tran_center+int(height/2)),(255,127,127),2,cv2.LINE_AA)
        if new_data[t_topo[0]-1][1] >= new_data[t_topo[1]-1][1]:
            image = cv2.line(image,pt1,(x_tran_center,y_tran_center+int(height/2)),(0,0,0),2,cv2.LINE_AA)
            image = cv2.line(image,pt2,(x_tran_center,y_tran_center-int(height/2)),(0,0,0),2,cv2.LINE_AA)
        else:
            image = cv2.line(image,pt1,(x_tran_center,y_tran_center-int(height/2)),(0,0,0),2,cv2.LINE_AA)
            image = cv2.line(image,pt2,(x_tran_center,y_tran_center+int(height/2)),(0,0,0),2,cv2.LINE_AA)
    
    image = cv2.flip(image, 0)
    plt.imshow(image)
    plt.show()

