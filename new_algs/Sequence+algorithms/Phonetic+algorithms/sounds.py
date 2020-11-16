from itertools import islice
from re import sub

### @package sounds
##    @brief Module providing the usual phonetic algorithms
##
##    The goal here is to find homophones using some of the established
##    phonetic algorithms like Soundex, Metaphone, Double Metaphone, etc.
##    The other purpose is simple syllable-based readability measures.
##    
##    Progress: Naive implementations of Soundex and Metaphone are complete,
##    along with simple Flesch tests for ease and grade level
    

###    @brief Straightforward implementation of a generalized Soundex algorithm
##
##    strInit is used to generate a code of length codeLength where consonantal
##    sounds are turned into numbered symbols representing like sounds
##
##    @param start False allows the usual Soundex property where the first letter
##    of the code is the first letter of the initial string. Setting to True means
##    the entire code will be digits in the case of a leading consonant, or else
##    a leading 'A' for a leading vowel
def Soundex(strInit, codeLength=4, start=False):

    ignored = "'.?!@hw"
    groups = (
        (' '),
        ('b', 'f', 'p', 'v'),
        ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'),
        ('d', 't'),
        ('l',),
        ('m', 'n'),
        ('r',),
        #('a', 'e', 'i', 'o', 'u', 'y')
        )
    strInit = strInit.lstrip()
    if not start:
        strFinal = [strInit[0]]
    strInit = strInit.lower()
    formerVal = 7
    curVal = 7
    inGroups = False
    for idx, group in enumerate(groups):
        if strInit[0] in group:
            formerVal = idx
            inGroups = True
            if start:
                strFinal = [str(idx)]
    if start and not inGroups:
        strFinal = ['A']
    inGroups = False
    strInit = ''.join(c for c in strInit if c not in ignored)
    for letter in strInit[1:]:
        for idx, group in enumerate(groups):
            if letter in group:
                curVal = idx
                inGroups = True
        if curVal != formerVal:
            if curVal != 0 and inGroups:
                strFinal.append(str(curVal))
        if not (inGroups):
            curVal = 7
        formerVal = curVal
        inGroups = False

    # len(strFinal) should be forced to codeLength (traditionally 4)
    strLen = len(strFinal)
    if strLen < codeLength:
        strFinal.extend(['0']*codeLength)

    return ''.join(strFinal[:4])

### @brief Helper function to get character-level n-grams from a source str
##
##  For example, getNGrams("Hello",2) should return a generator for:
##  "He", "el", "ll", "lo"
def getNGrams(source, n):
    for i in range(len(source)- n + 1):
        yield ''.join(islice(source, i, i + n))

### @brief Attempting to implement original Metaphone algorithm
##
##  See a verbal description https://en.wikipedia.org/wiki/Metaphone and
##  some BASIC code http://aspell.net/metaphone/metaphone.basic
##
##  @param initialVowel True differentiates leading vowels, while False
##  forces all leading vowels to "A"
##        
def Metaphone(strInit, initialVowel=True):
    strInit = strInit.upper()
    twoGrams = getNGrams(strInit, 2)
    threeGrams = getNGrams(strInit, 3)
    vowels = "AEIOU"
    softeners = ['I', 'E', 'Y']
    
    #previous and current 2Grams
    twos = [None, None]
    #previous two and current 3Grams
    threes = [None, None, None]

    #Deal with the first letter logic
    initialDict = {
        'KN': 'N',
        'GN': 'N',
        'PN': 'N',
        'AE': 'E',
        'WR': 'R'
        }


    for c in strInit:
        
        #increment the previous ngrams lists so that c is in each ngram
        twos[0] = twos[1]
        threes[0] = threes[1]
        threes[1] = threes[2]
        try:
            twos[1] = next(twoGrams)
        except:
            twos[1] = None
        try:
            threes[2] = next(threeGrams)
        except:
            threes[2] = None
            
        #Special case for beginning
        if threes[0] == None:
            if twos[0] == None:
                if twos[1] in initialDict:
                    finalList = [initialDict[twos[1]]]
                    continue
                else:
                    finalList = []
                    if c == 'X':
                        finalList.append('S')
                        continue
            if twos[0] in initialDict:
                continue
            
