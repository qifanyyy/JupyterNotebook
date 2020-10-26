from stringMatcher import *
from functools import partial
import random
import operator


misspell = []
correct = []
dictionary = []
soundexMisspellData = []
soundexDictionaryData = []

needlmanWunschAccurateGuesses = 0
smithWatermanAccurateGuesses = 0
soundexAccurateGuesses = 0 

needlmanWunschCorrectRecalls = 0
smithWatermanCorrectRecalls = 0
soundexCorrectRecalls = 0 

totalWordsRecalled = 0
totalWordsGuessed = 0

needlmanWunschIndex = 0
smithWatermanIndex = 1
soundexIndex = 2

def fileImport(fileName):

    importList = []
    with open(fileName) as inputfile:
        for line in inputfile:
            importList.append(line.strip())
    
    return importList

def importFiles():
    misspell.extend(fileImport('misspell.txt'))
    correct.extend(fileImport('correct.txt'))
    dictionary.extend(fileImport('dictionary.txt'))

def importSoundexFiles():
    soundexMisspellData.extend(fileImport('misspellSoundexStrings.txt'))
    soundexDictionaryData.extend(fileImport('dictionarySoundexStrings.txt'))

def getNextWord():
    for word in dictionary:
        yield(word)

"""
Returns a random element from a list
"""        
def getRandomElement(bestIndexList):
    "Assigns a random element to bestIndex."
    if(len(bestIndexList)>1):
        randomIndex = random.randint(0,(len(bestIndexList)-1))
        bestIndex = bestIndexList[randomIndex]
        return bestIndex
    elif(len(bestIndexList)>0): 
        return bestIndexList[0]
    else:
        return -1

"Map a partial function to the dictionary and return the match with best score"
def editDistanceMatchWithDictionary(partialFunction):
    matchScore = list(map(partialFunction,dictionary))
    bestIndex, bestValue = max(enumerate(matchScore), key=operator.itemgetter(1))
    
    "Stores the indicies of the best matchScore."
    bestIndexList = []

    "Loop through matchScore to find multiple bestValues."
    for i in range(0,len(matchScore)):
        if(matchScore[i] == bestValue):
            bestIndexList.append(i)
        
    return bestIndexList

"Map a partial function to the dictionary and return the match with best score"
def editDistanceMatchWithList(partialFunction, inputList):
    matchScore = list(map(partialFunction,inputList))
    bestIndex, bestValue = max(enumerate(matchScore), key=operator.itemgetter(1))
    
    "Stores the indicies of the best matchScore."
    bestIndexList = []

    "Loop through matchScore to find multiple bestValues."
    for i in range(0,len(matchScore)):
        if(matchScore[i] == bestValue):
            bestIndexList.append(inputList[i])
        
    return bestIndexList



"""Updates the accuracy score of algorithm
0 for Needleman Wunsch Score, 1 for Smith Waterman Score"""
def updateAccuracyScore(algorithm, guess, correct):
    score = 0
    global needlmanWunschAccurateGuesses
    global smithWatermanAccurateGuesses
    global soundexAccurateGuesses
    global totalWordsGuessed
    
    result = False

    if(guess == correct):
        score = 1
        result = True

    if(algorithm == needlmanWunschIndex):
        needlmanWunschAccurateGuesses += score
        totalWordsGuessed += 1
        "print(needlmanWunschAccurateGuesses)"
    elif(algorithm == smithWatermanIndex):
        smithWatermanAccurateGuesses += score
        totalWordsGuessed += 1
        "print(smithWatermanAccurateGuesses)"
    elif(algorithm == soundexIndex) :
        soundexAccurateGuesses += score
        totalWordsGuessed += 1 
    else:
        pass
    
    return result

"""
Update Recall Score based on the algorithm 
recall - whether the recall is true or false
"""
def updateRecallScore(algorithm, recall):
    global needlmanWunschCorrectRecalls
    global smithWatermanCorrectRecalls
    global soundexCorrectRecalls
    global totalWordsRecalled
    if(recall):
        recallResult = 1
    else:
        recallResult = 0

    if(algorithm == needlmanWunschIndex):
        needlmanWunschCorrectRecalls+= recallResult
        totalWordsRecalled += 1
        "print(needlmanWunschAccurateGuesses)"
    elif(algorithm == smithWatermanIndex):
        smithWatermanCorrectRecalls += recallResult
        totalWordsRecalled += 1
        "print(smithWatermanAccurateGuesses)"
    elif(algorithm == soundexIndex):
        soundexCorrectRecalls += recallResult
        totalWordsRecalled += 1 
    else:
        pass

