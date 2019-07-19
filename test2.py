from ij_roi import Roi
from ijpython_encoder import encode_ij_roi, RGB_encoder
from ijpython_decoder import decode_ij_roi
import numpy as np
import tifffile
import pylab as plt

pathname2 ="out4.tif"
tfile = tifffile.TiffFile(pathname2)
img_shape = tfile.asarray().shape


overlay_arr = []
if 'Overlays' in tfile.imagej_metadata:
    overlays = tfile.imagej_metadata['Overlays']
    if overlays.__class__.__name__ == 'list':
        #Multiple overlays and so iterate.
        for overlay in overlays:
            
            overlay_arr.append(decode_ij_roi(overlay,img_shape))
    else:
        #One overlay.
            overlay_arr.append(decode_ij_roi(overlays,img_shape))
else:
    print('no Overlays present in file.')

if 'ROI' in tfile.imagej_metadata:
    print('ROI')
    ROI = tfile.imagej_metadata['ROI']
    decode_ij_roi(ROI,img_shape)
else:
    print("ROI not present in file.")

for i in range(0,overlay_arr.__len__()):
	print(overlay_arr[i].getMask())
	
	plt.imshow(overlay_arr[i].getMask())
	plt.show()