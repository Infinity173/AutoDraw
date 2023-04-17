import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

First_choice_point = 22
Bus_distance = 500

# 读取节点坐标数据
row_data = pd.read_excel('data/data_57.xls',header=None)
data_old = row_data.values
data = []
for data_i in data_old:
    data_x = data_i[0]*1000
    data_y = data_i[1]*1000
    data_x = int(data_x)
    data_y = int(data_y)
    data.append([data_x,data_y])
# 读取拓扑关系数据
row_data = pd.read_excel('data/topology_data_57.xls',header=None)
topology_data = row_data.values

# 生成拓扑数据表
topo_list = []
for topo_i in topology_data:
    topo_xy = (topo_i[0],topo_i[1])
    topo_list.append(topo_xy)
# 生成节点坐标字典
pos={}
for i,data_i in enumerate(data):
    pos.update({i+1:(data_i[0],data_i[1])})

# 生成初始力导布局图
# ax1 = plt.subplot(1, 2, 1)
G1 = nx.Graph()
G1.add_edges_from(topo_list)
T = nx.minimum_spanning_tree(G1)
minTreeEdge = sorted(T.edges)
# nx.draw(G1, pos, with_labels=True, node_color='c', alpha=0.8)  # 绘制无向图
# nx.draw_networkx_edges(G1,pos,edgelist=T.edges,edge_color='b',width=4)  # 设置指定边的颜色

# 寻找节点与父节点
TreeSearchList = []
TreeSearchList.append({First_choice_point:0})
Traversed_List = []
Traversed_List.append(First_choice_point)
for list in TreeSearchList:
    treeSearchRowList = {}
    for list_i in list:
        for edge in minTreeEdge:
            if edge[0] == list_i and edge[1] not in Traversed_List:
                treeSearchRowList.update({edge[1]:list_i})
                Traversed_List.append(edge[0])
            elif edge[1] == list_i and edge[0] not in Traversed_List:
                treeSearchRowList.update({edge[0]:list_i})
                Traversed_List.append(edge[1])
    TreeSearchList.append(treeSearchRowList)
    # print(treeSearchRowList)
    if len(treeSearchRowList) == 0:
        break

position_list = []
# 重新布局：横平竖直，减少交叉
for i,list in enumerate(TreeSearchList):
    if len(list)>0 and i>0:
        for list_i in list.items():
            x_child = data[list_i[0]-1][0]
            y_child = data[list_i[0]-1][1]
            x_father = data[list_i[1]-1][0]
            y_father = data[list_i[1]-1][1]
            if (x_father,y_father) not in position_list:
                position_list.append((x_father,y_father))
            
            if abs(x_child-x_father) >= abs(y_child-y_father) and x_child-x_father<0:
                x_child = x_father-Bus_distance
                y_child = y_father
                data[list_i[0]-1][0] = x_child
                data[list_i[0]-1][1] = y_child
            elif abs(x_child-x_father) >= abs(y_child-y_father) and x_child-x_father>0:
                x_child = x_father+Bus_distance
                y_child = y_father
                data[list_i[0]-1][0] = x_child
                data[list_i[0]-1][1] = y_child
            elif abs(x_child-x_father) < abs(y_child-y_father) and y_child-y_father<0:
                x_child = x_father
                y_child = y_father-Bus_distance
                data[list_i[0]-1][0] = x_child
                data[list_i[0]-1][1] = y_child
            elif abs(x_child-x_father) < abs(y_child-y_father) and y_child-y_father>0:
                x_child = x_father
                y_child = y_father+Bus_distance
                data[list_i[0]-1][0] = x_child
                data[list_i[0]-1][1] = y_child
            
            # if (x_child,y_child) in position_list:
            #     a = (x_father,y_father+Bus_distance)
            #     b = (x_father+Bus_distance,y_father)
            #     c = (x_father,y_father-Bus_distance)
            #     d = (x_father-Bus_distance,y_father)               
            #     if a not in position_list:
            #         x_child = x_father
            #         y_child = y_father+Bus_distance
            #         data[list_i[0]-1][0] = x_child
            #         data[list_i[0]-1][1] = y_child
            #     elif a in position_list and b not in position_list:
            #         x_child = x_father+Bus_distance
            #         y_child = y_father
            #         data[list_i[0]-1][0] = x_child
            #         data[list_i[0]-1][1] = y_child
            #     elif a in position_list and b in position_list and c not in position_list:
            #         x_child = x_father
            #         y_child = y_father-Bus_distance
            #         data[list_i[0]-1][0] = x_child
            #         data[list_i[0]-1][1] = y_child
            #     elif a in position_list and b in position_list and c in position_list and d not in position_list:
            #         x_child = x_father-Bus_distance
            #         y_child = y_father
            #         data[list_i[0]-1][0] = x_child
            #         data[list_i[0]-1][1] = y_child
            #     elif a in position_list and b in position_list and c in position_list and d in position_list:
            #         print(list_i[0])
            #         print((x_child,y_child))
            j = 0
            if (x_child,y_child) in position_list:
                while j < 20:
                    (ii,jj) = divmod(j,4)
                    a = (x_father,y_father+(ii+1)*Bus_distance)
                    b = (x_father+(ii+1)*Bus_distance,y_father)
                    c = (x_father,y_father-(ii+1)*Bus_distance)
                    d = (x_father-(ii+1)*Bus_distance,y_father)
                    if jj==0 and a not in position_list:
                        x_child = x_father
                        y_child = y_father+(ii+1)*Bus_distance
                        data[list_i[0]-1][0] = x_child
                        data[list_i[0]-1][1] = y_child
                        break
                    elif jj==1 and a in position_list and b not in position_list:
                        x_child = x_father+(ii+1)*Bus_distance
                        y_child = y_father
                        data[list_i[0]-1][0] = x_child
                        data[list_i[0]-1][1] = y_child
                        break
                    elif jj==2 and a in position_list and b in position_list and c not in position_list:
                        x_child = x_father
                        y_child = y_father-(ii+1)*Bus_distance
                        data[list_i[0]-1][0] = x_child
                        data[list_i[0]-1][1] = y_child
                        break
                    elif jj==3 and a in position_list and b in position_list and c in position_list and d not in position_list:
                        x_child = x_father-(ii+1)*Bus_distance
                        y_child = y_father
                        data[list_i[0]-1][0] = x_child
                        data[list_i[0]-1][1] = y_child
                        break
                    j = j + 1
                    
            pos[list_i[0]] = (x_child,y_child)
            if (x_child,y_child) not in position_list:
                z = (x_child,y_child)
                position_list.append(z)

# 生成新的布局
# ax2 = plt.subplot(1, 2, 2)
nx.draw(G1, pos, with_labels=True, node_color='c', alpha=0.8)  # 绘制无向图
nx.draw_networkx_edges(G1,pos,edgelist=T.edges,edge_color='b',width=4)  # 设置指定边的颜色

plt.show()

