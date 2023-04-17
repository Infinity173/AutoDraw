import pandas as pd
import matplotlib.pyplot as plt
import cv2
import numpy as np

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
print(len(data))
# for i,data_i in enumerate(data):
#     row_id = i // 4
#     col_id = i % 4
#     x_left = col_id*160+20
#     x_right = x_left+120
#     y = 32*row_id+16
#     cv2.circle(picture,(x_left,y),2,(0,0,0),-1)
#     cv2.circle(picture, (x_right, y), 2, (0, 0, 0), -1)
#     cv2.line(picture,(x_left,y),(x_right,y),(0,0,0),1)

bus_t = []
bus_b = []
for data_i in data:
    if data_i[4] not in bus_t:
        bus_t.append(data_i[4])

for data_j in data:
    if data_j[8] not in bus_b:
        bus_b.append(data_j[8])

for i in range(len(bus_t)):
    y = 32*i+16
    x = 40
    cv2.circle(picture, (x, y), 2, (0, 0, 0), -1)

for j in range(len(bus_b)):
    y = 32*j+16
    x = 600
    cv2.circle(picture, (x, y), 2, (0, 0, 0), -1)

for data_i in data:
    for i,bus_i in enumerate(bus_t):
        if data_i[4]==bus_i:
            left_id = i
    for j,bus_j in enumerate(bus_b):
        if data_i[8]==bus_j:
            right_id = j
    cv2.line(picture,(40,32*left_id+16),(600,32*right_id+16),(0,0,0),1)

cv_show(picture)








