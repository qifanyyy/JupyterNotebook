import random
import math
import matplotlib.pyplot as mpl

def absList(lvar,digits=2):
	lresult = []
	for i in range(0,len(lvar)):
		lresult.append(abs(lvar[i]))
	return lresult
def roundList(lvar,digits=2):
	lresult = []
	for i in range(0,len(lvar)):
		lresult.append(round(lvar[i],digits))
	return lresult
def lsum(lvar, value):
	lresult = []
	for v in range(0,len(lvar)):
		result.append(lvar[v]*value) 
	return lresult
def lmult(lvar, value):
	lresult = []
	for v in range(0,len(lvar)):
		lresult.append(lvar[v]*value)
	return lresult
def ldiv(lvar, value):
	lresult = []
	for v in range(0,len(lvar)):
		lresult.append(lvar[v]/value)
	return lresult 
def lrdiv(lvar, value):
	lresult = []
	for v in range(0,len(lvar)):
		lresult.append(value/lvar[v])
	return lresult
def lpot(lvar, p):
	lresult = []
	for v in lvar:
		lresult.append(math.pow(v,p))
	return lresult
def lsuml(lvar1, lvar2):
	lresult = []
	for i in range(0,len(lvar1)):
		lresult.append(lvar1[i]+lvar2[i])
	return lresult
def lresl(lvar1, lvar2, absFlag=0):
	lresult = []
	for i in range(0,len(lvar1)):
		if(absFlag):
			lresult.append(abs(lvar1[i]-lvar2[i]))
		else:
			lresult.append(lvar1[i]-lvar2[i])
	return lresult
def lmultl(lvar1, lvar2):
	lresult = []
	for i in range(0,len(lvar1)):
		lresult.append(lvar1[i]*lvar2[i])
	return lresult
def ldivl(lvar1, lvar2):
	lresult = []
	for i in range(0,len(lvar1)):
		lresult.append(lvar1[i]/lvar2[i])
	return lresult
def lcos(lr,frecuency,absFlag=0):
	time = range(0,lr)
	frecuencyinHZ = lmult(time,(frecuency*math.pi/180))
	lresult = []
	for f in frecuencyinHZ:
		if(absFlag):
			lresult.append(round(abs(math.cos(f)),2))
		else:
			lresult.append(round((math.cos(f)),2))
	return lresult
def lsin(lr,frecuency,absFlag=0):
	time = range(0,lr)
	frecuencyinHZ = lmult(time,(frecuency*math.pi/180))
	lresult = []
	for f in frecuencyinHZ:
		if(absFlag):
			lresult.append(round(abs(math.sin(f)),2))
		else:
			lresult.append(round((math.sin(f)),2))
	return lresult
def randomUR(lr,minV,maxV,roundFlag=0):
	lresult = []
	for i in range(0,lr):
		if(roundFlag):
			lresult.append(int(round((random.uniform(minV,maxV)))))
		else:
			lresult.append(random.uniform(minV,maxV))
	return lresult
def randomGR(lr,minV,maxV,roundFlag=0):
	lresult = []
	maxT = (abs(minV)+abs(maxV))
	for i in range(0,lr):
		if(roundFlag):
			lresult.append(int(round((random.random()*maxT)-abs(minV))))
		else:
			lresult.append((random.random()*maxT)-abs(minV))
	return lresult
def graphFeatures(features,allinOneFlag=1):
	for f in features:
		mpl.plot(f)
		if(not(allinOneFlag)):
			mpl.show()
	if(allinOneFlag):
		mpl.show()
def listToString(vlist):
	stringl = ""
	for v in vlist:
		stringl = stringl+str(v)+","
	return stringl[:-1]
def writeCSV(filepath, features, target, labels):
    myfile = open(filepath,'w')
    #for v in target:
    labels.reverse()
    myfile.write(labels.pop()+",")
    myfile.write(listToString(target)+"\n")
    for row in features:
    	myfile.write(labels.pop()+",")
    	myfile.write(listToString(row)+"\n")	
    myfile.close()
    #print(stringResult)
