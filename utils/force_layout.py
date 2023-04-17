# import read_psse
import networkx as nx
import matplotlib.pyplot as plt

# 力导布局,返回节点位置坐标
def fr_layout(branch_list,transformer_list):
    bus_node = {}
    G = nx.Graph()

    weighted_edges = []
    for branch in branch_list:
        edge_row = (branch[0],branch[1],1)
        weighted_edges.append(edge_row)
    for transformer in transformer_list:
        edge_row = (transformer[0],transformer[1],2.5)
        weighted_edges.append(edge_row)

    G.add_weighted_edges_from(weighted_edges)
    pos = nx.kamada_kawai_layout(G,weight='weight')
    # nx.draw(G, pos, with_labels=True, node_color='r', alpha=0.8)
    # print(pos)
    for i in range(len(pos)):
        for item in pos.items():
            if i + 1 == item[0]:
                position = [item[1][0],item[1][1]]
                bus_node.update({i+1:position})
    return bus_node

# if __name__ == '__main__':
#     path = 'PSSE/ieee39.raw'
#     load_data,generator_data,branch_data,transformer_data = read_psse.readRaw(path)
#     load_list,generator_list,branch_list,transformer_list = read_psse.string2int(load_data,generator_data,branch_data,transformer_data)

#     bus_node = fr_layout(branch_list,transformer_list)
#     print(bus_node)