
import matplotlib.pyplot as plt
#OG KG
import string
import math
import random

class Point:
   def __init__(self, x, y):
   self.x, self.y = x, y

   def add(self, other):
   return Point(self.x + other.x, self.y + other.y)

	def println(self):
	print "({0}, {1})".format(self.x, self.y)

	def dist(self, other):
	return round(math.sqrt((self.x-other.x)*(self.x-other.x)+(self.y-other.y)*(self.y-other.y)),4)

class Edge:
	def __init__(self, p1, p2):
	self.p1, self.p2,self.dist = p1, p2, p1.dist(p2)

	def println(self):
	print "<edge = {4},<({0}, {1}); ({2}, {3})> >".format(self.p1.x, self.p1.y, self.p2.x, self.p2.y,self.dist)

def readPoints(fileName):
	f = open(fileName, 'r')
	text=f.readlines();   
	f.close()
	listPoints=[]

	for line in text:
	words = line.split()
	p=Point(float(words[0]), float(words[1]))
	#p.println()
	listPoints.append(p)
	return listPoints
def randomPoints(n):
	listPoints,low,high=[] , 0, 1000
	for i in range(n):
	listPoints.append(Point(random.randrange(low,high), random.randrange(low,high)))
	return listPoints
def makeAllEdges(listPoints):
	listEdges = []
	for i in xrange(0, len(listPoints),1):
	for j in xrange(i, len(listPoints),1):
    	if( i!=j):e = Edge(listPoints[i], listPoints[j])
		else: e = Edge(listPoints[i], listPoints[j])
		listEdges.append(e)
	return listEdges

def printList(listMyClasses):
	for item in listMyClasses:
	item.println()


def makeMatrix(listPoints):
	arr=[]
	for i in xrange(0, len(listPoints),1):
	listRow = []
	for j in xrange(0, len(listPoints),1):
		if( i!=j):e = listPoints[i].dist(listPoints[j])
		else: e = Point(0,0).dist(Point(0,100000))
		listRow.append(e)
	arr.append(listRow)
	return arr

def Prima(numberOfVertex, listPoints):
	min_e,sel_e,used=[],[],[]
	seq_v, seq_e = [],[] # return
	INF= 999999
	matrix = makeMatrix(listPoints)
	lenM = len(matrix)
	if(lenM==1):
	seq_e.append(Edge(listPoints[0],listPoints[0]))
	return seq_e
	for i in xrange(0, lenM, 1):
	min_e.append(INF)
	sel_e.append(-1)
	used.append(False)

	min_e[numberOfVertex] = 0    
	for i in xrange(0,lenM, 1):
		v=-1
		for j in xrange(0, lenM, 1):
			if(not(used[j]) and (v==-1 or min_e[j]<min_e[v])): v=j
		if(min_e[v]==INF):
		print("NO EMST")
		return;        
	used[v]=True
	seq_v.append(v)
	if(sel_e[v]!=-1):
		#print "sel_e[{0}]={1}".format(v,sel_e[v])
		e = Edge(listPoints[v], listPoints[sel_e[v]])
		seq_e.append(e)
	for to in xrange(0,lenM,1):
		if( matrix[v][to]< min_e[to]):
			min_e[to] = matrix[v][to]
			sel_e[to]=v
	return seq_e;
21.	# ------------read points----------------------
22.	"""a = readPoints("points.txt");
22.1.	#printList(a)
23.	listp = randomPoints(50)
24.	#printList(listp)
24.1.1.	#answer = Prima(0, a)# a - list of points"""
25.	# ------------rand points----------------------
26.	"""
27.	listp = randomPoints(10)
28.	answer = Prima(0, listp) # will get list edge <weight,(p1,p2),(p21,p22)>
29.	print" answer"
30.	printList(answer)
31.	"""         

def makeStrPlotAnswer(listPoints):
	answer = Prima(0,listPoints)
	#list1=[]
	#list2=[]
	listLines=[]
	for i in xrange( 0 , len(answer), 1):
		linex=[]
		liney=[]
		linex.append(answer[i].p1.x)
		linex.append(answer[i].p2.x)
		liney.append(answer[i].p1.y)
		liney.append(answer[i].p2.y)
		listLines.append(linex)
		listLines.append(liney)
	return listLines

def makeStrPlot(listPoints):
	listLines=[]
	for i in xrange( 0 , len(listPoints), 1):
		listLines.append(listPoints[i].x)
		listLines.append(listPoints[i].y)
	#print listLines
	return listLines

