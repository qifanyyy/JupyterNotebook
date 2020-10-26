import thread

class Metric(object):

    def combine(self, other):
        # this should be isolated in dataSet
        for key in set(self._freq.keys() + other._freq.keys()):
            if key not in self._freq:
                self._freq[key] = [0.0,0.0]

            for value in [0, 1]:
                self._freq[key][value] += other._freq.get(key, [0, 0])[value]		

            if key not in self._conj:
                self._conj[key] = [[0.0, 0.0], [0.0, 0.0]]
           
            for value in [0, 1]:
                for target in [0, 1]:
                    #[att_name][target_value][att_value]
                    self._conj[key][target][value] += other._conj.get(key, [[0.0, 0.0], [0.0, 0.0]])[target][value]
        
        self._N += other._N
        for target in [0, 1]:
            self._target[target] += other._target[target]
        return self
        
    def _readFile(self, fname, event, id, threadNum):
        with open(fname, 'r') as f:
            cnt = 0
            while True:
                line = f.readline()
                if not line: break
                if len(line) < 2: continue	
                if cnt % threadNum == id:
                    self.process(line)
                cnt += 1
        print 'Thread ' + str(id) + ' finished \n'
        event.set()
    
    def __init__(self):  # pylint: disable=E1002

        #dictionary like representation of lines
        self._freq = {}
        self._conj = {}
        self._target = [0.0, 0.0]
        self._N = 0.0
        
    def process(self, lineStr):
        
        #one more sample
        self._N += 1
        #count target class
        splitted = lineStr.split()
        target = int(splitted[0])
        self._target[target] += 1 
        
		
        # this should be isolated in dataSet
        for attVal in splitted[1:len(splitted)]:
            value = int(attVal.split(':')[1])
            name = attVal.split(':')[0]

            if name not in self._freq:
                self._freq[name] = [0.0, 0.0]
            self._freq[name][value] += 1		

            if name not in self._conj:
                self._conj[name] = [[0.0, 0.0], [0.0, 0.0]]
            #[att_name][target_value][att_value]
            self._conj[name][target][value] += 1

