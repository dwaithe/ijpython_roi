import struct
import tifffile
import ast
from ij_roi import Roi

"""	
Translated from Java source:
https://imagej.nih.gov/ij/developer/source/ij/io/RoiDecoder.java.html

ImageJ/NIH Image 64 byte ROI outline header
	2 byte numbers are big-endian signed shorts
	
	0-3		"Iout"
	4-5		version (>=217)
	6-7		roi type (encoded as one byte)
	8-9		top
	10-11	left
	12-13	bottom
	14-15	right
	16-17	NCoordinates
	18-33	x1,y1,x2,y2 (straight line)
	34-35	stroke width (v1.43i or later)
	36-39   ShapeRoi size (type must be 1 if this value>0)
	40-43   stroke color (v1.43i or later)
	44-47   fill color (v1.43i or later)
	48-49   subtype (v1.43k or later)
	50-51   options (v1.43k or later)
	52-52   arrow style or aspect ratio (v1.43p or later)
	53-53   arrow head size (v1.43p or later)
	54-55   rounded rect arc size (v1.43p or later)
	56-59   position
	60-63   header2 offset
	64-       x-coordinates (short), followed by y-coordinates
"""
VERSION_OFFSET = 4;
TYPE = 6;
TOP = 8;
LEFT = 10;
BOTTOM = 12;
RIGHT = 14;
N_COORDINATES = 16;
X1 = 18;
Y1 = 22;
X2 = 26;
Y2 = 30;
XD = 18;
YD = 22;
WIDTHD = 26;
HEIGHTD = 30;
STROKE_WIDTH = 34;
SHAPE_ROI_SIZE = 36;
STROKE_COLOR = 40;
FILL_COLOR = 44;
SUBTYPE = 48;
OPTIONS = 50;
ARROW_STYLE = 52;
FLOAT_PARAM = 52; #ellipse ratio or rotated rect width
POINT_TYPE= 52;
ARROW_HEAD_SIZE = 53;
ROUNDED_RECT_ARC_SIZE = 54;
POSITION = 56;
HEADER2_OFFSET = 60;
COORDINATES = 64;


C_POSITION = 4;
Z_POSITION = 8;
T_POSITION = 12;
NAME_OFFSET = 16;
NAME_LENGTH = 20;
OVERLAY_LABEL_COLOR = 24;
OVERLAY_FONT_SIZE = 28; #short
AVAILABLE_BYTE1 = 30;  #byte
IMAGE_OPACITY = 31;  #byte
IMAGE_SIZE = 32;  #int
FLOAT_STROKE_WIDTH = 36;  #float
ROI_PROPS_OFFSET = 40;
ROI_PROPS_LENGTH = 44;
COUNTERS_OFFSET = 48;

#subtypes
TEXT = 1;
ARROW = 2;
ELLIPSE = 3;
IMAGE = 4;
ROTATED_RECT = 5;
    
#options
SPLINE_FIT = 1;
DOUBLE_HEADED = 2;
OUTLINE = 4;
OVERLAY_LABELS = 8;
OVERLAY_NAMES = 16;
OVERLAY_BACKGROUNDS = 32;
OVERLAY_BOLD = 64;
SUB_PIXEL_RESOLUTION = 128;
DRAW_OFFSET = 256;
ZERO_TRANSPARENT = 512;





TYPES = {'polygon':0,'rect':1,'oval':2,'line':3,'freeline':4,'polyline':5,
        'noROI':6,'freehand':7,'traced':8,'angle':9,'point':10}





