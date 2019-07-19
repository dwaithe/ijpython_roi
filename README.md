# ImageJ to Python Region-of-Interest (ROI) exchange module.

Python implementation of the ImageJ ROI api:
https://imagej.nih.gov/ij/developer/source/ij/io/RoiDecoder.java.html
The underlying code is similar but not the same. Doing things in Python is different to how you would do it in Java.

This works with the Christoph Gohlke tifffile module:
https://www.lfd.uci.edu/~gohlke/code/tifffile.py.html

This can be installed using pip through:
pip install git+https://github.com/dwaithe/generalMacros/ijPython_roi

Requirements:
- tifffile
- numpy

### Background:
I wanted a way of efficiently encoding ROI into tiff files so that the information could be used interchangeably between ImageJ and Python.

I haven't implemented all the features. At the moment it is possible to encode and decode rectangular regions.




### Example usage Encoder:
```python
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


tifffile.imsave("out5.tiff",im_stk, shape=im_stk.shape,imagej=True,ijmetadata=metadata)



```


### Example usage Decoder:
```python
pathname2 ="out5.tif"
tfile = tifffile.TiffFile(pathname2)
img_shape = tfile.asarray().shape


if 'Overlays' in tfile.imagej_metadata:
    overlays = tfile.imagej_metadata['Overlays']
    if overlays.__class__.__name__ == 'list':
        #Multiple overlays and so iterate.
        for overlay in overlays:
            decode_ij_roi(overlay,img_shape)
    else:
        #One overlay.
        print ('overlays',overlays)
        decode_ij_roi(overlays,img_shape)
else:
    print('no Overlays present in file.')

if 'ROI' in tfile.imagej_metadata:
    print('ROI')
    ROI = tfile.imagej_metadata['ROI']
    decode_ij_roi(ROI,img_shape)
else:
    print("ROI not present in file.")
```
   
