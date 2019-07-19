
import numpy as np
RECTANGLE = 0
NORMAL = 3           

class Roi(object):
      def __init__(self,x,y,width,height,xMax,yMax,cornerDiameter=0):
            if width  < 1: width=1
            if height < 1: height=1
            if width  > xMax: width=xMax
            if height > yMax: height=yMax
            self.cornerDiameter = cornerDiameter
            self.x = x
            self.y = y
            startX = x; startY = y;
            oldX = x; oldY = y; oldWidth=0; oldHeight=0;
            self.width = width
            self.height = height
            self.name = None
            self.properties = None
            self.roiType = None
            self.subPixelRect = False
            self.position = 0

            self.polygonROI = False
            self.TextRoi = False
            self.ImageRoi = False
            self.RotatedRectRoi = False
            self.EllipseRoi = False
            self.PointRoi = False
            self.Line = False

            self.stroke = None
            self.strokeLineWidth = None
            self.strokeColor = None

            self.fillColor = None

            self.prototypeOverlay = None
            self.protoOverlay = None
            self.overlayLabelColor = None

            self.fontLabelColor = None

            self.hyperstackPosition = False

            self.channel = 0
            self.slice = 0
            self.frame = 0 



            oldWidth = width
            oldHeight = height
            clipX = x
            clipY = y
            clipWidth = width
            clipHeight = height
            state = NORMAL
            state = RECTANGLE
            fillColor = 'default'
      def getName(self):
            return self.name
      def getFontLabelColor(self):
            return self.fontLabelColor
      def getType(self):
            return self.roiType
      def setStrokeColor(self, strokeColor):
            self.strokeColor = strokeColor
      def getStrokeColor(self):
            return self.strokeColor
      def setFillColor(self,fillColor):
            self.fillColor = fillColor
      def getFillColor(self):
            return self.fillColor
      def getProperties(self):
            return self.properties
      def getStroke(self):
            return self.stroke
      def setStrokeWidth(self, strokeWidth):
            self.strokeWidth = strokeWidth

      def getStrokeWidth(self):
            if self.stroke != None:
                  return strokeLineWidth
            else:
                  return False
      def getRGB(self):
            return 
      def enableSubPixelResolution(self):
            self.bounds = [self.x,self.y,self.width,self.height]
            self.subPixel = True
      def subPixelresolution(self):
            return self.subPixelRect
      def setPosition(self,n):
            if n<0: n=0
            self.position = n
            self.channel = self.slice = self.frame = 0
            self.hyperstackPosition = False;
      def setPositionH(self, channel, sliceZ, frame):
            if channel <0: channel=0
            self.channel = channel
            if sliceZ <0: sliceZ=0
            self.slice = sliceZ
            if frame <0: frame=0
            self.frame = frame
            self.position = 0
            self.hyperstackPosition = True
      def getPosition(self):
            return self.position
      def getCPosition(self):
            return self.channel
      def getZPosition(self):
            if self.slice ==0 and self.hyperstackPosition ==False:
                  print('self.position',self.position)
                  return self.position
            else:
                  print('self.slice',self.slice)
                  return self.slice
      def getTPosition(self):
            return self.frame
      def setCornerDiameter(self, cornerDiameter):
            if (cornerDiameter<0): cornerDiameter = 0;
            self.cornerDiameter = cornerDiameter;
      def getCornerDiameter(self):
            return self.cornerDiameter

      def hasHyperStackPosition(self):
            return self.hyperstackPosition

      def getPrototypeOverlay(self):
            if self.protoOverlay != None:
                  return self.prototypeOverlay
            else:
                  #TODO: add new overlay
                  print("Overlays not yet implemented")
                  return False

      def getMask(self):
            mask = np.ones((self.height*self.width))*-1.
            return mask.reshape(self.height,self.width)

      def getFloatPolygon(self):
            if self.cornerDiameter >0:
                  pass
                  #ImageProcessor ip = getMask();
                  #Roi roi2 = (new ThresholdToSelection()).convert(ip);
                  #if (roi2!=null) {
                  #      roi2.setLocation(x, y);
                  #      return roi2.getFloatPolygon();
                  #}
            if self.subPixelRect:
                  xpoints = [None]*4
                  ypoints = [None]*4
                  xpoints[0] = self.x
                  ypoints[0] = self.y
                  xpoints[1] = self.x + self.width
                  ypoints[1] = self.y
                  xpoints[2] = self.x + self.width
                  ypoints[2] = self.y + self.height
                  xpoints[3] = self.x
                  ypoints[3] = self.y + self.height
                  return {'xpoints':xpoints,'ypoints':ypoints,'npoints':4}
            else:
                  pass
                  p = getPolygon()
                  return
      


