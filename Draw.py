import cv2
import numpy as np
import matplotlib.pyplot as plt

# 展示图片函数
def cv_show(img):
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

array = np.ndarray((640,640,3),np.uint8)
array[:, :, :] = 255
image = np.array(array,np.uint8)

cv2.line(image,(120,120),(160,123),(255,0,0),2,cv2.LINE_AA)

plt.imshow(image)
plt.grid()
plt.show()