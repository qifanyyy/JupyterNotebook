#In this file will reside all of the feature
#selection algorithms

import numpy as np
import matplotlib.pylab as plt

def entropyVector(x):
    '''
    Computes the entropy of a vector of discrete values
    '''
    vals=np.bincount(x)
    #excluding the empty bins at the end and start of x
    vals=vals[1:-2]
    den=np.sum(vals)
    probs=vals/np.float(den)
    entro=-np.sum([i*np.log2(i) for i in probs if i!=0])/np.float(np.log2(np.size(vals,0)))
#     plt.plot(x)
#     plt.show()
    return entro
def mutualInformation(jointProb):
    '''
    Calculates the mutual information from the output of
    the jointProbs function
    '''
    
    

def jointProbs(x,y):
    '''
    Calculates the probabilities of joint probabilities for the different values of x and y
    The values most be discrete,positive, starting from 0 or 1
    '''
    probs={}
    
    valsX,temp=np.unique(x,return_inverse=True)
    valsX=[int(i) for i in valsX]
    temp=np.bincount(temp) 
    pX=temp/float(sum(temp))
    
    valsY,temp=np.unique(y,return_inverse=True)
    valsY=[int(i) for i in valsY]
    temp=np.bincount(temp) 
    pY=temp/float(sum(temp))
    
    maxX=max(valsX)
    maxY=max(valsY)
    
    minX=min(valsX)
    minY=min(valsY)
    
    C={}
    
    #Another option would be to use sparse matrices however that will 
    #only work for 2 dimensional matrices 

    #This is a very efficient version of the algorithm
    for i in range(len(x)):
        key=str(x[i])+','+str(int(y[i]))
        if key in C.keys():
            C[key]+=1
        else:
            C[key]=1
        
    
    den=0
    for xi in valsX:
        for yi in valsY:
            key=str(xi)+','+str(yi)
            if key in C.keys():
                probs[key]=C[key]
                den+=C[key]
            else:
                probs[key]=0
    
    for (key,val) in probs.iteritems():
        probs[key]=probs[key]/float(den)
       
    
    totalSum=0
    for key,val in probs.iteritems():
        xVal,yVal=[int(i) for i in key.split(',')]
        
        indX=valsX.index(xVal)
        indY=valsY.index(yVal)
        if probs[key]==0:
            totalSum+=0
        else:
            totalSum+=probs[key]*np.log(probs[key]/(pX[indX]*pY[indY]))
        
        
     
    
#     return {'counts':C,'probabilities':probs}
    return totalSum
    


def informationGain(x,y):
    '''
    This implementation of information gain
    simply binerizes the data and then
    calculates information gain following the
    elements of information theory book equation in page
    x : features to be analyzed, where rows are data points and columns correspond to features 
    y : class labels 
    here Information gain is:
    I(y;x)=H(y)-H(y|x)   
    I(y;x)=\sum_{x,y} p(x,y)\frac {log(p(x,y))}{(p(x).p(y))} 
    '''
    
    x=np.array(x)
    y=np.array(y)
    
    xMax=np.max(x,0)
    xMin=np.min(x,0)
    bins=[]
    
    #Discretized data
    xD=[]
    try:
        for i in range(len(xMin)):
            #-1e-5 and+1e-5 added so that the extremes are included in the 
            #bins, this however generates two empty bins that's why the last
            #[1:-2]
            tempXD,tempBins=np.histogram(x[:,i],10)
            xD.append(np.digitize(x,tempBins))
            bins.append(tempBins)
            C=jointProbs(xD[-1],y)
            print(C)
    except:
#         bins.append(np.linspace(xMin-1e-5,xMax+1e-5, num=10))
        binsNum=len(np.unique(x))
        if binsNum<10:
            temp,tempBins=np.histogram(x,binsNum)
            xD.append(np.digitize(x,tempBins))
        else:
            temp,tempBins=np.histogram(x,10)
            xD.append(np.digitize(x,tempBins))
        C=jointProbs(xD[-1],y)
    return C

    


if __name__=='__main__':
#     x=np.random.rand(5,2)
#     y=np.round(np.random.rand(5,1))
    x=[1,1,0,1]
    y=[0,0,1,1]
    print(x)
    print(y)
    print(informationGain(x,y)) 
    
    
    