"""
Calculate Recall Score based on the algorithm 
"""
def calculateRecallScore(algorithm):
    global needlmanWunschCorrectRecalls
    global smithWatermanCorrectRecalls
    global soundexCorrectRecalls
    global totalWordsRecalled
    if(algorithm == needlmanWunschIndex):
        return (needlmanWunschCorrectRecalls/totalWordsRecalled*100)
    elif(algorithm == smithWatermanIndex):
        return (smithWatermanCorrectRecalls/totalWordsRecalled*100)
    elif(algorithm == soundexIndex):
        return (soundexCorrectRecalls/totalWordsRecalled*100)
    else:
        pass


"""Calculates the accuracy score of an algorithm
algorithm - the index of the algorithm under consideration.
Algorithms are documented as global variables"""
def calculateAccuracyScore(algorithm):
    global needlmanWunschAccurateGuesses
    global smithWatermanAccurateGuesses
    global soundexAccurateGuesses
    global totalWordsGuessed

    if(algorithm == needlmanWunschIndex):
        return (needlmanWunschAccurateGuesses/totalWordsGuessed*100)
    elif(algorithm == smithWatermanIndex):
        return (smithWatermanAccurateGuesses/totalWordsGuessed*100)
    elif(algorithm == soundexIndex):
        return (soundexAccurateGuesses/totalWordsGuessed*100)
    else:
        pass


"""Corrects Misspelled Words using NeedlmanWunsch Algorithm,
calculates the accuracy and logs the results in a text file """
def correctMispelledWordsUsingNeedlmanWunsch():
    print("Running Needlman Wunsch Algorithm")
    global needlmanWunschAccurateGuesses
    global totalWordsGuessed

    needlmanWunschResults = open("neelmanWunschResults.txt","w")
    needlmanWunschResults.write("Misspelled\tGuess\tCorrect\tRecall\n")

    needlmanWunschAccurateGuesses = 0
    totalWordsGuessed = 0
    
    for misspellWord in misspell:
        needlmanWunschPartial = partial(needlmanWunsch, misspellWord)
        
        guessWordList = editDistanceMatchWithDictionary(needlmanWunschPartial)
        bestIndex = getRandomElement(guessWordList)
        guessWord = dictionary[bestIndex]
        correctWord = correct[misspell.index(misspellWord)]

        
        found = updateAccuracyScore(needlmanWunschIndex, guessWord, correctWord)

        if(found):
            recall = True
        else:
            recall = isPresent(guessWordList, correctWord)


        updateRecallScore(needlmanWunschIndex, recall)
        print(misspellWord, guessWord, correctWord, recall, len(guessWordList))
        needlmanWunschResults.write("%s %s %s %s %s\n"% (misspellWord, guessWord,correctWord, recall, len(guessWordList)))
    
    recallScore = calculateRecallScore(needlmanWunschIndex)
    accuracyScore = calculateAccuracyScore(needlmanWunschIndex)

    print("Accuracy Score: %s"%accuracyScore)
    print("Recall Score: %s"%recallScore)


    needlmanWunschResults.write("Accuracy Score:%s\n" % accuracyScore)
    needlmanWunschResults.write("Recall Score:%s\n" % recallScore)
    needlmanWunschResults.close()


"""Corrects Misspelled Words using NeedlmanWunsch Algorithm,
calculates the accuracy and logs the results in a text file """
def correctMispelledWordsUsingSmithWaterman():
    print("Running smith waterman algorithm")
    global smithWatermanAccurateGuesses
    global totalWordsGuessed
        
    smithWatermanAccurateGuesses = 0
    totalWordsGuessed = 0

    smithWatermanResults = open("smithWatermanResults.txt","w")
    smithWatermanResults.write("Misspelled\tGuess\tCorrect\tRecall\n")

    for misspellWord in misspell:
        smithWatermanPartial = partial(smithWaterman, misspellWord)
        
        guessWordList = editDistanceMatchWithDictionary(smithWatermanPartial)
        bestIndex = getRandomElement(guessWordList)
        guessWord = dictionary[bestIndex]
        correctWord = correct[misspell.index(misspellWord)]
        
        found = updateAccuracyScore(smithWatermanIndex, guessWord, correctWord)

        if(found):
            recall = True
        else:
            recall = isPresent(guessWordList, correctWord)
        
        updateRecallScore(smithWatermanIndex, recall)

        print(misspellWord, guessWord, correctWord, recall, len(guessWordList))
        smithWatermanResults.write("%s %s %s %s %s\n"% (misspellWord, guessWord,correctWord, recall, len(guessWordList)))
        accuracyScore = calculateAccuracyScore(smithWatermanIndex)
    
    recallScore = calculateRecallScore(smithWatermanIndex)

    print("Accuracy Score: %s"%accuracyScore)
    print("Recall Score: %s"%recallScore)

    smithWatermanResults.write("Accuracy Score:%s\n" % accuracyScore)
    smithWatermanResults.write("Recall Score:%s\n" % recallScore)
    smithWatermanResults.close()


