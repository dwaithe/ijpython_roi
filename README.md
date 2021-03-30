# ImageJ Region-of-Interest (ROI) Python Tiff exchange module.

Python implementation of the ImageJ ROI API:
https://imagej.nih.gov/ij/developer/source/ij/io/RoiDecoder.java.html
The underlying code is similar but not the same. Doing things in Python is different to how you would do it in Java. Many of the functions implemented in the Java API are not needed for the Python. The goal is provide coordinates and pixel masks from the main ROI types. 

This works with the Christoph Gohlke tifffile module:
https://www.lfd.uci.edu/~gohlke/code/tifffile.py.html

This can be installed using pip through:
python -m pip install ijroipytiff

Requirements:
- tifffile
- numpy

### Background:
I wanted a way of efficiently encoding ROI into tiff files so that the information could be used interchangeably between ImageJ and Python.





### Example usage Encoder:
```python

from ijroipytiff.ij_roi import Roi
from ijroipytiff.ijpython_encoder import encode_ij_roi,  RGB_encoder
import numpy as np
import tifffile

im_stk = np.zeros((100, 1, 512, 512)).astype(np.float32)


data = []
roi_b = Roi(30, 40, 140, 120, im_stk.shape[2], im_stk.shape[3], 0)
roi_b.name = "Region 1"
roi_b.roiType = 1
roi_b.position = 10
roi_b.strokeLineWidth = 3.0
roi_b.strokeColor = RGB_encoder(255, 0, 255, 255)

data.append(encode_ij_roi(roi_b))

roi_b = Roi(130, 140, 140, 120, im_stk.shape[2], im_stk.shape[3], 0)
roi_b.name = "Region 1"
roi_b.roiType = 1
roi_b.position = 10
roi_b.strokeLineWidth = 3.0
roi_b.strokeColor = RGB_encoder(255, 0, 0, 255)

data.append(encode_ij_roi(roi_b))

metadata = {'hyperstack': True ,'slices': 100, 'channels':1, 'images': 100, 'ImageJ': '1.52g', 'Overlays':data , 'loop': False}

tifffile.imsave("out4.tiff", im_stk, shape=im_stk.shape, imagej=True, ijmetadata=metadata)


```


### Example usage Decoder:
```python

import tifffile
import numpy as np
from ijroipytiff.ij_roi import Roi
from ijroipytiff.ijpython_decoder import decode_ij_roi

from ijroipytiff.ij_ovalroi import OvalRoi
import pylab as plt

pathname2 ="out4.tiff"
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
        img[5,y0:y0+hei, x0:x0+wid] = overlay_arr[i].getMask()
   
    
plt.imshow(img[5,:,:])
plt.show()
```
