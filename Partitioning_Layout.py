import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import Read_PSSE

# Fluid_Communities分区算法
def Fluid_Communities_Partitioning(G,k,max_iter):
    part_result = nx.algorithms.community.asyn_fluidc(G,k,max_iter)
    result = []
    for part in part_result:
        result_row = []
        for i in part:
            result_row.append(i)
        result.append(result_row)
    return result

# 力导算法布局
def FR_Layout(G,partitioning_result,topology_list,display_index):
    if display_index>len(partitioning_result) or display_index<0:
        print('error, please select again!')
    
    elif 0<display_index<=len(partitioning_result):
        display_list_new = []
        display_list = partitioning_result[display_index-1]
        for i in display_list:
            display_list_new.append(i)
        for list in topology_list:
            if list[0] in display_list and list[1] not in display_list:
                display_list_new.append(list[1])
            elif list[0] not in display_list and list[1] in display_list:
                display_list_new.append(list[0])

        pos = nx.kamada_kawai_layout(G)
        G_new = nx.Graph()
        topology_list_new = []
        for topology in topology_list:
            if topology[0] in display_list_new and topology[1] in display_list_new:
                topology_list_new.append(topology)
        G_new.add_edges_from(topology_list_new)
        
        point_number = 0
        for result in partitioning_result:
            point_number = point_number + len(result)
        for j in range(point_number):
            if j+1 not in display_list_new:
                del pos[j+1]

    elif display_index==0:
        pos = nx.kamada_kawai_layout(G)
        G_new = G

    return G_new,pos

if __name__ == '__main__':
    # 得到拓扑关系
    path = 'PSSE/ieee118.raw'
    load_data,generator_data,branch_data,transformer_data = Read_PSSE.readRaw(path)
    _,_,branch_list,transformer_list = Read_PSSE.string2int(load_data,generator_data,branch_data,transformer_data)
    topology_list = []
    for branch in branch_list:
        topology_list.append(branch)
    for transformer in transformer_list:
        topology_list.append(transformer)

    # 得到graph并进行分区
    G = nx.Graph()
    G.add_edges_from(topology_list)
    result = Fluid_Communities_Partitioning(G,6,10000)
    print(result)

    # 得到力导布局
    G_new,pos = FR_Layout(G,result,topology_list,4)
    G_all,pos_all = FR_Layout(G,result,topology_list,0)
    # 绘图
    # color_map = []
    # for pos_i in pos_all.items():
    #     for i,result_i in enumerate(result):
    #         if pos_i[0] in result_i:
    #             color_map.append(i*0.1)   
    nx.draw(G_new, pos, with_labels=True,node_color='r', alpha=0.5)
    plt.show()
    # nx.draw(G_all, pos_all, with_labels=True,node_color=color_map, alpha=0.5)
    # plt.show()


    


