import math
import time

# Katie Hummel
# Fri 10/26/18
# pg. 209 of textbook

class BloomFilter:
    def __init__(self, count, falsePosPct=0): # count=num of thing to go in bloomfilter
        self.numBits = math.ceil(-1*(count * math.log(falsePosPct/100)) / ((math.log(2))**2)) # number of bits (m)
        self.numHashes = math.ceil((self.numBits/count)*math.log(2))
        self.bA = bytearray((self.numBits+7)//8)

        self.masks = {}
        for i in range(8):
            self.masks[i] = 1 << i

    def add(self, word): # doesn't have to be a word
        for i in range(self.numHashes):
            bitIdx = hash(word + str(i)) % self.numBits
            byteIdx = bitIdx >> 3 # bitIdx // 8
            exponent = bitIdx & 7 # bitIdx % 8 # index into byte
            mask = self.masks[exponent] # 2**exponent # 1 << exponent
            self.bA[byteIdx] |= mask

    def __contains__(self, word):
        for i in range(self.numHashes):
            bitIdx = hash(word + str(i)) % self.numBits
            byteIdx = bitIdx >> 3  # bitIdx // 8
            exponent = bitIdx & 7  # bitIdx % 8
            mask = self.masks[exponent] # 2**exponent # 1 << exponent
            value = self.bA[byteIdx] & mask
            if value == 0:
                return False
        return True

    def __str__(self):
        rv = str(self.numHashes) + " " + str(len(self.bA)) + "\n"
        for i in range(len(self.bA)-1, -1, -1):
            rv += bin(self.bA[i])
        return rv

def readDict(filename):
    words = []
    with open(filename, 'r') as wordsInfile:
        for line in wordsInfile:
            words.append(line.strip())
    return words

def getDecWords(filename):
    decWords = []
    # create list of declaration words
    with open(filename, 'r') as decInfile:
        for line in decInfile:
            words = line.split()
            for word in words:
                if "." in word and "-" in word:
                    periodIdx = word.index(".")
                    dashIdx = word.index("-")
                    firstWord = word[:periodIdx].lower().strip()
                    secondWord = word[periodIdx + 3:].lower().strip()
                    decWords.append(firstWord)
                    decWords.append(secondWord)
                elif word[0] == "-":
                    decWords.append(word[2:].lower().strip())
                elif word.strip()[-1] in ".,:;-":
                    decWords.append(word.lower().strip()[:-1])
                elif word != "&":
                    decWords.append(word.lower().strip())
    return decWords


def main():
    words = readDict('wordsEn.txt')

    bf = BloomFilter(len(words), .5)

    # add words to bloom filter
    # time computation
    startTime = time.time()
    for word in words:
        bf.add(word)
    endTime = time.time()
    total = endTime-startTime
    print("Time of adding to bloom filter: {:.3f}sec".format(total))
    print()

    decWords = getDecWords('declaration.txt')

    # spell check The Declaration of Independence
    print("Incorrect words:")
    for word in decWords:
        if word not in bf:
            print(word)

# computational time for adding to bf using // and %: ~4.88 sec
# computational time for adding to bf using shift operations: ~4.45 sec
# computational time for adding to bf using shift operations and dict for mask values: ~4.35 sec

# Note to self:
# can tell if a bit is on by using a mask and anding it
# mask used to turn bits on and off

if __name__ == "__main__":
    main()