#-------------------form windows----------------
from numpy import arange
import matplotlib
#matplotlib.use('WXAgg') #with warning

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import wx

#Frame->panel->buttons, texts, labels
class CanvasPanel(wx.Panel):
	def __init__(self, parent,id):
	wx.Panel.__init__(self, parent,id)

	self.mouseList=[] #TRUE - clear
	# if clean=T then there is no MST on canvas ( but points can exist)
	self.clean = True
	# newList was created from mouse
	self.mouse=False

	self.figure = Figure() # necessary
	self.axes = self.figure.add_subplot(111)# necessary
	self.canvas = FigureCanvas(self, -1, self.figure)#nec
	self.sizer = wx.BoxSizer(wx.VERTICAL)
	self.sizer.Add(self.canvas, 1, wx.LEFT| wx.GROW, 90) # 90 - gap from left

	self.n=50
	self.newList = randomPoints(self.n)

	self.label = wx.StaticText(self,-1,label=u'Enter N :',pos=(10,0),size=(80,25))

	self.txt = wx.TextCtrl(self,-1,'',pos=(0,30), size=(90,25))
	self.Bind(wx.EVT_TEXT, self.EvtText)

	self.buttonExit = wx.Button(self, -1, "Exit",(0,60))

	# self - parrent, .,title, (0,0) - position on frame
	self.buttonDraw = wx.Button(self, -1, "Draw",(0,90))
	# analize event
	self.Bind(wx.EVT_BUTTON, self.OnButtonClickDraw, self.buttonDraw)

	self.buttonRand = wx.Button(self, -1, "Randomize",(0,120))
	self.Bind(wx.EVT_BUTTON, self.OnButtonClickRandomize, self.buttonRand)

	self.buttonClean = wx.Button(self, -1, "Clean",(0,150))
	self.Bind(wx.EVT_BUTTON, self.OnButtonClickClean, self.buttonClean)

	"""self.buttonSubmit = wx.Button(self, -1, "Submit\n mouseList",(0,180), (88,40))
	self.Bind(wx.EVT_BUTTON, self.OnButtonClickSubmit, self.buttonSubmit)"""
	self.figure.canvas.Bind(wx.EVT_LEFT_DCLICK,self.OnLeftClick)
	#self.canvas...


	self.SetSizer(self.sizer)# stretch graph
	self.Fit()


	def OnLeftClick(self,event):
	print" mouse"

	if(self.clean):            
		pos = event.GetPosition()
		self.mouseList.append(Point(pos.x -75 ,505-pos.y)) #y vice versa       

		self.axes.axis([0,460,0,450]) # 535-75 = 460 X # 505-55=450 Y                                            
		self.axes.plot(pos.x -75 ,505-pos.y,'go')
		self.canvas.draw()


	else: self.mouseList=[]
	if(len(self.mouseList)>0):
		self.newList= self.mouseList
		self.mouse=True



	def EvtText(self, event):
		self.n = int(event.GetString())
		print self.n
		if(self.n>100000): print"very big N, N:=10 000"
		if(self.n>3800): self.n=3800



	def OnButtonClickDraw(self,event):
		print("draw button begin")
		self.clean=False
		self.figure.set_canvas(self.canvas)
		self.axes.clear()
		if(self.mouse): self.axes.axis([0,460,0,450])


	   #prepare answer for drawing
	   listLines = makeStrPlotAnswer(self.newList)
	   for i in xrange(0,len(listLines),2):
		    self.axes.plot(listLines[i], listLines[i+1],  'ro-')
		self.canvas.draw()
		self.mouseList=[]
		print("draw button end")


	def OnButtonClickRandomize(self, event):
		print" rand button"
		self.mouse=False
		self.newList = randomPoints(self.n)

	def OnButtonClickClean(self,event):
		print("clean button")
		self.figure.set_canvas(self.canvas)
		self.axes.clear()
		self.mouseList=[]
		self.canvas.draw()
		self.clean=True


class myFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size=(700, 600))
		self.panel = CanvasPanel(self, -1)

		self.Bind(wx.EVT_BUTTON, self.OnButtonClickExit, self.panel.buttonExit)


		self.Centre()
		self.Show(True)

	def OnButtonClickExit(self, event):
		print" forth button exit"
		#self.Destroy() # may be used to canvas
		self.Close()


if __name__ == "__main__":

	app=wx.App()
	myFrame(None, -1, title = 'EMST')
	app.MainLoop()
	print "OK" 
