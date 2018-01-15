import matplotlib
# matplotlib.use('Qt4Agg')
import pylab
# assumption: breath frequency: 6/min
import numpy as np
import cv2

#translate image
def translate_image(image,x,y):
    rows,cols = image.shape
    M = np.float32([[1,0,x],[0,1,y]])
    dst = cv2.warpAffine(image,M,(cols,rows))
    return dst


def create_sample_data():
    x = np.linspace(0, 65535,65536)
    t = np.linspace(0, 60, 60) #300s 60 frames
    Tm,Xm = np.meshgrid(t, x)

    single_image = np.zeros([256,256])
    for i in range(0,20):
        for j in range(0,20):
            single_image[i+100,j+100] = 1

    dst = translate_image(single_image,10,0)
    D = []
    for i in range(0,60):
        z = 10*np.sin(i)
        t_image = translate_image(single_image,0,z)
        D.append(np.reshape(t_image,[256*256,1]))
    D_array = np.array(D)[:,:,0]
    return D_array

