# perform Dmd method to the given image sequence. extract and save the slow modes as the reference image

from read_dcm import DcmRead
from PyDMD import DMD
import numpy as np
import time
from past.utils import old_div
import SimpleITK as sitk
import matplotlib.pyplot as plt
import sys
from DCE_tools import simulate_motion as sm
# root_location = '/home/cai/Documents/data_set/DICOMfiles/p01104954/test'# image sequences directory
# reference_image = '/home/cai/Documents/result/zi_gong/'# the loc that used to save reference images
#
# dcm = DcmRead(dir_files=root_location, key_word="IM")
# Data = dcm.read_images()
#
# print("perform dmd on the image sequence")
# sizem = 576
# sizen = 576
# dmd = DMD(svd_rank=-1)
# dmd_info = dmd.fit(X=Data[:,0:-2])
# index = np.argsort(np.abs(old_div(np.log(dmd_info.eigs), (2. * np.pi))))
# slow_mode_index = index < 1
#
# single_mode = np.reshape(dmd_info.modes[:,0],[sizem,sizen])
# reference = sitk.GetImageFromArray(np.abs(single_mode))
# sitk.WriteImage(reference, reference_image+'slow_mode1.mha')
#
# single_mode = np.reshape(dmd_info.modes[:,1],[sizem,sizen])
# reference = sitk.GetImageFromArray(np.abs(single_mode))
# sitk.WriteImage(reference, reference_image+'slow_mode2.mha')
#
# single_mode = np.reshape(dmd_info.modes[:,2],[sizem,sizen])
# reference = sitk.GetImageFromArray(np.abs(single_mode))
# sitk.WriteImage(reference, reference_image+'slow_mode3.mha')

Data = sm.create_sample_data()
dmd = DMD(svd_rank=-1)
dmd_info = dmd.fit(X=Data.T)
index = np.argsort(np.abs(old_div(np.log(dmd_info.eigs), (2. * np.pi))))
slow_mode_index = index < 1

# modes = dmd_info.modes[:, slow_mode_index]
# eigs = dmd_info.eigs[slow_mode_index]
# re_images = dmd.recon_fn_data(modes, eigs)
# single = np.reshape(re_images[:,0],[sizem,sizen])
# single_mode = np.reshape(modes,[sizem,sizen])
# reference = sitk.GetImageFromArray(np.abs(single_mode))
# sitk.WriteImage(reference, reference_image+'slow_mode.mha')
# single_image = np.reshape(Data[:,0],[sizem,sizen])
# image = sitk.GetImageFromArray(np.abs(single_image))
# sitk.WriteImage(image,reference_image+'moving.mha')
