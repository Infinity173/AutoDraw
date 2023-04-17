import numpy as np
from math import dist
import random
import copy
import matplotlib.pyplot as plt

# population为种群中个体数目，bus_numbers为母线数量
def initialization(population, bus_numbers):
    initialized = []
    for i in range(population):
        random_path_array = np.random.choice(list(range(0, 5)), size=bus_numbers*2)
        random_path_list = random_path_array.tolist()
        initialized.append(random_path_list)
    return initialized

###   l1 [xa, ya, xb, yb]   l2 [xa, ya, xb, yb]
def Intersect(l1, l2):
    v1 = (l1[0] - l2[0], l1[1] - l2[1])
    v2 = (l1[0] - l2[2], l1[1] - l2[3])
    v0 = (l1[0] - l1[2], l1[1] - l1[3])
    a = v0[0] * v1[1] - v0[1] * v1[0]
    b = v0[0] * v2[1] - v0[1] * v2[0]

    temp = l1
    l1 = l2
    l2 = temp
    v1 = (l1[0] - l2[0], l1[1] - l2[1])
    v2 = (l1[0] - l2[2], l1[1] - l2[3])
    v0 = (l1[0] - l1[2], l1[1] - l1[3])
    c = v0[0] * v1[1] - v0[1] * v1[0]
    d = v0[0] * v2[1] - v0[1] * v2[0]

    if a*b < 0 and c*d < 0:
        return True
    else:
        return False

#topology_mat为各个节点之间的最短距离
def fitness(path, topology_mat):
    # all_length = 0
    all_cross = 1
    all_reapet = 1
    all_angle = 1
    # for topology in topology_mat:
    #     point_1_index = topology[0]
    #     point_2_index = topology[1]
    #     x_1_index = 2*(point_1_index-1)
    #     y_1_index = 2*(point_1_index-1)+1
    #     x_1 = path[x_1_index]
    #     y_1 = path[y_1_index]
    #     x_2_index = 2*(point_2_index-1)
    #     y_2_index = 2*(point_2_index-1)+1
    #     x_2 = path[x_2_index]
    #     y_2 = path[y_2_index]
    #     distance = dist((x_1,y_1),(x_2,y_2))
    #     all_length += distance

    for i, topology in enumerate(topology_mat):
        point_1_index = topology[0]
        point_2_index = topology[1]
        x_1_index = 2 * (point_1_index - 1)
        y_1_index = 2 * (point_1_index - 1) + 1
        x_1 = path[x_1_index]
        y_1 = path[y_1_index]
        x_2_index = 2 * (point_2_index - 1)
        y_2_index = 2 * (point_2_index - 1) + 1
        x_2 = path[x_2_index]
        y_2 = path[y_2_index]
        if x_1 != x_2 and y_1 !=y_2:
            all_angle = all_angle+10

    path_i = 0
    while path_i < 14:
        path_j = path_i + 1
        while path_j < 14:
            if path[path_i*2]== path[path_j*2] and path[path_i*2+1] == path[path_j*2+1]:
                all_reapet = all_reapet + 1
            path_j = path_j +1
        path_i = path_i + 1

    for i,topology in enumerate(topology_mat):
        point_1_index = topology[0]
        point_2_index = topology[1]
        x_1_index = 2*(point_1_index-1)
        y_1_index = 2*(point_1_index-1)+1
        x_1 = path[x_1_index]
        y_1 = path[y_1_index]
        x_2_index = 2*(point_2_index-1)
        y_2_index = 2*(point_2_index-1)+1
        x_2 = path[x_2_index]
        y_2 = path[y_2_index]

        j=i+1
        while j < len(topology_mat):
            point_1_index = topology_mat[j][0]
            point_2_index = topology_mat[j][1]
            x_1_index = 2 * (point_1_index - 1)
            y_1_index = 2 * (point_1_index - 1) + 1
            x_1_else = path[x_1_index]
            y_1_else = path[y_1_index]
            x_2_index = 2 * (point_2_index - 1)
            y_2_index = 2 * (point_2_index - 1) + 1
            x_2_else = path[x_2_index]
            y_2_else = path[y_2_index]

            l1=[x_1, y_1, x_2, y_2]
            l2=[x_1_else, y_1_else, x_2_else, y_2_else]
            if Intersect(l1,l2):
                all_cross = all_cross+1
            j = j+1

    fit = 1.5*1/all_cross+1.2*1/all_reapet+3*1/all_angle
    return fit

