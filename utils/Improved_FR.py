import networkx as nx
import numpy as np
import scipy as sp
import scipy.sparse
import matplotlib.pyplot as plt
import random
# import read_psse

def Improved_FR_Layout(G,iterations=50,threshold=1e-4,weight="weight",node_degree=None):
    center = np.zeros(2)

    if len(G) == 0:
        return {}
    if len(G) == 1:
        return {nx.utils.arbitrary_element(G.nodes()): center}
    
    A = nx.to_numpy_array(G, weight=weight)
    nnodes, _ = A.shape
    pos = np.asarray(np.random.rand(nnodes, 2),dtype=A.dtype)
    k = np.sqrt(1.0 / nnodes)
    
    
    t = max(max(pos.T[0]) - min(pos.T[0]), max(pos.T[1]) - min(pos.T[1])) * 0.1
    dt = t / (iterations + 1)
    delta = np.zeros((pos.shape[0], pos.shape[0], pos.shape[1]), dtype=A.dtype)
    
    for _ in range(iterations):
        delta = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
        distance = np.linalg.norm(delta, axis=-1)
        np.clip(distance, 0.01, None, out=distance)
        fr = k * k / distance**2
        fr = node_degree*fr
        fr = node_degree*fr
        fa = A * distance / k
        fa = fa / node_degree
        displacement_r = np.einsum("ijk,ij->ik", delta, fr)
        displacement_a = np.einsum("ijk,ij->ik", delta, fa)
        displacement = displacement_r - displacement_a
        length = np.linalg.norm(displacement, axis=-1)
        length = np.where(length < 0.01, 0.5, length)
        delta_pos = np.einsum("ij,i->ij", displacement, t / length)
        pos += delta_pos
        # cool temperature
        t -= dt
        if (np.linalg.norm(delta_pos) / nnodes) < threshold:
            break

    pos = dict(zip(G,pos))
    return pos        

def get_node_weight(G,load_list,generator_list):
    weighted_nodes = []
    degree = {}
    for n, d in G.degree():
        degree.update({n:d}) 
    
    for generator in generator_list:
        bus_id = generator[0]
        degree[bus_id] = degree[bus_id] + 1

    for load in load_list:
        load_id = load[0]
        degree[load_id] = degree[load_id] + 1

    for i in range(len(G)):
        node_row = []
        for j in range(len(G)):
            weight = (degree[i+1]*0.2+1)*(degree[j+1]*0.2+1)
            node_row.append(weight)
        weighted_nodes.append(node_row)
    
    return weighted_nodes

def get_edge_weight(branch_list,transformer_list):
    weighted_edges = []
    for branch in branch_list:
        edge_row = (branch[0],branch[1],1)
        weighted_edges.append(edge_row)
    for transformer in transformer_list:
        edge_row = (transformer[0],transformer[1],4)
        weighted_edges.append(edge_row)
    return weighted_edges

if __name__ == '__main__':
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
    weighted_edges = get_edge_weight(branch_list,transformer_list)
    G.add_weighted_edges_from(weighted_edges)
    weighted_nodes = get_node_weight(G,load_list,generator_list) 
    pos = Improved_FR_Layout(G,iterations=2000,node_degree=weighted_nodes)
    nx.draw(G, pos, with_labels=True, node_color='r', alpha=0.8)
    plt.show()