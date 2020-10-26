import random

# represents an attribute
class Attribute(object):

    def __init__(self, name):
        self._values = []
        self._name = name

    def add(self, *args):
        map(self._addSingle, args)
        
    def _addSingle(self, value):
        #possible attribute values
        self._values.append(value)

    def getValues(self):
        return self._values

    def valueCount(self):
        return len(self._values)

    def __str__(self):
        return self._name

#generates attributes with random number of values, used for testing
class RandomAttributeFactory(object):

    def __init__(self, start):
        #The first attribute's id will be labeled 'start',
        #the second at start + 1, etc.
        self._next = start

    def getNext(self):
        #assign a random attribute name
        randomAtt = RandomAttribute('rand' + str(self._next))
        self._next = self._next + 1

        #assign a random number of values from 2 to 14
        str_list = map(str, range(1, random.randint(2, 5)))
        map(randomAtt.add, str_list)

        return randomAtt


class RandomAttribute(Attribute):

    def sample(self):
        return self._values[random.randint(0, self.valueCount() - 1)]
    
    def setValues(self, values):
        self._values = values

class SampleSet(object):

    def __init__(self):
        self.values = []
        self.parameters = []

    def addDefinition(self, attribute):
        self.parameters.append(attribute)
	
    def addSample(self, line):
        sample = [line.split()[0]]
        
        for token in line.split()[1:self.size()]:
            sample.append(token.split(':')[1])

        if len(sample) < len(self.parameters):
            return		
			
        self.values.append(sample)
		
    def size(self):
        return len(self.parameters)
		
    def startIdx(self):
        self._idx = 0

    def getNext(self, attr):
        self._idx += 1
        return self._values[self._idx][attr]
	    
