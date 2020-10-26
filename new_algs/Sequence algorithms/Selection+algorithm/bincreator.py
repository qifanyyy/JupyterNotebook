import numpy as np

def getDynamicBins(data):
	xbinsetList = []
	#print data
	for i in range(0,data.shape[1]):
		xbinset = []
		f = np.array(data.ix[:,i])
		samples = len(f)
		domainSize = float(len(set(f)))
		std = np.std(f)
		#xbinset.append(round(domainSize/2))
		#xbinset.append(round(domainSize/4))
		#xbinset.append(round(domainSize/8))
		xbinset.append(round(pow(domainSize,0.5))) #Square Root
		xbinset.append(round(np.log2(domainSize))) #Strugles
		xbinset.append(round(2*pow(domainSize,0.3333))) #Rice
		xbinset.append(round((3.5*std)/pow(domainSize,0.3333))) #Scott normal
		#print xbinset
		for i in range(0,len(xbinset)):
			if(domainSize<=30):
				xbinset[i] = domainSize
			else:
				if(xbinset[i]>domainSize/5 and domainSize>50):
					xbinset[i] = domainSize/5
				if(xbinset[i]<=1):
					xbinset[i] = 2
		xbinset = map(int,xbinset)
		xbinset = set(xbinset)
		xbinset = list(xbinset)
		#print xbinset
		xbinsetList.append(xbinset)				
	return xbinsetList