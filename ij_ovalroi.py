import numpy as np
from ij_roi import Roi

class OvalRoi(Roi):
      """docstring for OvalRoi"""
      def __init__(self,x,y,width,height,xMax,yMax,cornerDiameter=0):
            super(OvalRoi, self).__init__(x,y,width,height,xMax,yMax,cornerDiameter=0)
            
            

      def getMask(self):
            a = self.width/2.0
            b = self.height/2.0
            a2 = a**2
            b2 = b**2
            a -= 0.5
            b -= 0.5
            mask = np.zeros((self.height*self.width))
            for y in range(0,self.height):
                  offset = y*self.width
                  for x in range(0,self.width):
                        xx = x-a
                        yy = y-b
                        if ((xx*xx/a2+yy*yy/b2) <=1.0):
                              mask[offset+x] = -1
            return mask.reshape(self.height,self.width)
      def getPolygon(self,absoluteCoordinates):
            mask = self.getMask()
            wand = Wand(mask)
            wand.autoOutline(self.width/2,self.height/2, 255,255)
            if absoluteCoordinates == True:
                  for i in range (0, wandpoints):
                        wand.xpoints[i] += x
                        wand.ypoints[i] += y
            return Polygon(wand.xpoints, wand.ypoints,wand.npoints)
