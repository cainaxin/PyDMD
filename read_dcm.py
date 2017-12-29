"""
read and imshow dicom files
"""
# import matplotlib
# matplotlib.use('Qt4Agg')
import dicom
import pylab
import numpy as np
import os

# read dcm images from files


class DcmRead:
    """
    dir_files: folder path
    keyword:
    """
    def __init__(self, dir_files=None, key_word=None):
        self.dir_files = dir_files
        self.key_word = key_word
        self.filename = None
        self.shape = (0, 0)
    """
    read the folder
    """

    def hide_name(self):
        # hide patient name and save the new image to the sub-folder
        files = os.listdir(self.dir_files)
        files.sort(key = str.lower)
        for fi in files:
            fi_d = os.path.join(self.dir_files, fi)
            if self.key_word in fi_d:
                ds = dicom.read_file(fi_d)
                ds.PatientsName = 'anonymized'
                ds.save_as(self.dir_files+'/hide_name/'+fi)

    def read_images(self):
        # initialization
        files = os.listdir(self.dir_files)
        files.sort(key = str.lower)
        count = 0
        count_no_dcm = 0
        d_images = None
        rows = 0
        cols = 0
        ds = None
        self.filename = files
        for fi in files:
            fi_d = os.path.join(self.dir_files, fi)
            if self.key_word in fi_d:
                ds = dicom.read_file(fi_d)
                if count <= 0:
                    rows = ds.pixel_array.shape[0]
                    cols = ds.pixel_array.shape[1]
                    d_images = np.zeros((rows * cols, int(len(files) - count_no_dcm)))
                origin_data = ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept #edited by cnx 2017/12/28 read the origin data from dicom
                d_images[:, count] = np.reshape(origin_data, (rows * cols))
                count += 1
            else:
                count_no_dcm += 1
        self.shape = ds.pixel_array.shape
        return d_images

    def read_dcm_data(self, filename):
        name = self.dir_files+'/'+filename
        ds = None
        if os.path.isfile(name):
            ds = dicom.read_file(name)
        else:
            print("file dose not exist")
        #return ds.pixel_array
        return ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept #edited by cnx 2017/12/28 read the origin data from dicom

    """
    show single dcm data
    """
    def show_dcm(self, filename):
        if self.read_dcm_data(filename=filename).any() != 0:
            pylab.imshow(self.read_dcm_data(filename=filename), cmap='gray')
            pylab.show()
    """
    save image sequence for png format
    """
    def save_dcm_sequence(self, images, save_location='result'):
        count = 0
        if os.path.isdir(save_location):
            pass
        else:
            os.mkdir(save_location)
        [row, col] = np.shape(images)
        for fi in self.filename:
            name = self.dir_files+'/'+fi
            if self.key_word in name:
                image = np.abs(np.reshape(images[:, count], self.shape))
                pylab.imshow(image, cmap='gray')
                pylab.savefig(save_location+'/'+fi)
                count += 1
                if count >= col:
                    break

    def save_data_sequence(self, images, save_location='result', name=None):
        count = 0
        if os.path.isdir(save_location):
            pass
        else:
            os.mkdir(save_location)
        [row, col] = np.shape(images)
        for i in range(0,col):
                image = np.abs(np.reshape(images[:, i], self.shape))
                pylab.imshow(image, cmap='gray')
                pylab.savefig(save_location + '/'+name[i])

    @staticmethod
    def normalize_data(Data):
        pData = abs(Data)
        min_data = np.tile(pData.min(0), [pData.shape[0], 1])
        max_data = np.tile(pData.max(0), [pData.shape[0], 1])
        norm_data = (pData - min_data) / (max_data - min_data)
        return norm_data



