"""
plot the time intensity curve of DCE-MRI
edited by nx.cai 2017.11.22
"""
import sys
sys.path.append('/home/cai/Documents/PyDMD/')
import numpy as np
import matplotlib.pyplot as plt
from read_dcm import DcmRead
import dicom
import SimpleITK as sitk
import os
image_dir = None #the results dir
"""
Input: iamge_sequence: the dce-mri data. the size is mn*t. m and n are related to the row and col of the image.
T is for pixel position and image_size is the size of the single dcm image
function: get curve data from image sequence
"""
def get_data(image_sequence = None, T = None, image_size = None):
    [x, y] = [T[0], T[1]]
    [pixels ,num] = np.shape(image_sequence)
    Data = []
    for i in range(0,num):
        a1 = image_sequence[T[0]*image_size[1] + T[1],i]
        a2 = image_sequence[(T[0]+1)*image_size[1] + T[1],i]
        a3 = image_sequence[(T[0]-1)*image_size[1] + T[1],i]
        a4 = image_sequence[T[0]*image_size[1] + (T[1]+1),i]
        a5 = image_sequence[(T[0]+1)*image_size[1] + (T[1]-1),i]
        a6 = image_sequence[(T[0]-1)*image_size[1] + T[1],i]
        a7 = image_sequence[T[0]*image_size[1] + T[1],i]
        a8 = image_sequence[(T[0]+1)*image_size[1] + (T[1]+1),i]
        a9 = image_sequence[(T[0]-1)*image_size[1] + (T[1]-1),i]
        pixel_data = (a1+a2+a3+a4+a5+a6+a7+a8+a9)/9
        Data.append(pixel_data)
    curve_data = np.array(Data)
    return curve_data

"""
for each col is the intensities of image sequences at one pixel location. 
each row indicates the curve is obtained from different sequences at the same pixel location 
each curve will be shown in different color
"""
def draw(Data = None, lable_name=None,save_loc = None):
    x = np.linspace(1,np.shape(Data)[0],np.shape(Data)[0])
    plt.figure()
    plt.xlabel('time point')
    plt.ylabel('pixel value')
    for i in range(0, np.shape(Data)[1]):
        # draw curve
        y = Data[:, i]
        plt.plot(x,y,"x-",label=lable_name[i])
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.savefig(save_loc)

def getDataFrom_mhd(image_dir,key,mask):
    file_names = os.listdir(image_dir)
    file_names.sort(key = str.lower)
    flag = 0
    data = []
    for fi in file_names:
        if key in fi and 'mhd' in fi:
            #print("read file sequence:"+fi)
            file_name = os.path.join(image_dir,fi) #setting the fixed image
            image_data = sitk.GetArrayFromImage(sitk.ReadImage(file_name))
            image_data = image_data*mask
            image_data = image_data[118:169,67:125]
            data.append(np.reshape(image_data,[image_data.shape[0]*image_data.shape[1],1]))
    array_data = np.array(data)[:,:,0].T
    return array_data

def save_curve(input_dir = None,T_point = None):
    Data = getDataFrom_mhd(input_dir,key='moving')
    curve_data.append(get_data(Data,T = T_point,image_size=[256,256]))
    lable_name.append('moving')
    Data = getDataFrom_mhd(input_dir,key='result')
    curve_data.append(get_data(Data,T = [141,98],image_size=[256,256]))
    lable_name.append('IM_1026')

def draw_hist(input_array = None):
    i = 1
if __name__=="__main__":
    input_dir = "/home/cai/Documents/registration/test/out/lung/my_method/images"
    curve_data = []
    lable_name = []
    save_loc = "../../1.png"
    input_dir = "/home/cai/Documents/registration/test/out/lung/IM_1021/images"
    Data = getDataFrom_mhd(input_dir,key='moving')
    curve_data.append(get_data(Data,T = [141,97],image_size=[256,256]))
    lable_name.append('moving')
    # Data = getDataFrom_mhd(input_dir,key='result')
    # curve_data.append(get_data(Data,T = [141,97],image_size=[256,256]))
    # lable_name.append('IM_1021')

    input_dir = "/home/cai/Documents/registration/test/out/lung/my_method/images"
    Data = getDataFrom_mhd(input_dir,key='result')
    curve_data.append(get_data(Data,T = [141,97],image_size=[256,256]))
    lable_name.append('my_method')

    # input_dir = "/home/cai/Documents/registration/test/out/lung/IM_1046/images"
    # Data = getDataFrom_mhd(input_dir,key='result')
    # curve_data.append(get_data(Data,T = [141,97],image_size=[256,256]))
    # lable_name.append('IM_1046')

    input_dir = "/home/cai/Documents/registration/test/out/lung/IM_1076/images"
    Data = getDataFrom_mhd(input_dir,key='result')
    curve_data.append(get_data(Data,T = [141,97],image_size=[256,256]))
    lable_name.append('IM_1076')

    # input_dir = "/home/cai/Documents/registration/test/out/lung/IM_1066/images"
    # Data = getDataFrom_mhd(input_dir,key='result')
    # curve_data.append(get_data(Data,T = [141,97],image_size=[256,256]))
    # lable_name.append('IM_1066')

    draw(np.array(curve_data).T,lable_name,save_loc='bijiao12.png')