def feature1(numberOfRecords,verbose=0):#time cos mod logic
	time = range(0,numberOfRecords)
	noise1 = randomUR(numberOfRecords,-1,1,0)
	features = []
	target = []
	passcos = []
	passmod = []
	coslimit = 0.2
	features.append(time) #0 time
	features.append(lcos(numberOfRecords,7,1))#1 time*cos(7*pi/180)	
	features.append(randomUR(numberOfRecords,10,40,1)) #2  /10%2===1
	features.append(randomUR(numberOfRecords,0.4,1.2,1)) #3
	features.append(randomUR(numberOfRecords,0.4,1.2,1)) #4
	features.append(randomUR(numberOfRecords,0,0.6,1)) #5
	features.append(randomUR(numberOfRecords,int(round(numberOfRecords/4)),numberOfRecords+int(round(numberOfRecords/4)),1)) #6
	features.append(randomUR(numberOfRecords,0,numberOfRecords*2,1)) #7 noise
	features.append(randomUR(numberOfRecords,0,numberOfRecords/2,1)) #8 noise
	features.append(randomGR(numberOfRecords,0,numberOfRecords,10)) #9 noise
	features.append(randomGR(numberOfRecords,0,numberOfRecords,10)) #10noise
	features.append(lmult(time,10)) #11 noise correlated with var0
	features.append(roundList(lsuml(features[0],noise1)))#12 var0 + noise
	#feature extraction
	features.append(lsuml(lsuml(features[3],lmult(features[4],2)),lmult(features[5],4)))#13 x*1 y*2 z*4 (logic)
	for x in features[1]:
		if(x>coslimit):
			passcos.append(1)
		else:
			passcos.append(0)
	for x in features[2]:
		if((x/10)%2):
			passmod.append(1)
		else:
			passmod.append(0)
	features.append( lmultl(lmultl(lresl(features[6],features[0]),passcos),passmod) )#14 if(cos>coslimit) and if(var2/10%2) * (var6-var0)
	for i in range(0,numberOfRecords):
		if(features[6][i]>features[0][i] and features[1][i]>coslimit and ((features[2][i]/10))%2 and features[3][i] and features[4][i] and not(features[5][i]) ):
			target.append(1)
		else:
			target.append(0)
	if(verbose):
		print sum(target)
	return [features,target]
def feature2(numberOfRecords,verbose=0):#timcos -timesin >5
	time = range(0,numberOfRecords)
	cos = lcos(numberOfRecords,17,0)
	sin = lsin(numberOfRecords,17,0)
	noiseU = randomUR(numberOfRecords,-2,2,0)
	noiseG = randomGR(numberOfRecords,-4,4,0)
	noiseU = roundList(noiseU,2)
	noiseG = roundList(noiseG,2)
	features = []
	target = []
	features.append(lsuml(time,lmult(cos,5))) #0 time+cos
	features.append(lsuml(time,lmult(sin,5))) #1 time+sin
	features.append(randomUR(numberOfRecords,0,numberOfRecords*2,1)) #2 noise
	features.append(randomUR(numberOfRecords,0,numberOfRecords/2,1)) #3 noise
	features.append(randomUR(numberOfRecords,0,numberOfRecords,1)) #4 noise
	features.append(randomUR(numberOfRecords,0,numberOfRecords*3,1)) #5 noise
	features.append(randomUR(numberOfRecords,0,numberOfRecords/3,1)) #6 noise
	features.append(randomUR(numberOfRecords,0,numberOfRecords,1)) #7 noise
	f0rf1 = roundList(lresl(features[0],features[1],1))
	#feature extraction
	features.append(lsuml(f0rf1,noiseU ))#8 (var8+noiseU)
	features.append(lsuml(f0rf1,noiseG ))#9 (var8+noiseU)
	#features.append(f0rf1)#10 abs(var0 - var1) 
	for i in range(0,numberOfRecords):
		if(abs(features[0][i] - features[1][i]) > 5  ):
			target.append(1)
		else:
			target.append(0)
	if(verbose):
		print sum(target)
	return [features,target]
