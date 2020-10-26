import numpy as np
from correlationMesures import *
import bincreator as bc
import cut as cut
#from pandas import *
#from matplotlib import gridspec
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
#import matplotlib.pyplot as plt
#import time
#import msvcrt as m
#import sys
#"best=good in this time" 

def plot_sample(x,y, numBinx, numBiny, step):
        fig = plt.figure(1)
        gs = gridspec.GridSpec(4,4)
        ax1 = fig.add_subplot(gs[:3, :3])
        ax1.scatter(x, y, color='blue')
        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax1.set_xlabel('X axis')
        ax1.set_ylabel('Y axis')
        ax2 = fig.add_subplot(gs[3,:3])
        ax2.hist(x, numBinx, facecolor='g')
        ax2.set_xticklabels([])
        ax2.yaxis.set_visible(False)
        ax2.set_xlabel('Histogram of X')
        ax3 = fig.add_subplot(gs[:3, 3])
        ax3.hist(y, numBiny, orientation='horizontal', facecolor='g')
        ax3.set_yticklabels([])
        ax3.xaxis.set_visible(False)
        ax3.set_ylabel('Histogram of Y')
        #"""
        ax4 = fig.add_subplot(gs[3, 3])
        H, xedges, yedges = np.histogram2d(y, x, bins=(numBinx, numBiny))
        X, Y = np.meshgrid(xedges, yedges)
        #ax4.pcolormesh(X, Y, H)
        ax4.set_aspect('equal')
        ax4.xaxis.set_visible(False)
        ax4.yaxis.set_visible(False)
        #"""
        gs.update(wspace=0.5, hspace=0.5)
        H, xedges, yedges = np.histogram2d(y, x, bins=(numBinx, numBiny))
        print str(H)
        plt.show()
        #fig.show()
         

def maxlist(a,b):
	result = []
	for i in range(0,len(a)):
		result.append(max(a[i],b[i]))
	return result

def getOrderRank(xlist):
	rank = [i[0] for i in sorted(enumerate(xlist), key=lambda x:x[1])]
	rank.reverse()
	print rank
	return rank

def printresult(PMDbest,PMD2best,labelcol):
	for i in range(0,len(PMDbest)):
		print i,labelcol,":",PMDbest[i],PMD2best[i]

def plotCorrelation():
	#if(i == 0 or i == 1):
		#plot_sample(x,y,numBinx, 2, 1)
		#plot_sample(x,y,numBinx, 2, 1)
		#print sum(x) 
		#plt.figure(1)
		#plt.subplot(211)
		#plt.title(str(sum(x)))
		#plt.hist(x,numBinx)
		#plt.subplot(212)
		#plt.title(str(sum(y)))			
		#plt.hist(y,numBinx)
		#plt.show()
	return True

def get_corrlab(numBinx,numBiny,data,cols):	
	PMD = []
	PMD2 = []
	y = np.array(data.ix[:,-1])
	for i in range(0,cols):
		x = np.array(data.ix[:,i])
		PMD.append(round(propuesta_mutual_dependency(x, y, numBinx, numBiny),3))
		PMD2.append(round(propuesta2_mutual_dependency(x, y, numBinx, numBiny),3))
	return PMD, PMD2

def get_bestcorlab(xbinset,ybinset,data):
	cols = data.shape[1]-1
	PMDbest = [0] * (cols)
	PMD2best = [0] * (cols)
	for numBinx in xbinset:
		for numBiny in ybinset:
			PMD, PMD2 = get_corrlab(numBinx, numBiny, data, cols)
			PMDbest = maxlist(PMDbest,PMD)
			PMD2best = maxlist(PMD2best,PMD2)
			#print numBinx,numBiny,":",PMD,PMD2
			#print numBinx,numBiny
			#getOrderRank(PMDbest)
			#getOrderRank(PMD2best)
	#print PMDbest,PMD2best
	#printresult(PMDbest,PMD2best,cols)
	getOrderRank(PMDbest)
	getOrderRank(PMD2best)
	print PMDbest
	print PMD2best
	return [PMDbest, PMD2best]

