import ijpython_decoder as dec
import tifffile as tifffile
import ast
import struct
import numpy as np
import json
def RGB_encoder(fA,fR,fG,fB):
	bA = (fA).to_bytes(1, 'big') #ALPHA 0-255
	bR = (fR).to_bytes(1, 'big') #RED  0-255
	bG = (fG).to_bytes(1, 'big') #GREEN  0-255
	bB = (fB).to_bytes(1, 'big') #BLUE  0-255
	return int.from_bytes(bA+bR+bG+bB, byteorder='big')
def encode_ij_roi(roi_b):
	HEADER_SIZE = 64
	HEADER2_SIZE = 64
	VERSION = 227 # v1.50d (point counters)


	TYPES = {'polygon':0,'rect':1,'oval':2,'line':3,'freeline':4,'polyline':5,
		'noROI':6,'freehand':7,'traced':8,'angle':9,'point':10}
	


	


	def write(roi_b):
		def putShort(loc,num):
			dt = (num).to_bytes(2, 'big')
			data[loc:loc+2] = dt
		def putChar(loc,num):
			dt = struct.pack('!c', num)
			data[loc:loc+1] = dt
		def putByte(loc,num):
			dt = (num).to_bytes(1, 'big')
			data[loc:loc+1] = dt
		def putInt(loc,num):
			dt = (num).to_bytes(4, 'big')
			data[loc:loc+4] = dt
		def putFloat(loc,num):
			dt = struct.pack('!f', num)
			data[loc:loc+4] = dt
		def putName(loc, roiName,hdr2Offset):
			offset = hdr2Offset+HEADER2_SIZE
			nameLength = roiName.__len__()
			putInt(hdr2Offset+dec.NAME_OFFSET, offset)
			putInt(hdr2Offset+dec.NAME_LENGTH, nameLength)
			for i in range(0, nameLength):
				putShort(offset+i*2, ord(roiName[i]))
		def saveStrokeWidthAndColor(roi_b):
			stroke = roi_b.getStroke()
			print("stroke",stroke)
			if stroke != None:
				putShort(dec.STROKE_WIDTH, stroke.getLineWidth())
			strokeColor = roi_b.getStrokeColor()
			print("strokeColor",strokeColor)
			if strokeColor != None:
				putInt(dec.STROKE_COLOR, strokeColor)
			fillColor = roi_b.getFillColor()
			print("fillColor",fillColor)
			if fillColor != None:
				putInt(dec.FILL_COLOR, fillColor)

		def putHeader2(roi_b, hdr2Offset):
			putInt(dec.HEADER2_OFFSET,hdr2Offset)
			putInt(hdr2Offset+dec.C_POSITION, roi_b.getCPosition())
			
			if roi_b.hasHyperStackPosition() == True:
				zpos = roi_b.getZPosition()
			else:
				zpos = 0
			
			putInt(hdr2Offset+dec.Z_POSITION, zpos)
			putInt(hdr2Offset+dec.T_POSITION, roi_b.getTPosition())
			proto = roi_b.getPrototypeOverlay
			overlayLabelColor = roi_b.overlayLabelColor
			if overlayLabelColor!=None:
				putInt(hdr2Offset+dec.OVERLAY_LABEL_COLOR, overlayLabelColor.getRGB())
			font = roi_b.getFontLabelColor()
			if font != None:
				putShort(hdr2Offset+dec.OVERLAY_FONT_SIZE, font.getSize())
			if roiNameSize >0:
				putName(roi_b,roi_b.name,hdr2Offset)
			strokeWidth = roi_b.getStrokeWidth()
			if roi_b.getStroke() == None:
				strokeWidth = 0.0
			putFloat(hdr2Offset+dec.FLOAT_STROKE_WIDTH, strokeWidth)
			if roiPropsSize >0:
				putProps(roi_b, hdr2Offset)
			if countersSize >0:
				putPointCounters(roi,hdr2Offset)
		def saveOverlayOptions(roi_b, options):
			#TODO finish saveOVerlayOptions
			print('TODO do overlay')
			return False

			#proto = roi_b.getPrototypeOverlay()
			#if (proto.getDrawLabels()):
			#	options |= dec.OVERLAY_LABELS
			#if (proto.getDrawNames()):
			#	options |= dec.OVERLAY_NAMES
			#if (proto.getDrawBackgrounds()):
			#	options |= dec.OVERLAY_BACKGROUNDS
			#font = proto.getLabelFont()
			#if (font!=None and font.getStyle() == Font.BOLD):
			#	options |= RoiDecoder.OVERLAY_BOLD
			#putShort(dec.OPTIONS, options)

		if  isinstance(roi_b.x, float):
			roi_b.enableSubPixelResolution()
		rtype = TYPES['rect']
		roiType = roi_b.getType() 

		roiName = roi_b.getName()
		if roiName != None:
			roiNameSize = roiName.__len__()*2;
		else:
			roiNameSize = 0

		roiProps = roi_b.getProperties()
		if (roiProps!=None):
			roiPropsSize = roiProps.__len__()*2;
		else:
			roiPropsSize = 0;

		n = 0
		options = 0
		x = None;y = None
		xf = []; yf = []
		floatSize = 0
		if roi_b.polygonROI:
			#TODO add options for polygon ROI.
			print('polygonROI are not ready yet.')
			return False



		countersSize = 0;


		# Python 3
		data = bytearray(HEADER_SIZE+HEADER2_SIZE+(n*4)+floatSize+roiNameSize+roiPropsSize+countersSize)
		data[0]=73; data[1]=111; data[2]=117; data[3]=116; # "Iout"

		putShort(dec.VERSION_OFFSET,VERSION)
		putByte(dec.TYPE,roiType) 
		putShort(dec.TOP, int(roi_b.y))
		putShort(dec.LEFT, int(roi_b.x))
		putShort(dec.BOTTOM, int(roi_b.y+roi_b.height))
		putShort(dec.RIGHT, int(roi_b.x+roi_b.width));
		

		print('roi_b.subPixelRect',roi_b.subPixelRect)
		if roi_b.subPixelRect and (rtype==TYPES['rect'] or rtype==TYPES['oval']):
			
			p = roi_b.getFloatPolygon()
			if p['npoints'] == 4:
				print('pppppp',p)
				putFloat(dec.XD, p['xpoints'][0])
				putFloat(dec.YD, p['ypoints'][0])
				putFloat(dec.WIDTHD, p['xpoints'][1]- p['xpoints'][0])
				putFloat(dec.HEIGHTD, p['ypoints'][2]- p['ypoints'][1])
				options |= dec.SUB_PIXEL_RESOLUTION;
				putShort(dec.OPTIONS,options)


				print(data)
		if n > 65535:
			if (rtype==TYPES['polygon'] or rtype==TYPES['freehand'] or rtype==TYPES['traced']):
				name = roi_b.getName()
				#TODO: start new shapeROI.
				#roi = new ShapeRoi(roi);
				#if (name!=null) roi.setName(name);
				#saveShapeRoi(roi, rect, f, options);
				#return;
			
			
			print("Non-polygonal selections with more than 65k points cannot be saved.");
			n = 65535;
		
		putShort(dec.N_COORDINATES, n);
		putInt(dec.POSITION,roi_b.getPosition())

		if rtype==TYPES['rect']:
		
			arcSize = roi_b.getCornerDiameter()
			if arcSize >0:
				putShort(dec.ROUNDED_RECT_ARC_SIZE,arcSize)

		if roi_b.Line:
			#TODO add options for line ROI.
			print('line ROI are not ready yet.')
			return False
		if roi_b.PointRoi:
			#TODO add options for PointRoi ROI.
			print('point ROI are not ready yet.')
			return False
		if roi_b.RotatedRectRoi or roi_b.EllipseRoi:
			#TODO add options for RotatedRectRoi and EllipseRoi ROI.
			print('RotatedRectRoi nor EllipseRoi are not ready yet.')
			return False


		if VERSION >= 218:
			saveStrokeWidthAndColor(roi_b)
			if roi_b.polygonROI and roi_b.isSplineFit():
				options |= dec.SPLINE_FIT
				putShort(dec.OPTIONS,options)

		if n == 0 and roi_b.TextRoi:
			saveTextRoi(roi_b)
		elif n==0 and roi_b.ImageRoi:
			options = saveImageRoi(roi_b, options)
		else:
			print('colours')
			putHeader2(roi_b, HEADER_SIZE+n*4+floatSize)

		if n>0:
			base1 = 64
			base2 = base1+2*n
			for i in range(0,n):
				putFloat(base1+1*4, x[i])
				putFloat(base2+1*4, y[i])
			if xf != None:
				base1 = 64+4*n
				base2 = base1+4*n
				for i in range(0,n):
					putFloat(base1+1*4, xf[i])
					putFloat(base2+1*4, yf[i])

		saveOverlayOptions(roi_b,options)
		print(data)
		return data

	return write(roi_b)

