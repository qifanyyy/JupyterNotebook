"""
Features Selector
"""

from chisquared import ChiSquared
from mutualinfo import MutualInfo
import thread
import threading

class FeatureSelector(object):

    _supported = {'chi_squared': ChiSquared,
                  'mutual_inf': MutualInfo}

    def __init__(self, technique, id, threadNum):  # pylint: disable=E1002

        self._id = id
        self._threadNum = threadNum
        #fail if wrong argument
        if technique not in self._supported.keys():
            raise ValueError("The technique must be one of" + str(self._supported.keys()))
        
        self._metric = self._supported[technique]()
        self._dataSet = set
    
	# run selection
    def select(self, k):
        featureSet = self._metric.select()
        
        featureSet.sort(key = lambda x : x[1])
        featureSet.reverse()
		
		#keep k best 
        return featureSet[0:k]
		
    def process(self, line):
        self._metric.process(line)
        
    def startProcessing(self, fname):
        #prepare the data set itself
        event = threading.Event()
        try:
            thread.start_new_thread( self._metric._readFile, (fname, event, self._id, self._threadNum, ) )
        except Exception, e:
            print "Error: unable to start thread" + str(e)
        
        return event
    def combine(self, other):
        self._metric.combine(other._metric)
        return self