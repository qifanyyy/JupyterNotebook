
class Heap(object):

    def __init__(self, polarity):

        self.polarity = polarity
        self.keys = []
        self.vals = []

    def getmin(self):
        if self.polarity=="min":
            return [self.keys[0], self.vals[0]]
        else:
            raise(NameError, "No getmin() method for heap with polarity 'max'.")

    def getmax(self):
        if self.polarity=="max":
            return [-1 * self.keys[0], self.vals]
        else:
            raise(NameError, "No getmax() method for heap with polarity 'min'.")

    def getsize(self):
        return len(self.keys)

    def insert(self, key, val):

        if self.polarity=="max":    # max heap uses negative values
            key *= -1
        # Add val at end of heap
        self.keys.append(key)
        self.vals.append(val)
        iNew = len(self.keys)-1
        iParent = int((iNew-1)/2)

        # bubble up
        while self.keys[iNew] < self.keys[iParent] and iNew>0:
            self.keys[iNew], self.keys[iParent] = self.keys[iParent], self.keys[iNew]
            self.vals[iNew], self.vals[iParent] = self.vals[iParent], self.vals[iNew]
            iNew = iParent
            iParent = int((iNew-1)/2)

    def extractmax(self):
        temp = self.extractmin()
        return [-1 * temp[0], temp[1]]

    def extractmin(self):

        # save current minimum to return value
        old_min_key = self.keys[0]
        old_min_val = self.vals[0]
        # swap last element into first position
        self.keys[0] = self.keys[-1]
        self.vals[0] = self.vals[-1]
        # save a copy as x; it'll be used a number of times
        x = self.keys[0]
        # delete last element
        del self.keys[-1]
        del self.vals[-1]

        # bubble down
        iKey = 0
        iChild1 = 1
        iChild2 = 2
        done = False


        while iChild2 < len(self.keys) and not done:

            if x > self.keys[iChild1] or x > self.keys[iChild2]:

                # Bubble down. Pick the child to swap with to be the smaller one
                if self.keys[iChild1] < self.keys[iChild2]:
                    self.keys[iChild1], self.keys[iKey] = self.keys[iKey], self.keys[iChild1]
                    self.vals[iChild1], self.vals[iKey] = self.vals[iKey], self.vals[iChild1]
                    iKey = iChild1
                else:
                    self.keys[iChild2], self.keys[iKey] = self.keys[iKey], self.keys[iChild2]
                    self.vals[iChild2], self.vals[iKey] = self.vals[iKey], self.vals[iChild2]
                    iKey = iChild2

                # Update children
                iChild1 = iKey * 2 + 1
                iChild2 = iKey * 2 + 2
            else:   # no bubble down necessary
                done = True

        # If new position has 1 or 0 kids, do final swap if necessary and then exit the while loop.
        if not done:    # heap not fully arranged yet, but node has at most 1 child
            if iChild1 < len(self.keys):    # value has one child. Bubble down if necessary
                if x > self.keys[iChild1]:
                    # swap
                    self.keys[iChild1], self.keys[iKey] = self.keys[iKey], self.keys[iChild1]
                    self.vals[iChild1], self.vals[iKey] = self.vals[iKey], self.vals[iChild1]

        return [old_min_key, old_min_val]
