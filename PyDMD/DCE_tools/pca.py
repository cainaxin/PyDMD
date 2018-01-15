# use the pca to evaluate the registration results
#  -*- coding: utf-8 -*
import numpy as np
import ti_curve as tc
import SimpleITK as sitk
import pylab
import cv2
#零均值化
def zeroMean(dataMat):
    meanVal=np.mean(dataMat,axis=0)     #按列求均值，即求各个特征的均值
    newData=dataMat-meanVal
    return newData,meanVal

def pca(dataMat,n):
    newData,meanVal=zeroMean(dataMat)
    covMat=np.cov(newData,rowvar = False)    #求协方差矩阵,return ndarray；若rowvar非0，一列代表一个样本，为0，一行代表一个样本

    eigVals,eigVects=np.linalg.eig(np.mat(covMat))#求特征值和特征向量,特征向量是按列放的，即一列代表一个特征向量
    eigValIndice=np.argsort(eigVals)            #对特征值从小到大排序
    n_eigValIndice=eigValIndice[-1:-(n+1):-1]   #最大的n个特征值的下标
    n_eigVect=eigVects[:,n_eigValIndice]        #最大的n个特征值对应的特征向量
    lowDDataMat=newData*n_eigVect               #低维特征空间的数据
    reconMat=(lowDDataMat*n_eigVect.T)+meanVal  #重构数据
    return lowDDataMat,reconMat

def pca_eig(dataMat):
    newData,meanVal=zeroMean(dataMat)
    covMat=np.cov(newData,rowvar = False)    #求协方差矩阵,return ndarray；若rowvar非0，一列代表一个样本，为0，一行代表一个样本

    eigVals,eigVects=np.linalg.eig(np.mat(covMat))#求特征值和特征向量,特征向量是按列放的，即一列代表一个特征向量
    eigValIndice=np.argsort(eigVals)            #对特征值从小到大排序
    return eigValIndice

def draw_hist(dataMat):
    print("under edited")

if __name__=="__main__":
    mask_dir = '/home/cai/Documents/registration/test/input/mask.mha'
    mask_image = np.array(sitk.GetArrayFromImage(sitk.ReadImage(mask_dir)))[0,:,:]

    input_dir = '/home/cai/Documents/registration/test/out/lung/IM_1061/images'
    image_array = tc.getDataFrom_mhd(input_dir,key= 'result',mask = mask_image)

    new_data,mean = zeroMean(image_array.T)
    #eig = pca_eig(new_data)
    U,S,V = np.linalg.svd(new_data,full_matrices=False)
    eig = np.array(sorted(abs(S),reverse = True))
    x = (eig/np.sum(eig))
    print( x.round(3))
    input_dir = '/home/cai/Documents/registration/test/out/lung/my_method/images'
    image_array = tc.getDataFrom_mhd(input_dir,key= 'result',mask = mask_image)

    new_data,mean = zeroMean(image_array.T)
    #eig = pca_eig(new_data)
    U,S,V = np.linalg.svd(new_data,full_matrices=False)
    eig2 = np.array(sorted(abs(S),reverse = True))
    x = eig2/np.sum(eig2)
    print(x.round(3))