"""Corrects Misspelled Words using Soundex Algorithm, 
and logs the results in a text file. 
"""
def correctMispelledWordsUsingSoundex():
    print("Running Soundex Algorithm")
    global soundexAccurateGuesses
    global totalWordsGuessed
    global soundexCorrectRecalls

    soundexAccurateGuesses = 0
    totalWordsGuessed = 0
    soundexCorrectRecalls = 0

    soundexResults = open("soundexResults.txt","w")
    soundexResults.write("Misspelled\tGuess\tCorrect\tRecall\n")
    
    for soundexMisspellWord in soundexMisspellData:
        guessWord = compareSoundexStringWithDictionaryForAccuracy(soundexMisspellWord)
        "guessWordFilteredNeedlman = compareSoundexStringWithDictionaryAndNeedlmanForAccuracy(soundexMisspellWord, soundexMisspellData.index(soundexMisspellWord))"
        correctWord = correct[soundexMisspellData.index(soundexMisspellWord)]
        misspellWord = misspell[soundexMisspellData.index(soundexMisspellWord)]

        recall = compareSoundexStringWithDictionaryForRecall(soundexMisspellWord, correctWord)

        updateAccuracyScore(soundexIndex, guessWord, correctWord)
        updateRecallScore(soundexIndex, recall)

        soundexResults.write("%s\t%s\t%s\t%s\n"%(misspellWord,guessWord, correctWord,recall))
        print("%s\t%s\t%s\t%s\n"%(misspellWord,guessWord, correctWord, recall))

    
    soundexAccuracyScore = calculateAccuracyScore(soundexIndex)
    soundexRecallScore = calculateRecallScore(soundexIndex)

    soundexResults.write("Soundex Accuracy Score:%s\n" % soundexAccuracyScore)
    soundexResults.write("Soundex Recall Score:%s\n" % soundexRecallScore)
    
    
    print("Soundex Accuracy Score:%s\n" % soundexAccuracyScore)
    print("Soundex Recall Score:%s\n" % soundexRecallScore)
    soundexResults.close()


    """Corrects Misspelled Words using Soundex Algorithm and Needlman Filtering, 
and logs the results in a text file. 
"""
def correctMispelledWordsUsingSoundexAndNeedlman():
    print("Running Soundex with Needleman Algorithm")
    global soundexAccurateGuesses
    global totalWordsGuessed
    global soundexCorrectRecalls

    soundexAccurateGuesses = 0
    totalWordsGuessed = 0
    soundexCorrectRecalls = 0

    soundexResults = open("soundexNeedlemanResults.txt","w")
    soundexResults.write("Misspelled\tGuess\tCorrect\tRecall\n")
    
    for soundexMisspellWord in soundexMisspellData:
        guessWord = compareSoundexStringWithDictionaryAndNeedlmanForAccuracy(soundexMisspellWord, soundexMisspellData.index(soundexMisspellWord))
        correctWord = correct[soundexMisspellData.index(soundexMisspellWord)]
        misspellWord = misspell[soundexMisspellData.index(soundexMisspellWord)]

        recall = compareSoundexStringWithDictionaryForRecall(soundexMisspellWord, correctWord)

        updateAccuracyScore(soundexIndex, guessWord, correctWord)
        updateRecallScore(soundexIndex, recall)

        soundexResults.write("%s\t%s\t%s\t%s\n"%(misspellWord,guessWord, correctWord,recall))
        print("%s\t%s\t%s\t%s\n"%(misspellWord,guessWord, correctWord, recall))

    
    soundexAccuracyScore = calculateAccuracyScore(soundexIndex)
    soundexRecallScore = calculateRecallScore(soundexIndex)

    soundexResults.write("Soundex Accuracy Score:%s\n" % soundexAccuracyScore)
    soundexResults.write("Soundex Recall Score:%s\n" % soundexRecallScore)
    
    
    print("Soundex Accuracy Score:%s\n" % soundexAccuracyScore)
    print("Soundex Recall Score:%s\n" % soundexRecallScore)
    soundexResults.close()


"""Corrects Misspelled Words using Needlman Wunsch Algorithm,
 and Smith Wateman Algorithm calculates the accuracy 
 and logs the results in a text file """