if __name__ == "__main__":

	pathname2 ="out3.tif"
	tfile = tifffile.TiffFile(pathname2)
	img_shape = ast.literal_eval(tfile.imagej_metadata['Info'].split("\n")[0].split('ImageDescription: ')[1])['shape']


	overlays_o = []
	count =0 
	if 'Overlays' in tfile.imagej_metadata:
		overlays = tfile.imagej_metadata['Overlays']
		if overlays.__class__.__name__ == 'list':
			#Multiple overlays and so iterate.
			for overlay in overlays:
				print('counter',count)
				count +=1
				roi_b = dec.decode_ij_roi(overlay,img_shape)
				data = encode_ij_roi(roi_b)
				overlays_o.append(data)
		else:
			#One overlay.
			roi_b = dec.decode_ij_roi(overlays,img_shape)
			data = encode_ij_roi(roi_b)
			overlays_o.append(data)
	else:
		print('no Overlays present in file.')

	
	if 'ROI' in tfile.imagej_metadata:
		print('ROI')
		ROI = tfile.imagej_metadata['ROI']
		roi_b = dec.decode_ij_roi(ROI,img_shape)
		data = encode_ij_roi(roi_b)
		dec.decode_ij_roi(data,img_shape)
	else:
		print("ROI not present in file.")

	

	print('rrrrr',tfile.imagej_metadata)
	print('wwwwwwwwwwwwwwwwww')

	im_stk = tfile.asarray()
	ijm = tfile.imagej_metadata
	metadata = {'hyperstack': ijm['hyperstack'] ,'slices': ijm['slices'], 'images': ijm['images'], 'ImageJ': '1.52g', 'Overlays':overlays_o , 'ROI':data,'loop': ijm['loop']}
	#metadata['channels'] = tfile.imagej_metadata['channels']
	#meta['Overlays'] = ''
	#meta['ROI'] = ''
	
	tifffile.imsave("/Users/dwaithe/Desktop/out4.tiff",im_stk, imagej=True, ijmetadata=metadata)

	print('bbbbbbbbbbbbbbbbbb')

	pathname2 ="/Users/dwaithe/Desktop/out4.tiff"
	#pathname2 = 'out3.tif'
	tfile = tifffile.TiffFile(pathname2)
	#tfile.imagej_metadata = meta
	print(tfile.imagej_metadata)

	