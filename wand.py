


class Wand(object):
	"""docstring for Wand"""
	def __init__(self, arg):
		super(Wand, self).__init__()
		self.arg = arg
		OUR_CONNECTED = 4
		EIGHT_CONNECTED =8
		LEGACY_MODE =1

		#maxPoints = 1000;
		self.xpoints = []
		self.ypoints = []

		THRESHOLDED_MODE = 256


	def autoOutline(startX,startY,tolerance,mode):
		if startX <0 or startX>=width or startY<0 or startY>=height:
			return

		exactPixelValue = tolerance==0
		thresholdMode = (mode & THRESHOLDED_MODE) !=0
		legacyMode = (mode & LEGACY_MODE) != 0 && tolerance == 0
		if(!thresholdMode):
			startValue = getPixel(startX,startY)
			lowerThreshold = startValue - tolerance
			upperThreshold = startValue + tolerance
		x = startX
		y = startY
		seedX
		if inside(x,y):
			seedX = x
			while(inside(x,y)==True):
				x+=1
		else:
			while(inside == False):
				x+1
				if (x>=width): return
			seedX = x
		fourConnected
		if legacyMode:
			fourConnected = !thresholdMode && !(isLine(x,y)):
		else:
			fourConnected = (mode & FOUR_CONNECTED) !=0
		first = True
		while(True):
			insideSelected = traceEdge(x,y, fourConnected)
			if legacyMode:return


	def inside(self.x,y):
		if x<0 or x>=self.width or y<0 or y>=self.height:
			return False
		value = getPixel(x,y)
		return value>=lowerThreshold && value<=upperThreshold
	def inside_dir(self.x,y,direction):

		case = direction & 3 #Will return number between 0 and 3.
		if case == 0: return self.inside(x,y)
		elif case == 1:return self.inside(x,y-1)
		elif case == 2:return self.inside(x-1,y-1)
		elif case == 3:return self.inside(x-1,y)


	def traceEdge(self,startX,startY, fourConnected):
		npoints = 0
		xmin = self.width
		if(inside(startX,startY)):
			startDirection = 1
		else:
			startDirection = 3
			startY += 1
		x = startX
		y = startY
		direction = startDirection
		while(x!=startX or y!=startY or (direction&3!=startDirection)):
			if fourConnected == True: # 4-connected.
				while newDirection < direction+2:
					if (!self.inside(x,y,newDirection)):
						break
					newDirection += 1
				newDirection -= 1
			else: # 8-connected.
				newDirection = direction +1
				while (newDirection >= direction):
					if inside(x, y, newDirection):break;
						newDirection -= 1

			if allPoints or (newDirection!=direction):
				self.addPoint(x,y)
			case = newDirection&3
			if case == 0: x += 1; break
			elif case == 1: y -= 1; break
			elif case == 2: x -= 1; break
			elif case == 3: y += 1; break

			direction = newDirection

		if self.xpoints[0]!=x && !allPoints:
			addPoint(x,y)
		return (direction <=0):
	def addPoint(self, x,y):
		self.xpoints.append(x)
		self.ypoints.append(y)
		if self.xmin>x:xmin = x





