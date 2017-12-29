# -*- coding:utf-8 -*-
import matplotlib

# import nose
#
matplotlib.use('agg')
#
from read_dcm import DcmRead
from PyDMD import DMD
import numpy as np
import time
from past.utils import old_div
import SimpleITK as sitk
import matplotlib.pyplot as plt

# the root location that used for saving results
root_location = 'result/lung/'
# the loc that used to save origin images
origin_loc = 'original_images'
# the loc that used to save step one results
low_rank_loc = 'low_rank_images'
sparse_loc = 'sparse_images'
# the loc that used to save step two results
rec_loc = 'reconstructed_images'
each_mode_loc = 'low_rank_mode'
win_size = 3
# num of modes that used to reconstructed
first_n_modes = 0
time1 = time.time()
for first_n_modes in range(1,15):
    print('...'+str(first_n_modes)+'...')
    time2 = time.time()
    print(time2 - time1)
    dcm = DcmRead(dir_files="data_set/lung", key_word="IM")
    Data = dcm.read_images()
    """
    step one windowed DMD, sampling rate: 3
    """
    print('begin step one')
    threshold = 1
    dmd = DMD(svd_rank=-1)
    # creating a list for storing modes and eigs
    modes = None
    eig = None
    low_rank_modes = []
    sparse_modes = []
    # normalize each col of the image data
    norm_data = dcm.normalize_data(Data)
    # if first_n_modes == 1:
    #     dcm.save_dcm_sequence(norm_data, save_location=root_location+origin_loc)
    for i in range(0, Data.shape[1]-win_size+1):
        Data_win = norm_data[:, i:i+win_size]
        dmd_info = dmd.fit(X=Data_win)
        # sort the array in descending order
        index = np.argsort(np.abs(old_div(np.log(dmd_info.eigs), (2. * np.pi))))
        # select first n slow modes
        slow_mode_index = index < threshold
        # eig = dmd_info.eigs[slow_mode_index]
        modes = dmd_info.modes[:, slow_mode_index]
        sparse = dmd_info.modes[:, ~slow_mode_index]
        low_rank_modes.append(modes)
        sparse_modes.append(sparse[:, -1])

    # save low_rank_images and sparse images
    low_rank_images = np.array(low_rank_modes)[:, :, 0].T
    sparse_images = np.array(sparse_modes).T
    if first_n_modes == 1:
        norm_low_rank_images = dcm.normalize_data(low_rank_images)
        norm_sparse_images = dcm.normalize_data(sparse_images)
        dcm.save_dcm_sequence(norm_low_rank_images, save_location=root_location+low_rank_loc+'w_'+str(win_size))
        dcm.save_dcm_sequence(norm_sparse_images, save_location=root_location+sparse_loc+'w_'+str(win_size))
    """
    step two: apply dmd to the reconstructed images and then extracted the first three low frequency modes
    """
    print('begin step two')
    modes_st = None
    dmd_step_two = dmd.fit(X=low_rank_images)
    # sort the array in increasing order
    index = np.argsort(np.abs(old_div(np.log(dmd_step_two.eigs), (2. * np.pi))))
    slow_mode_index = index < first_n_modes
    modes_step_two = dmd_step_two.modes[:, slow_mode_index]
    eigs_step_two = dmd_step_two.eigs[slow_mode_index]
    re_images = dmd.recon_fn_data(modes_step_two, eigs_step_two)
    # norm_re_images = dcm.normalize_data(re_images)
    dcm.save_dcm_sequence(re_images, save_location=root_location+rec_loc+'w_'+str(win_size)+'st_'+str(first_n_modes))

    # save each slow mode/low rank image in terms of increasing order
    num = np.shape(index)[0]
    image_list = []
    name = []
    print('the num of images are:'+str(num))
    for i in range(0, num):
        mode_index = index == i
        mode = dmd_step_two.modes[:, mode_index]
        image_list.append(mode)
        name.append(str(i))
    images = np.array(image_list)[:, :, 0].T
    loc = root_location+each_mode_loc+'w_'+str(win_size)+'st_'+str(first_n_modes)
    if first_n_modes == 1:
        dcm.save_data_sequence(images, save_location=loc, name=name)





