import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

Init_point = [9,13,38,4,15,12,24,56,32,41]

# 读取节点坐标数据
row_data = pd.read_excel('data/data_57.xls',header=None)
data = row_data.values
# 读取拓扑关系数据
row_data = pd.read_excel('data/topology_data_57.xls',header=None)
topology_data = row_data.values

# 广度搜索函数
def bfsearch(data,s,level):
    TreeSearchList = []
    TreeSearchList.append({s:0})
    Traversed_List = []
    Traversed_List.append(s)
    for list in TreeSearchList:
        treeSearchRowList = {}
        for list_i in list:
            for edge in data:
                if edge[0] == list_i and edge[1] not in Traversed_List:
                    treeSearchRowList.update({edge[1]:list_i})
                    Traversed_List.append(edge[1])
                elif edge[1] == list_i and edge[0] not in Traversed_List:
                    treeSearchRowList.update({edge[0]:list_i})
                    Traversed_List.append(edge[0])
        TreeSearchList.append(treeSearchRowList)
        # print(Traversed_List)
        if len(treeSearchRowList) == 0:
            break
    TreeSearchList = TreeSearchList[0:level]
    return TreeSearchList

# 生成拓扑数据表
topo_list = []
for topo_i in topology_data:
    topo_xy = (topo_i[0],topo_i[1])
    topo_list.append(topo_xy)
# 生成节点坐标字典
pos={}
for i,data_i in enumerate(data):
    pos.update({i+1:(data_i[0],data_i[1])})

# 生成高亮坐标列表
Init_node = {}
for point in Init_point:
    for pos_i in pos:
        if pos_i == point:
            Init_node.update({pos_i:(data[pos_i-1][0],data[pos_i-1][1])})

# 生成初始力导布局图
# ax1 = plt.subplot(1, 2, 1)
G1 = nx.Graph()
G1.add_edges_from(topo_list)
color_map = []
for i in G1:
    color_map.append('c')
for node in G1:
    if node in Init_point:
        color_map[node-1] = 'r'
nx.draw(G1, pos, with_labels=True, node_color=color_map, alpha=0.8)  # 绘制无向图
nx.draw_networkx_edges(G1,pos,edge_color='black',width=2)  # 设置指定边的颜色


z = bfsearch(topology_data,24,4)
print(z)

plt.show()