def get_corrlabDynamic(xbinset,ybinset,x,y):	
	PMD = []
	PMD2 = []
	for numBinx in xbinset:
		for numBiny in ybinset:
			#print numBinx
			#print numBiny
			PMD.append(round(propuesta_mutual_dependency(x, y, numBinx, numBiny),3))
			PMD2.append(round(propuesta2_mutual_dependency(x, y, numBinx, numBiny),3))
	#print PMD, PMD2
	return max(PMD), max(PMD2)

def get_bestcorlabDynamic(data):
	cols = data.shape[1]-1
	PMDbest = [0] * (cols)
	PMD2best = [0] * (cols)
	binList = bc.getDynamicBins(data)
	#print binList
	y = np.array(data.ix[:,-1])
	for i in range(0,cols):
		x = np.array(data.ix[:,i])
		xbinset = binList[i]
		ybinset = binList[cols]
		PMD, PMD2 = get_corrlabDynamic(xbinset, ybinset, x,y)
		PMDbest[i] = PMD
		PMD2best[i] = PMD2
		print i,xbinset,ybinset,PMD,PMD2
	#print PMDbest
	#print PMD2best
	features = getOrderRank(PMDbest)
	getOrderRank(PMD2best)
	#print PMDbest,PMD2best
	PMDbest.sort()
	PMDbest.reverse()
	print PMDbest
	nf = cut.greatestDiff(PMDbest)
	features = features[0:nf]
	print features
	newX = np.array(data.ix[:,features])
	return [newX, y]
#Parece ser que el correr 

#print "ejemplo.csv"
#fs.get_bestcorlab(xbinset, ybinset, 'Data\ejemplo.csv', 6, 5)
#print "data.csv"
#fs.get_bestcorlab(xbinset, ybinset, 'Data\data.csv', 4, 3)
#print "data-fs.csv"
#fs.get_bestcorlab(xbinset, ybinset, 'Data\data-fs.csv', 6, 5)
#print "data-fsfe.csv"
#fs.get_bestcorlab(xbinset, ybinset, 'Data\data-fsfe.csv', 7, 6)

#print "Data\data2400-r20" #buenos 0,1,2 #Observaciones: Excelente
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data2400-r20.csv', 24, 23)
#print "Data\data-f1" # 1,2,3,4,5,6 #Observaciones: Corte complicado por la distancia
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data-f1.csv', 14, 13)
#print "Data\data-f2" #0,1  #Observaciones: EXCELENTE (mas bins)
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data-f2.csv', 9, 8)
#print "Data\data-f2-fe" #0,1  #Observaciones: Excelente
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data-f2-fe.csv', 11, 10)
#print "Data\data-f3" #0,1 Observaciones: Corte complicado, debido a que una de las 2 caracteristicas esta muy bien evaluada y la otra esta muy cerca del ruido
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data-f3.csv', 7, 6)
#print "Data\data-f4" #0,1,2,3 #Observaciones: Excelente
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data-f4.csv', 7, 6)

#print "data-r50.csv"
#fs.get_bestcorlab(xbinset, ybinset, 'Data\data-r50.csv', 54, 53)
#print "colon-cancer.csv"

#fs.get_bestcorlab(xbinset, ybinset, 'Data\colon-cancer.csv', 2001, 2000)
#print "colon-cancer-fs.csv"
#fs.get_bestcorlab(xbinset, ybinset, 'Data\colon-cancer-fs.csv', 11, 10)
#print "colon-cancer-fs2.csv"
#fs.get_bestcorlab(xbinset, ybinset, 'Data\colon-cancer-fs2.csv', 11, 10)

#print "Data/train.csv" #0,1,2,3 #Observaciones: Excelente
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data/trainv2.csv', 59, 58)

#print "Data/flex-ct.csv" #0,1,2,3 #Observaciones: Excelente
#fs.get_bestcorlab(xbinset, ybinset, 'Data/flex-ct.csv', 28, 27)

#print "Data/flex-ct.csv" #0,1,2,3 #Observaciones: Excelente
#fs.get_bestcorlab(xbinset, ybinset, 'Data/finalDataStrict.csv', 32, 31)