def feature3(numberOfRecords,verbose=0):#inside circle and A>B
	features = []
	target = []
	f0mf1 = [] #f0>f1
	noiselow = randomUR(numberOfRecords,-0.67,0.67,1)
	features.append(randomUR(numberOfRecords,-numberOfRecords*2,numberOfRecords*2,1)) #0 var0 
	features.append(randomUR(numberOfRecords,-numberOfRecords,numberOfRecords,1)) #1 var1
	features.append(noiselow) #2 noise1
	features.append(lmult(noiselow,10)) #3 noise1*10
	features.append(randomUR(numberOfRecords,0,numberOfRecords*2,1)) #4 noise2
	features.append(randomGR(numberOfRecords,0,numberOfRecords/2,1)) #5 noise3
	#feature extraction
	for x in range(0,numberOfRecords):
		if(abs(features[0][x]) >= features[1][x]):
			f0mf1.append(1)
		else:
			f0mf1.append(0)
	features.append(lsuml(f0mf1,noiselow)) #6 if var0 > var1 = 1 + noiselow
	f0f1pow = lpot(lsuml(lpot(features[0],2), lpot(features[1],2)),0.5)
	features.append(f0f1pow) #7 (f0^1+f1^2)^0.5

	for i in range(0,numberOfRecords):
		if( (abs(features[0][i]) >= features[1][i] ) and f0f1pow[i]>1118 ):
			target.append(1)
		else:
			target.append(0)
	if(verbose):
		print sum(target)
	return [features,target]
def feature4(numberOfRecords,verbose=0):#targetNoiseCorrelation
	features = []
	target = randomUR(numberOfRecords,0,1,1) #3 noise
	roundList
	smallnoise = 0.5
	mediumnoise = 1
	bignoise = 2
	features.append(roundList(lsuml(target,randomUR(numberOfRecords,-smallnoise,smallnoise,0)),2)) #0 sUR
	features.append(roundList(lsuml(target,randomUR(numberOfRecords,-mediumnoise,mediumnoise,0)),2)) #1 mUR
	features.append(roundList(lsuml(target,randomUR(numberOfRecords,-bignoise,bignoise,0)),2)) #2 bGR
	features.append(roundList(lsuml(target,randomUR(numberOfRecords,-mediumnoise,mediumnoise,0)),2)) #3 mGR
	features.append(randomUR(numberOfRecords,0,numberOfRecords*2,1)) #4 Unoise
	features.append(randomGR(numberOfRecords,0,numberOfRecords/2,1)) #5 Gnoise
	if(verbose):
		print sum(target)
	return [features,target]
#'''
f1,t1 = feature1(1000,1)
l1 = ['target','time','cos','0to40','x','y','z','val','noise1','noise2','noise3','noise4','timex10','time+noise','logic','restrictions']
writeCSV("f1.csv",f1,t1,l1)
f2,t2 = feature2(1000,1)
l2 = ['target','v1','v2','n1','n2','n3','n4','n5','n6','v1-v2+noiseU','v1-v2+noiseG','v1-v2']
writeCSV("f2.csv",f2,t2,l2)
f3,t3 = feature3(1000,1)
l3 = ['target','var0','var1','noise1','noise1*10','noise2','noise3','var0>var1+noise1','insidecircle']
writeCSV("f3.csv",f3,t3,l3)
f4,t4 = feature4(1000,1)
l4 = ['target','target+sNoiseU','target+mNoiseU','target+bNoiseG','target+mNoiseG','noiseU1','noiseG1',]
writeCSV("f4.csv",f4,t4,l4)
#'''

#graphFeatures(f3[0:4],0)
#graphFeatures(f3,0)
#counterVar = 0
#print t1
#print sum(t1)
#for f in f1:
#	print counterVar,f
#	counterVar = counterVar+1
