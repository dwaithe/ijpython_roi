from ijroi.ij_roi import Roi
from ijroi.ijpython_encoder import encode_ij_roi, RGB_encoder
from ijroi.ijpython_decoder import decode_ij_roi
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

#Shows how to create mask image.
img = np.zeros((img_shape))
for i in range(0,overlay_arr.__len__()):

    if overlay_arr[i] != False:
        x0 = overlay_arr[i].x
        y0 = overlay_arr[i].y
        wid = overlay_arr[i].width
        hei = overlay_arr[i].height
        img[y0:y0+hei, x0:x0+wid] = overlay_arr[i].getMask()
   
    
plt.imshow(img)
plt.show()