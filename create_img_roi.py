from ij_roi import Roi
from ijpython_encoder import encode_ij_roi, RGB_encoder
import numpy as np
import tifffile

im_stk = np.zeros((100,1,512,512)).astype(np.float32)


data = []
roi_b = Roi(30,40,140,120, im_stk.shape[2],im_stk.shape[3],0)
roi_b.name = "Region 1"
roi_b.roiType = 1
roi_b.position = 10
roi_b.strokeLineWidth = 3.0
roi_b.strokeColor = RGB_encoder(255,0,255,255)

data.append(encode_ij_roi(roi_b))

roi_b = Roi(130,140,140,120, im_stk.shape[2],im_stk.shape[3],0)
roi_b.name = "Region 1"
roi_b.roiType = 1
roi_b.position = 10
roi_b.strokeLineWidth = 3.0
roi_b.strokeColor = RGB_encoder(255,0,0,255)


data.append(encode_ij_roi(roi_b))




metadata = {'hyperstack': True ,'slices': 100,'channels':1, 'images': 100, 'ImageJ': '1.52g', 'Overlays':data , 'loop': False}
#metadata['channels'] = tfile.imagej_metadata['channels']
#meta['Overlays'] = ''
#meta['ROI'] = ''

tifffile.imsave("/Users/dwaithe/Desktop/out5.tiff",im_stk, shape=im_stk.shape,imagej=True,ijmetadata=metadata)


pathname2 ="/Users/dwaithe/Desktop/out5.tiff"
#pathname2 = 'out3.tif'
tfile = tifffile.TiffFile(pathname2)
#tfile.imagej_metadata = meta
print(tfile.imagej_metadata)