def decode_ij_roi(roi,img_shape):
    xMax = img_shape[1]
    yMax = img_shape[2]
    
    
    
    class ShapeRoi():
        def __init__(self,shapeArray):

            xypoints = shapeArray
        def setName(self,name):
            self.name
    def getStrokeWidthAndColor(roi_b, hdr2Offset):
        strokeWidth = getShort(STROKE_WIDTH);
        if (hdr2Offset>0):
            strokeWidthD = getFloat(hdr2Offset+FLOAT_STROKE_WIDTH);
            if strokeWidthD>0.0:
                strokeWidth = strokeWidthD
        
        if (strokeWidth>0.0):
            roi_b.setStrokeWidth(strokeWidth);
        strokeColor = getInt(STROKE_COLOR);
        if (strokeColor!=0):
            #alpha = (strokeColor>>24)&0xff;
            #roi.setStrokeColor(new Color(strokeColor, alpha!=255));
            roi_b.setStrokeColor(strokeColor)
        
        fillColor = getInt(FILL_COLOR);
        if (fillColor!=0):
            #alpha = (fillColor>>24)&0xff;
            #roi.setFillColor(new Color(fillColor, alpha!=255));
            roi_b.setFillColor(fillColor)
        return

    def getShapeRoi():
        rtype = getByte(TYPE)
        if rtype != TYPES['rect']:
            print ("Invalid composite ROI type")
            return False
        top = getShort(TOP)
        left = getShort(LEFT)
        bottom = getShort(BOTTOM)
        right = getShort(RIGHT)
        width = right-left
        height = bottom-top
        n = getInt(SHAPE_ROI_SIZE)

        shapeArray = []
        base = COORDINATES;
        for i in range (0,n):
            shapeArray[i]= getFloat(base)
            base +=4;
        roi_b = ShapeRoi(shapeArray)
        roi_b.setName(getROIName())
        return roi_b


    def getROIName(roi,HEADER2_OFFSET,NAME_OFFSET,NAME_LENGTH):
        "Function which returns the name of ROI"
        offset = getInt(HEADER2_OFFSET+NAME_OFFSET)
        length = getInt(HEADER2_OFFSET+NAME_LENGTH)

        if offset == 0 and length == 0:
            return ""

        if offset+(length*2) > size:
            return ""
        #print(offset,length,str(roi[offset:offset+(length*2)],'utf-8'))
        return bytearray(roi)[offset:offset+(length*2)].decode('ascii')

    def getShort(st):
        return int.from_bytes(roi[st:st+2], byteorder='big')
    def getUnsignedShort(st):
        return int.from_bytes(roi[st:st+2], byteorder='big')
    def getByte(st):
        return int.from_bytes(roi[st:st+1], byteorder='big')
    def getFloat(st):
        return struct.unpack('!f', roi[st:st+4])[0]
    def getInt(st):
        return int.from_bytes(roi[st:st+4], byteorder='big')


    
    
    size = roi.__len__()
    
    check_byte0 = int.from_bytes(roi[0:1], byteorder='big')
    check_byte1 = int.from_bytes(roi[1:2], byteorder='big')
    
    if (check_byte0 !=73 or check_byte1 !=111):  #"Iout"
        print("This is not an ImageJ ROI");
        return False
    
    mutable_bytes = roi[0:4].decode('utf-8')
    
    version = getShort(VERSION_OFFSET)
    rtype = getByte(TYPE)
    top = getShort(TOP)
    left = getShort(LEFT)
    bottom = getShort(BOTTOM)
    right = getShort(RIGHT)
    width = right-left
    height = bottom-top
    
    #Not sure about this one.
    n = getUnsignedShort(N_COORDINATES)
    options = getShort(OPTIONS)
    position = getInt(POSITION);
    hdr2Offset = getInt(HEADER2_OFFSET)
    channel = 0; sliceZ = 0; frame = 0
    overlayLabelColor =0
    overlayFontSize = 0
    imageOpacity = 0
    imageSize = 0
    
    subPixelResolution = (options and SUB_PIXEL_RESOLUTION)!=0 and  version>=222;
    drawOffset = subPixelResolution and (options and DRAW_OFFSET)!=0;
    subPixelRect = version>=223 and subPixelResolution and (rtype==TYPES['rect'] or rtype==TYPES['oval']);
    
    xd=0.0; yd=0.0; widthd=0.0; heightd=0.0;

    
    
    if subPixelRect:
        xd = getFloat(XD)
        
        yd = getFloat(YD)
        widthd = getFloat(WIDTHD)
        heightd = getFloat(HEIGHTD)
        
    if (hdr2Offset>0 and hdr2Offset+IMAGE_SIZE+4<=size):

        channel = getInt(hdr2Offset+C_POSITION)
        sliceZ = getInt(hdr2Offset+Z_POSITION)
        frame = getInt(hdr2Offset+T_POSITION)
        overlayLabelColor = getInt(hdr2Offset+OVERLAY_LABEL_COLOR)
        overlayFontSize = getInt(hdr2Offset+OVERLAY_FONT_SIZE)
        imageOpacity = getInt(hdr2Offset+IMAGE_OPACITY)
        imageSize = getInt(hdr2Offset+IMAGE_SIZE)
    
    
    isComposite = getInt(SHAPE_ROI_SIZE)>0   
    
    if isComposite:
        print("This script does not yet support ROI which are of type composite.")
        return False
        #TODO
            #roi_b = getShapeRoi();
            #if version>=218:
            #    getStrokeWidthAndColor(roi, hdr2Offset);
            #roi_b.setPosition(position);
            #if channel>0 or sliceZ>0 or frame>0:
            #    roi_b.setPosition(channel, sliceZ, frame);
        #    decodeOverlayOptions(roi, version, options, overlayLabelColor, overlayFontSize);
        #    if (version>=224) {
        #        String props = getRoiProps();
        #        if (props!=null)
        #            roi.setProperties(props);
        #    }
        #    return roi;
        #}
    
    if(rtype == TYPES['rect']):
        if subPixelRect:
            
            roi_b = Roi(xd, yd, widthd, heightd,xMax,yMax)
            roi_b.subPixelRect = True

        else:
            
            roi_b = Roi(left,top, width, height,xMax,yMax)
            roi_b.subPixelRect = False

        arcSize = getShort(ROUNDED_RECT_ARC_SIZE)
        
        if arcSize > 0:
            roi_b.setCornerDiameter(arcSize)
    elif(rtype == TYPES['oval']):
        print("This script does not yet support ROI which are oval.")
        #TODO: oval option.
        return False
    elif(rtype == TYPES['line']):
        print("This script does not yet support ROI which are line.")
        #TODO: line option.
        return False
    elif(rtype == TYPES['polygon']):
        print("This script does not yet support ROI which are polygon.")
        #TODO: polygon option.
        return False
        
    
    roi_b.name =  getROIName(roi,hdr2Offset,NAME_OFFSET,NAME_LENGTH)
 
    if(version>=218):
        getStrokeWidthAndColor(roi_b,hdr2Offset)
    
    
    
  
    roi_b.roiType = rtype
    

    
   


    roi_b.setPosition(position);
    if (channel>0 or sliceZ>0 or frame>0):
        roi_b.setPositionH(channel, sliceZ, frame)


    return roi_b


if __name__ == "__main__":

    pathname2 ="out3.tif"
    tfile = tifffile.TiffFile(pathname2)
    img_shape = ast.literal_eval(tfile.imagej_metadata['Info'].split("\n")[0].split('ImageDescription: ')[1])['shape']



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
    