##        print(" Adding", c, 'to:', finalList)
        # Check for duplicate adjacent letters and skip when on the first
        if c != 'C' and twos[1] == c*2:
            continue

        # Aside from initial letter rule, vowels are dropped
        if c in vowels:
            continue
        
        # GH before something other than None (end) or vowel, eg before t, drops
        # "soft" G becomes J
        # 'GN' before end drops G
        if c == 'G':
            if twos[0] != 'GG':
                if twos[1] and twos[1][1] in softeners:
                    finalList.append('J')
                    continue
                if threes[2] == None and twos[1] == 'GN':
                    continue
                if twos[1] == 'GH':
                    if threes[2] == None or threes[2][2] not in vowels:
                        continue
            finalList.append('K')
            continue

        # 'C' in 'CK' drops, 'CIA', 'CH' yield 'X', but 'SCH' C becomes K
        # "soft" C becomes S
        if c == 'C':
            if threes[2] == 'CIA':
                finalList.append('X')
                continue
            if twos[1] == 'CH':
                if threes[1] == 'SCH':
                    finalList.append('K')
                    continue
                finalList.append('X')
                continue
            if twos[1][1] in softeners:
                finalList.append('S')
                continue
            finalList.append('K')
            continue

        # SH sound goes to X
        if c == 'S':
            if twos[1] == 'SH' or threes[2] in ('SIA', 'SIO'):
                finalList.append('X')
                continue

        if c == 'X':
            finalList.append('KS')
            continue

        # 'D' before soft G becomes 'J', else 'T'
        # Ignoring Wikipedia's rule "5. 'D' transforms to 'J'
        # if followed by 'GE', 'GY', 'GI', to avoid unnecessary
        # 'JJ' in output since the soft 'G' also gets sent to 'J'...
        if c == 'D':
            if twos[1] == 'DG' and threes[2] and threes[2][2] in softeners:
                continue
            finalList.append('T')
            continue

        if c == 'T':
            if threes[2] in ('TIA', 'TIO', 'TCH'):
                if threes[2] == 'TCH':
                    continue
                finalList.append('X')
                continue
            if twos[1] == 'TH':
                finalList.append('0')
                continue
            
        
        if c == 'P':
            if twos[1] == 'PH':
                finalList.append('F')
                continue

        if c == 'K':
            if twos[0][0] == 'C':
                continue
            finalList.append('K')
            continue

        # semi-vowels only carry through if before a vowel
        if c in ('W', 'Y'):
            if twos[1] and twos[1][1] in vowels:
                finalList.append(c)
                continue
            continue

        if c == 'Q':
            finalList.append('K')
            continue

        if c == 'V':
            finalList.append('F')
            continue

        # Drop B for final 'MB'
        if threes[2] == None and twos[0] == 'MB':
            continue

        # Word final GNED drops the 'G', but it would be added above
        # NIN is a cheating way to check for _GNING_; one solution
        # would be fours and fives using ngram helper again
        if c == 'N':
            if threes[2] in ('NED', 'NIN') and twos[0][0] == 'G':
                finalList = finalList[:-1]
            finalList.append('N')
            continue

        # Drop if after a vowel and not before a vowel
        # Also drop if after initial W or any P
        if c == 'H':
            if not twos[0]:
                finalList.append(c)
                continue
            if twos[0] in ('PH', 'CH', 'SH', 'TH'):
                continue
            if twos[0] == 'WH' and threes[0] == None:
                finalList.append('W')
                continue
            # If G came first, vowel rule uses letter before G
            if twos[0] == 'GH':
                prior = threes[0][0]
            else:
                prior = twos[0][0]
            if twos[1] and prior in vowels and twos[1][1] not in vowels:
                continue

        finalList.append(c)

    return ''.join(finalList)

### @brief Double Metaphone implementation
##
## 
##  Working off of http://aspell.net/metaphone/dmetaph.cpp and 
def doubleMetaphone(initStr):
    pass

### @brief naive syllable counting algorithm
##
##  Quick estimate of syllables in a string, useful for Flesch-Kincaid
##
def countSyllables(initStr, andWords=False, andLengths=False):
    syllables = 0
    words = initStr.upper().split(' ')
    words = [word for word in words if len(word)>0]
    initLen = len(words)
    
    if andLengths:
        wLengths = []
    for word in words:
        cvWord = ''.join(c for c in word if c.isalpha())

        alphaLen = len(cvWord)
        if alphaLen == 0:
            initLen -= 1
            continue
        if andLengths:
            wLengths.append(alphaLen)
        
        cvWord = sub("[^AEIOUY]", 'C', cvWord)
        cvWord = sub("[AEIOUY]", 'V', cvWord)
        
        # every space-delimited word counts as a syllable
        syllables += 1
        if len(word) > 3:
            if word[-1] == 'E':
                syllables -= 1
        
        threes = getNGrams(cvWord, 3)
        first = True
        for three in threes:
            if three == 'VVV':
                syllables += 1
            if three in ('VCV', 'CCV') and not first:
                syllables += 1
            first = False
    if andWords:
        if andLengths:
            return syllables, initLen, wLengths
        return syllables, initLen
    if andLengths:
        return syllables, wLengths
    return syllables

### @brief helper function for readability testing
##
def countSentences(initStr):
    finStr = initStr.upper()
    for abbreviation in ('MR. ', 'MS. ', 'MRS. ', 'DR. ', 'ST. '):
        finStr = sub(abbreviation, '', finStr)
    return len(finStr.split('. '))


### @brief Flesch and Flesch-Kincaid helper function
##
##  @return tuple with (words/sentence, syllables/word)
def fleschMetrics(initStr):
    sylls, words = countSyllables(initStr, andWords=True)
    sents = countSentences(initStr)
    return (float(words)/sents), (float(sylls)/words)

def fleschEase(initStr):
    wordOverSents, syllOverWords = fleschMetrics(initStr)
    return round(206.835 - 1.015*wordOverSents - 84.6*syllOverWords, 1)

def fleschKincaid(initStr):
    wordOverSents, syllOverWords = fleschMetrics(initStr)
    return round(0.39*wordOverSents + 11.8*syllOverWords - 15.59, 1)

### @brief comparison function to put the phonetic algorithms to use
##
##  For now, algorithm is meant to be Soundex or Metaphone or a partial
##  function of either to account for their optional arguments
##  lambda functions could also be passed in for example lambda x: x
##  so truth would only be if they match exactly, case and all
def isHomophone(a,b, algorithm=Soundex):
    return algorithm(a) == algorithm(b)
