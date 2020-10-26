#construction of ReliefF function

"""
Given a dataset, number of random instances to pick form the dataset and
number of features to consider in each iteration (k), the function returns the weigths of the attributes
of the dataset.
These weigths can then be used as the final results out of the ReliefF algorithm

Paper-

Marko Robnik-ˇSikonja and Igor Kononenko. Theoretical and empirical analysis of relieff
and rrelieff. Machine learning, 53(1-2):23–69, 2003.

"""
def reliefF(df,n_neighbours=10,instances_to_select=10):
  import numpy as np
  
  feature=df.iloc[:,:-1]
  targetClass=df.iloc[:,-1]
  m,n=feature.shape

  weights=np.zeros(n,dtype='int')

  classes=np.unique(targetClass)

  m2=instances_to_select #number of features to pickup randomly from the 
  k=n_neighbours #number of neighbours to consider

  instances=np.array(list(range(1,m)))
  

  minimums=np.min(feature.values,axis=0)
  maximums=np.max(feature.values,axis=0)

  differ=np.subtract(maximums,minimums)


  for i in range(m2):
    chosen=np.random.choice(instances[:-1])
    instances=np.delete(instances,np.where(instances==chosen))

    rI=feature.iloc[chosen,:].values

    instanceClass=targetClass[chosen]
    probIClass=len(np.where(targetClass==instanceClass)[0])/m #getting the probaility of choosing this class

    hit=[]
    miss={}

    low,high,tem1,tem2=0,m,(chosen-1),(chosen+1)
    hitFlag=True
    missFlag=True
    
    
    while(hitFlag==True):

      if targetClass[tem1]==instanceClass:
        hit.append(tem1)
      if targetClass[tem2]==instanceClass:
        hit.append(tem2)
      if len(hit)==k:
        hitFlag=False
      if tem1>0:
        tem1-=1
      if tem2<m-1:
        tem2+=1
    for x in classes:
      if x==instanceClass:
        continue
      #print(instanceClass,x)
      cli=max(np.where(targetClass==x)[0]) #finding the last instance of the class x
      if cli>chosen:
        tem=min(np.where(targetClass==x)[0])
        miss[x]=list(range(tem,tem+k))
      else:
        tem=max(np.where(targetClass==x)[0])
        miss[x]=list(range(cli-k+1,cli))

    #print("Chosen-",chosen,"Hits-",hit,"Misses-",miss)

    totalHit=np.zeros(n,dtype='int')

    for hit in range(k):
      hI=feature.iloc[hit,:].values
      dRH=np.divide(np.abs(np.subtract(rI,hI)),differ)
      dRH=dRH/(m2*k)
      totalHit=np.add(totalHit,dRH)

    totalMiss=np.zeros(n,dtype='int')

    for eachClass in miss:

      tMiss=np.zeros(n,dtype='int')
      pclass=len(np.where(targetClass==eachClass)[0])/m #getting the probability of getting this class
      postProb=pclass/(1-probIClass) #calculating the posterior probanility of getting this class

      for eachMiss in miss[eachClass]:
        mI=feature.iloc[eachMiss,:].values
        dRM=np.divide(np.abs(np.subtract(rI,mI)),differ)
        dRM=dRM/(m2*k)
        tMiss=np.add(tMiss,dRM)

      totalMiss=np.add(totalMiss,(tMiss*postProb))

    weights=np.add(weights,totalMiss)
    weights=np.subtract(weights,totalHit) 
    
  return weights
