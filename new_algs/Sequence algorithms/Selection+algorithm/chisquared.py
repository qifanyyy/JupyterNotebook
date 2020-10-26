
"""
    Chi Squared metric
"""
from metric import Metric
from math import log



class ChiSquared(Metric):
    

    # returns [(attr, metric), (attr, metric), (attr, metric)]    
    def select(self):
	
        for att in self._freq.keys():
            for target in [0,1]:
                self._conj[att][target][0] = self._target[target] - self._conj[att][target][1]
            
        metrics = []
        for att in self._freq.keys():
            metric = 0.0
            for target in [0, 1]:
                for attVal in [0, 1]:
                  
                    NEtEc = float(self._conj[att][target][attVal])/self._N
                    # N x P(t) * P(c)
                    Pt = self._conj[att][0][attVal] + self._conj[att][1][attVal]
                    if Pt == 0:
                        continue
                    EEtEc = float(Pt * self._target[target])/self._N
                    #print 'NEtEc: ' + str(NEtEc) + ' EEtEc: ' + str(EEtEc) + ' '+ str(target) + ' ' + str(attVal)
                    metric += float((NEtEc - EEtEc) * (NEtEc - EEtEc))/EEtEc
            metrics.append((att, metric))
            
        return metrics
		