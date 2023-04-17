import numpy as np
import pandas as pd
import cv2

# def SearchTree(bus_id):
#     bus_id_copy = [a for a in bus_id]

# 展示图片函数
def cv_show(img):
    cv2.imshow('test',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 生成白色背景图片，像素640*640
picture = np.full((int(960),int(640),3),255,dtype=np.uint8)

# 读取数据
row_data = pd.read_excel('test.xlsx',header=0)
data = row_data.values
bus_name = []
for data_i in data:
    if data_i[4] not in bus_name:
        bus_name.append(data_i[4])
    if data_i[8] not in bus_name:
        bus_name.append(data_i[8])

bus_id = []
for data_i in data:
    bus_id_row = []
    bus_id_row.append(data_i[0])
    for i,bus_i in enumerate(bus_name):
        if data_i[4] == bus_i:
            bus_id_row.append(i)
    for j,bus_j in enumerate(bus_name):
        if data_i[8] == bus_j:
            bus_id_row.append(j)
    bus_id.append(bus_id_row)

# bus_id = np.array(bus_id)
# # print(bus_id[:,-1])
save_data = []
for bus_i in bus_id:
    dic = {"id":bus_i[0],"head_bus_id":bus_i[1],"bottom_bus_id":bus_i[2]}
    save_data.append(dic)
df = pd.DataFrame(save_data)
df.to_excel('data.xlsx', index=False, encoding='utf-8')

bus_list = []
bus_row = []
for bus_i in bus_id:
    if bus_i[1]==0 or bus_i[2]==0:
        bus_row.append(bus_i)
bus_list.append(bus_row)

i = 0
search_list_old = []
search_list_old.append(0)
search_index = []
search_index.append([0])
flage = True
while flage:
    search_list = []
    bus_list_row = []
    for bus_i in bus_list[i]:
        if bus_i[2] not in search_list_old and bus_i[2] not in search_list:
            search_list.append(bus_i[2])
        elif bus_i[1] not in search_list_old and bus_i[1] not in search_list:
            search_list.append(bus_i[1])
    search_index.append(search_list)
    for bus_i in bus_id:
        if bus_i[1] in search_list and bus_i[2] not in search_list_old and bus_i not in bus_list_row:
            bus_list_row.append(bus_i)
        elif bus_i[2] in search_list and bus_i[1] not in search_list_old and bus_i not in bus_list_row:
            bus_list_row.append(bus_i)
    bus_list.append(bus_list_row)
    for bus_i in bus_list[i]:
        if bus_i[2] not in search_list_old:
            search_list_old.append(bus_i[2])
        elif bus_i[1] not in search_list_old:
            search_list_old.append(bus_i[1])
    if len(bus_list_row)<1:
        flage = False
    i = i + 1

for bus_i in bus_list:
    print(bus_i)

for j,search_i in enumerate(search_index):
    l = len(search_i)
    if l > 0:
        spacing_distance = int(600/l)
        for i in range(l):
            cv2.line(picture,(150*j+20,20+spacing_distance*i+10),(150*j+20,20+spacing_distance*(i+1)-10),(0,0,0),1)
            y_center = int((20+spacing_distance*(i+1)+20+spacing_distance*i)/2)
            cv2.putText(picture, str(search_i[i]), (150*j+20, y_center), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0, 0, 0),1,cv2.LINE_AA)
    if j < len(search_index)-2:
        for bus_i in bus_list[j]:
            if bus_i[1] in search_i and bus_i[2] in search_index[j+1]:
                x_l = search_i.index(bus_i[1])
                x_r = search_index[j+1].index(bus_i[2])
            elif bus_i[2] in search_i and bus_i[1] in search_index[j+1]:
                x_l = search_i.index(bus_i[2])
                x_r = search_index[j+1].index(bus_i[1])
            spacing_distance_1 = int(600/len(search_i))
            spacing_distance_2 = int(600/len(search_index[j+1]))
            y_center_1 = int((20+spacing_distance_1*(x_l+1)+20+spacing_distance_1*x_l)/2)
            y_center_2 = int((20+spacing_distance_2*(x_r+1)+20+spacing_distance_2*x_r)/2)
            cv2.line(picture,(150*j+20,y_center_1),(150*(j+1)+20,y_center_2),(0,0,0),1)
cv_show(picture)





