from cache import *

R_MAX = 0.829608938547

def analyse(params):

    dictFilepath = "C:/Users/saumy/OneDrive/Desktop/Sem1/Knowledge Technologies/Project1KT_assignment1-master/KT_assignment1-master/KT1_code_final/src//dictionary.txt"
    misspell = open("C:/Users/saumy/OneDrive/Desktop/Sem1/Knowledge Technologies/Project1KT_assignment1-master/KT_assignment1-master/KT1_code_final/src/misspell.txt",'r').readlines()
    correct = open('C:/Users/saumy/OneDrive/Desktop/Sem1/Knowledge Technologies/Project1KT_assignment1-master/KT_assignment1-master/KT1_code_final/src//correct.txt', 'r').readlines()


    dictionary = {}
    correctSpelling = {}

    # convert the dictionary into a dict, strip \n
    for word in open(dictFilepath, 'r'):
        word = word.strip('\n')
        dictionary[word] = 1

    # define the set of intended spellings
    for i in range(0, len(misspell)):
        correctSpelling[misspell[i].strip('\n')] = correct[i].strip('\n')

    # Classes that implement various approximate string matching algorithms
    approxAlgs = init_cache(params, dictionary)

    for typo in misspell:
        typo = typo.strip('\n')

        for algorithm in approxAlgs:

            # Run the algorithms
            approxAlgs[algorithm].findCorrections(typo)


            # evaluate statistics
            approxAlgs[algorithm].stats['num_attempted'] += len(approxAlgs[algorithm].possibleSpellings[typo])

            try:
                # print algorithm
                # print typo
                # print sorted(approxAlgs[algorithm].possibleSpellings[typo])
                # print correctSpelling[typo]
                # print '\n'
                # this will KeyError unless the correct spelling was found by the algorithm
                if approxAlgs[algorithm].possibleSpellings[typo][correctSpelling[typo]]:

                    approxAlgs[algorithm].stats['match'] += 1

                    if len(approxAlgs[algorithm].possibleSpellings[typo]) == 1:
                        approxAlgs[algorithm].stats['perfect_match'] += 1

            except KeyError:
                approxAlgs[algorithm].stats['incorrect'] += 1

            # compute evaluation values
            if approxAlgs[algorithm].stats['num_attempted'] != 0:
                precision = float(approxAlgs[algorithm].stats['match'])/ approxAlgs[algorithm].stats['num_attempted']
                approxAlgs[algorithm].evaluation['precision'] = precision

            if (approxAlgs[algorithm].stats['match'] + approxAlgs[algorithm].stats['incorrect']) != 0:
                recall = float(approxAlgs[algorithm].stats['match'])\
                           / (approxAlgs[algorithm].stats['match'] + approxAlgs[algorithm].stats['incorrect'])

                recall = recall/R_MAX   # normalise recall
                approxAlgs[algorithm].evaluation['recall'] = recall

            if (approxAlgs[algorithm].stats['match'] + approxAlgs[algorithm].stats['incorrect']) != 0:
                accuracy = float(approxAlgs[algorithm].stats['perfect_match'])\
                           / (approxAlgs[algorithm].stats['match'] + approxAlgs[algorithm].stats['incorrect'])
                approxAlgs[algorithm].evaluation['accuracy'] = accuracy

            # if len (approxAlgs[algorithm].possibleSpellings[typo]) > 1:
            #     print(typo + str(approxAlgs[algorithm].possibleSpellings[typo]))

    for algorithm in approxAlgs:
        approxAlgs[algorithm].storeDat()
    write_cache(approxAlgs, params)

