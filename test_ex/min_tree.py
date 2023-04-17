import numpy as np
import matplotlib.pyplot as plt # 导入 Matplotlib 工具包
import networkx as nx  # 导入 NetworkX 工具包

# 1. 天然气管道铺设
G1 = nx.Graph()  # 创建：空的 无向图
# G1.add_weighted_edges_from([(1,2,5),(1,3,6),(2,4,2),(2,5,12),(3,4,6),
#                 (3,6,7),(4,5,8),(4,7,4),(5,8,1),(6,7,5),(7,8,10)])  # 向图中添加多条赋权边: (node1,node2,weight)

G1.add_weighted_edges_from([(1,2,1),(1,5,1),(2,3,1),(2,4,1),(2,5,1),(3,4,1),(4,5,1),(4,7,1),(4,9,1),(5,6,1),(6,11,1),(6,12,1),(6,13,1),(7,8,1),(7,9,1),(9,10,1),(9,14,1),(10,11,1),(12,13,1),(13,14,1)])  # 向图中添加多条赋权边: (node1,node2,weight)

T = nx.minimum_spanning_tree(G1)  # 返回包括最小生成树的图
print(T.nodes)  # 最小生成树的 顶点
print(T.edges)  # 最小生成树的 边
print(sorted(T.edges)) # 排序后的 最小生成树的 边
print(sorted(T.edges(data=True)))  # data=True 表示返回值包括边的权重

mst1 = nx.tree.minimum_spanning_edges(G1, algorithm="kruskal") # 返回最小生成树的边
print(list(mst1))  # 最小生成树的 边
mst2 = nx.tree.minimum_spanning_edges(G1, algorithm="prim",data=False)  # data=False 表示返回值不带权
print(list(mst2))

# 绘图
pos={1:(0,0),2:(0,3),3:(0,6),4:(3,3),5:(3,0),6:(6,0),7:(3,5),8:(3,6),9:(6,6),10:(6,5),11:(6,3),12:(9,0),13:(9,3),14:(9,6)}  # 指定顶点位置
nx.draw(G1, pos, with_labels=True, node_color='c', alpha=0.8)  # 绘制无向图
labels = nx.get_edge_attributes(G1,'weight')
nx.draw_networkx_edge_labels(G1,pos,edge_labels=labels, font_color='m') # 显示边的权值
nx.draw_networkx_edges(G1,pos,edgelist=T.edges,edge_color='b',width=4)  # 设置指定边的颜色
plt.show()
