import SimpleITK as sitk
import dicom
import numpy as np
import pylab
# fixedImage3d = sitk.ReadImage('/home/cai/Desktop/exampleinput/fixed.mhd')
# fixedImage2d = sitk.Extract(fixedImage3d, (fixedImage3d.GetWidth(), fixedImage3d.GetHeight(), 0), (0, 0, 0))
# movingImage3d = sitk.ReadImage('/home/cai/Desktop/exampleinput/moving.mhd')
# movingImage2d = sitk.Extract(movingImage3d, (movingImage3d.GetWidth(), movingImage3d.GetHeight(), 0), (0, 0, 0))

ds = dicom.read_file('/home/cai/Desktop/IM_1080.dcm')  # Read file
fixedImage2d = sitk.GetImageFromArray(ds.pixel_array)  # Convert to sitk.Image
ds = dicom.read_file('/home/cai/Desktop/IM_1021.dcm')  # Read file
movingImage2d = sitk.GetImageFromArray(ds.pixel_array)  # Convert to sitk.Image

affine_parameterMap = sitk.GetDefaultParameterMap("affine")
bspline_parameterMap = sitk.GetDefaultParameterMap("bspline")
affine_parameterMap['ResultImageFormat'] = ['mhd']
bspline_parameterMap['ResultImageFormat'] = ['mhd']
affine_parameterMap['MaximumNumberOfIterations'] = ['200']
bspline_parameterMap['MaximumNumberOfIterations'] = ['200']
elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetFixedImage(fixedImage2d)
elastixImageFilter.SetMovingImage(movingImage2d)
bspline_parameterMap['Metric0Weight'] = ['1']
bspline_parameterMap['Metric1Weight'] = ['1']
bspline_parameterMap['Metric'] = ['NormalizedMutualInformation','TransformBendingEnergyPenalty']
affine_parameterMap['Metric'] = ['NormalizedMutualInformation']
bspline_parameterMap['NumberOfResolutions'] = ['3']
bspline_parameterMap['GridSpacingSchedule'] = ['1.988100','1.410000', '1.000000']

elastixImageFilter.SetParameterMap(affine_parameterMap)
elastixImageFilter.AddParameterMap(bspline_parameterMap)
elastixImageFilter.LogToFileOn()
elastixImageFilter.SetOutputDirectory('/home/cai/Desktop')
elastixImageFilter.SetLogFileName('cnx')
a = elastixImageFilter.GetParameterMap()
elastixImageFilter.WriteParameterFile(bspline_parameterMap,'/home/cai/Desktop/bspling')
elastixImageFilter.WriteParameterFile(affine_parameterMap,'/home/cai/Desktop/affine')
print("_______________________________-")
elastixImageFilter.PrintParameterMap()
print("_______________________________-")
elastixImageFilter.Execute()

# sitk.WriteImage(elastixImageFilter.GetResultImage())
# ds = dicom.read_file('/home/cai/Desktop/IM_1021.dcm')
result_Image = elastixImageFilter.GetResultImage()
sitk.WriteImage(movingImage2d,'/home/cai/Desktop/fix.mha')
sitk.WriteImage(result_Image,'/home/cai/Desktop/result_image.mha')
sitk.WriteImage(fixedImage2d,'/home/cai/Desktop/moving.mha')
# result_array = sitk.GetArrayFromImage(resultImage)
# pylab.figure(2)
# pylab.imshow(result_array)
#
# transformParameterMap = elastixImageFilter.GetTransformParameterMap()

# transformixImageFilter = sitk.TransformixImageFilter()
# transformixImageFilter.SetTransformParameterMap(transformParameterMap)
#
# transformixImageFilter.SetMovingImage(movingImage2d)
# transformixImageFilter.Execute()
#sitk.WriteImage(result_Image, '/home/cai/Desktop/result_image.dcm')
