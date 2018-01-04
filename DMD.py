# perform Dmd method to the given image sequence. extract and save the slow modes as the reference image

from read_dcm import DcmRead
from PyDMD import DMD
import numpy as np
import time
from past.utils import old_div
import SimpleITK as sitk
import matplotlib.pyplot as plt

root_location = '../data_set/lung'# image sequences directory
reference_image = '/home/cai/Desktop/'# the loc that used to save reference images

dcm = DcmRead(dir_files=root_location, key_word="IM")
Data = dcm.read_images()

print("perform dmd on the image sequence")

dmd = DMD(svd_rank=-1)
dmd_info = dmd.fit(X=Data)
index = np.argsort(np.abs(old_div(np.log(dmd_info.eigs), (2. * np.pi))))
slow_mode_index = index < 1
modes = dmd_info.modes[:, slow_mode_index]
eigs = dmd_info.eigs[slow_mode_index]
re_images = dmd.recon_fn_data(modes, eigs)
single = np.reshape(re_images[:,0],[256,256])
single_mode = np.reshape(modes,[256,256])
reference = sitk.GetImageFromArray(np.abs(single_mode))
sitk.WriteImage(reference, reference_image+'slow_mode.mhd')
single_image = np.reshape(Data[:,0],[256,256])
image = sitk.GetImageFromArray(np.abs(single_image))
sitk.WriteImage(image,reference_image+'moving.mhd')