def select(generation, population, topology_mat):
    all_fitness = []
    for path in generation:
        fit = fitness(path, topology_mat)
        all_fitness.append(fit)
    fitness_array = np.array(all_fitness)
    fitness_array = fitness_array / fitness_array.sum()
    selected_index = np.random.choice(list(range(population)), size=population, p=fitness_array)
    selected = []
    for index in selected_index:
        selected.append(generation[index])
    return selected


def cross(selected, population, probability, bus_numbers):
    # 内层嵌套需要深拷贝才能开辟新的内存空间
    crossed = copy.deepcopy(selected)
    frequency = population * probability
    count = 0
    i = 0
    while i < population - 1 and count < frequency:
        # 随机生成两个交叉点
        position1 = random.randrange(0, int(bus_numbers/2))
        position1 = position1*2
        position2 = random.randrange(int(bus_numbers/2), bus_numbers)
        position2 = position2*2
        # 截取交叉片段
        crossed1 = selected[i].copy()
        crossed2 = selected[i + 1].copy()
        crossed12 = crossed1[position1:position2 + 1]
        crossed22 = crossed2[position1:position2 + 1]
        # 交叉生成染色体1
        result1 = crossed1[:position1]
        result1.extend(crossed22)
        result1.extend(crossed1[position2+1:])
        # 交叉生成染色体2
        result2 = crossed2[:position1]
        result2.extend(crossed12)
        result2.extend(crossed2[position2+1:])

        crossed[i] = result1
        crossed[i + 1] = result2
        count += 1
        i += 2
        return crossed

def mutation(crossed, population, probability, bus_numbers):
    #内层嵌套需要深拷贝才能开辟新的内存空间
    mutated = copy.deepcopy(crossed)
    for i in range(population):
        whether_mutated = True if random.random() < probability else False
        if whether_mutated:
            #随机生成两个点
            position1 = random.randrange(0, int(bus_numbers/2))
            position1 = position1*2
            position2 = random.randrange(int(bus_numbers/2), bus_numbers)
            position2 = position2*2
            #将中间染色体逆转
            # mid_reversed = crossed[i][position1: position2 + 1]
            # mid_reversed.reverse()
            head_reversed = crossed[i][position1:position1+1]
            tail_reversed = crossed[i][position2:position2+1]
            #拼接生成变异后染色体
            result = crossed[i][:position1]
            result.extend(tail_reversed)
            result.extend(crossed[i][position1+1:position2])
            result.extend(head_reversed)
            result.extend(crossed[i][position2+1:])
            #result.extend(mid_reversed)
            #result.extend(crossed[i][position2 + 1:])
            mutated[i] = result
    return mutated

def search(final_generation, topology_mat):
    all_fitness = []
    for path in final_generation:
        fit = fitness(path, topology_mat)
        all_fitness.append(fit)
    index = all_fitness.index(max(all_fitness))
    return final_generation[index]

def ga(population, generations, cross_probability, mutation_probability, topology_mat, bus_numbers):
    generation = initialization(population, bus_numbers)
    for i in range(generations):
        generation = select(generation, population, topology_mat)
        generation = cross(generation, population, cross_probability, bus_numbers)
        generation = mutation(generation, population, mutation_probability, bus_numbers)
    best = search(generation, topology_mat)
    return best, round(1 / fitness(best, topology_mat))

if __name__ == '__main__':
    topology_mat = [[1, 2], [1, 5], [2, 3], [2, 4], [2, 5], [3, 4], [4, 5], [6, 11], [6, 12], [6, 13], [7, 8], [7, 9],[9, 10], [9, 14], [10, 11], [12, 13], [13, 14],[4,7],[4,9],[5,6]]
    best_value = 0xffff
    best_path = []
    for i in range(10):
        path, value = ga(60, 300, 0.7, 0.05, topology_mat, 14)
        if value < best_value:
            best_value = value
            best_path = path
    print(best_path, best_value)

    i = 0
    while i < 14:
        x = best_path[i*2]
        y = best_path[i*2+1]
        plt.scatter(x,y)
        plt.text(x,y, f"{i + 1}", fontsize=12, color="k")
        i = i + 1
    for topology in topology_mat:
        x_head = best_path[(topology[0]-1)*2]
        y_head = best_path[(topology[0]-1)*2+1]
        x_tail = best_path[(topology[1]-1)*2]
        y_tail = best_path[(topology[1]-1)*2+1]
        plt.plot([x_head, x_tail], [y_head, y_tail])
    plt.show()

