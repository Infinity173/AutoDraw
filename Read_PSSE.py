import numpy as np
import os
import re
import networkx as nx
import matplotlib.pyplot as plt

# 读取PSS/E文件数据,path为raw文件所在路径
def readRaw(path):
    f = open(path, encoding='utf-8')
    contents = f.readlines()
    f.close()
    
    load_data = []
    generator_data = []
    branch_data = []
    transformer_data = []

    for i,content in enumerate(contents):
        if (bool(re.search("BEGIN LOAD DATA", content))):
            load_data_begin = i
        if (bool(re.search("END OF LOAD DATA", content))):
            load_data_end = i
        if (bool(re.search("BEGIN GENERATOR DATA", content))):
            generator_data_begin = i
        if (bool(re.search("END OF GENERATOR DATA", content))):
            generator_data_end = i
        if (bool(re.search("BEGIN BRANCH DATA", content))):
            branch_data_begin = i
        if (bool(re.search("END OF BRANCH DATA", content))):
            branch_data_end = i
        if (bool(re.search("BEGIN TRANSFORMER DATA", content))):
            transformer_data_begin = i
        if (bool(re.search("END OF TRANSFORMER DATA", content))):
            transformer_data_end = i

    load_data = contents[load_data_begin+1:load_data_end]
    generator_data = contents[generator_data_begin+1:generator_data_end]
    branch_data = contents[branch_data_begin+1:branch_data_end]
    transformer_data = contents[transformer_data_begin+1:transformer_data_end]

    return load_data,generator_data,branch_data,transformer_data

# 将读取的string数据转换为int数据类型
def string2int(load_data,generator_data,branch_data,transformer_data):
    load_list = []
    generator_list = []
    branch_list = []
    transformer_list = []
    for x in load_data:
        list_row = []
        x_list = x.split(',')
        match_1 = re.search(r'\d+', x_list[0])
        id_1 = int(match_1.group())
        list_row.append(id_1)
        load_list.append(list_row)

    for x in generator_data:
        list_row = []
        x_list = x.split(',')
        match_1 = re.search(r'\d+', x_list[0])
        id_1 = int(match_1.group())
        list_row.append(id_1)
        generator_list.append(list_row)

    for x in branch_data:
        list_row = []
        x_list = x.split(',')
        match_1 = re.search(r'\d+', x_list[0])
        match_2 = re.search(r'\d+', x_list[1])
        id_1 = int(match_1.group())
        id_2 = int(match_2.group())
        list_row.append(id_1)
        list_row.append(id_2)
        branch_list.append(list_row)

    for i,x in enumerate(transformer_data):
        if i%4==0:
            list_row = []
            x_list = x.split(',')
            match_1 = re.search(r'\d+', x_list[0])
            match_2 = re.search(r'\d+', x_list[1])
            id_1 = int(match_1.group())
            id_2 = int(match_2.group())
            list_row.append(id_1)
            list_row.append(id_2)
            transformer_list.append(list_row)
    return load_list,generator_list,branch_list,transformer_list

if __name__ == '__main__':
    path = 'PSSE/ieee39.raw'
    load_data,generator_data,branch_data,transformer_data = readRaw(path)
    load_list,generator_list,branch_list,transformer_list = string2int(load_data,generator_data,branch_data,transformer_data)

    topology_list = []
    for branch in branch_list:
        # if branch not in topology_list:
        topology_list.append(branch)
    for transformer in transformer_list:
        # if transformer not in topology_list:
        topology_list.append(transformer)
    
    # 绘制力导布局图
    G = nx.Graph()
    G.add_edges_from(topology_list)
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='r', alpha=0.8)
    plt.show()