def correctMispelledWords():
    global smithWatermanAccurateGuesses
    global needlmanWunschAccurateGuesses
    global totalWordsGuessed
        
    smithWatermanAccurateGuesses = 0
    needlmanWunschAccurateGuesses = 0
    totalWordsGuessed = 0

    combinedResults = open("combinedResults.txt","w")
    combinedResults.write("Misspelled Word \t NeedlmanWunsch Guess \t SmithWaterman Guess \t Correct Word\n")
    
    for misspellWord in misspell:
        needlmanWunschPartial = partial(needlmanWunsch, misspellWord)
        needlmanWunschGuessWord = editDistanceMatchWithDictionary(needlmanWunschPartial)
        
        smithWatermanPartial = partial(needlmanWunsch, misspellWord)
        smithWatermanGuessWord = editDistanceMatchWithDictionary(needlmanWunschPartial)
        
        correctWord = correct[misspell.index(misspellWord)]
        
        updateAccuracyScore(smithWatermanIndex, smithWatermanGuessWord, correctWord)
        updateAccuracyScore(needlmanWunschIndex, needlmanWunschGuessWord, correctWord)
        
        combinedResults.write("%s \t %s \t %s \t %s \n"%(misspellWord
        ,needlmanWunschGuessWord, smithWatermanGuessWord, correctWord))
        
        print(misspellWord,"Needlaman Wunsch:", needlmanWunschGuessWord,"Smith Waterman:"
        ,smithWatermanGuessWord, correctWord)

    needlmanWunschAccuracyScore = calculateAccuracyScore(needlmanWunschIndex)
    smithWatermanAccuracyScore = calculateAccuracyScore(smithWatermanIndex)

    combinedResults.write("Needlman Wunsch Accuracy Score:%s\n" % needlmanWunschAccuracyScore)
    combinedResults.write("Smith Waterman Accuracy Score:%s\n" % smithWatermanAccuracyScore)
    
    combinedResults.close()

    """Generates soundex strings of the source list by creating a
    new file of the given fileName. One soundex string per line corresponding to the
    list"""
def generateSoundexStrings(sourceList, fileName):
    outputFile = open(fileName, "w")
    for word in sourceList:
        soundexWord = soundexConvertString(word)
        outputFile.write("%s\n"%soundexWord)
        "print(word, soundexWord)"
    outputFile.close()

def generateSoundexFiles():
    importFiles()
    generateSoundexStrings(misspell,"misspellSoundexStrings.txt")
    generateSoundexStrings(dictionary,"dictionarySoundexStrings.txt")

"""Compares a soundex string with dictionary and returns a random word
from the matched words
"""
def compareSoundexStringWithDictionaryForAccuracy(sourceSoundexString):
    soundexMatchIndices = compareSoundexStringWithDictionary(sourceSoundexString)

    bestMatchIndex = getRandomElement(soundexMatchIndices)


    "print(bestMatchIndex)"
    "print(soundexDictionaryData[bestMatchIndex])"
    if(bestMatchIndex != -1):
        return dictionary[bestMatchIndex]
    else:
        return "-"

"""Compares a soundex string with dictionary and returns a random word
from the matched words
"""
def compareSoundexStringWithDictionaryAndNeedlmanForAccuracy(sourceSoundexString, sourceSoundexStringIndex):
    soundexMatchIndices = compareSoundexStringWithDictionary(sourceSoundexString)
    needlmanWunschGuessWord = "-"
    soundexMatchWords = []

    for i in range(0, len(soundexMatchIndices)):
        soundexMatchIndex = soundexMatchIndices[i]
        soundexMatchWords.append(dictionary[soundexMatchIndex])
 
    if(len(soundexMatchIndices)>0):
        needlmanWunschPartial = partial(needlmanWunsch, misspell[sourceSoundexStringIndex])
        needlmanWunschGuessList = editDistanceMatchWithList(needlmanWunschPartial, soundexMatchWords)
        needlmanWunschGuessWord = getRandomElement(needlmanWunschGuessList)

    return needlmanWunschGuessWord



"""Compares a soundex string with dictionary and returns a True 
if the correct word is in the soundex list of guesses
"""
def compareSoundexStringWithDictionaryForRecall(sourceSoundexString, correctWord):
    soundexMatchIndices = compareSoundexStringWithDictionary(sourceSoundexString)
    correctWordIsPresent = isPresent(soundexMatchIndices, correctWord)
    return correctWordIsPresent
    


"""
Returns a list containing the indicies of the mataches
in soundexDictionaryData
"""
def compareSoundexStringWithDictionary(sourceSoundexString):
    soundexMatchIndices = []
    for i in range(0,len(soundexDictionaryData)):
        if(sourceSoundexString == soundexDictionaryData[i]):
            soundexMatchIndices.append(i)
    return soundexMatchIndices
    

"""
Returns true if the correctWord is present in the list of words
"""
def isPresent(listOfIndices, correctWord):
    for index in listOfIndices:
        if(dictionary[index] == correctWord):
            return True
    return False








importFiles()
generateSoundexFiles()
importSoundexFiles()


correctMispelledWordsUsingSoundex()
correctMispelledWordsUsingSoundexAndNeedlman()
correctMispelledWordsUsingNeedlmanWunsch()
correctMispelledWordsUsingSmithWaterman()

