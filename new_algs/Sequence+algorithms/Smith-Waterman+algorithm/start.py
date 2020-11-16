import glob
import os
import shutil

from algorithm import SmithWaterman                     #importing libraries and functions

avgweight = []                                            #declaring empty lists, so that value can be inserted into them later
maximumweight = []
mostsimsentence1 = []
mostsimsentence2 = []


def RemoveUnusedPunctuation(str):                           #removing punctuations
    new_str = str.replace('!', '')

    new_str = new_str.replace(',', '')

    new_str = new_str.replace(':', '')

    new_str = new_str.replace(';', '')

    new_str = new_str.replace('?', '')

    new_str = new_str.replace('\'', '')

    new_str = new_str.replace('"', '')

    new_str = new_str.replace('(', '')

    new_str = new_str.replace(')', '')

    return (new_str)


def CalculateSimilarity(string1, string2):                  #function calling with string1 and string2

    weight = 0.0
    averageWeight = 0.0
    totalWeight = 0.0
    maxWeight = 0.0
    mostSimilarSentence1 = ""
    mostSimilarSentence2 = ""
    numOfComparison = 0
    #string 1 is the main text everytime whereas content of string 2 varies from the string's list

    if len(string1)==0:
        avgweight.append(str(averageWeight))  # appending every result in the empty list everytime
        maximumweight.append(str(maxWeight))
        mostsimsentence1.append(str(mostSimilarSentence1))
        mostsimsentence2.append(str(mostSimilarSentence2))
    elif len(string2)==0:
        avgweight.append(str(averageWeight))  # appending every result in the empty list everytime
        maximumweight.append(str(maxWeight))
        mostsimsentence1.append(str(mostSimilarSentence1))
        mostsimsentence2.append(str(mostSimilarSentence2))
    elif string1 is string2:
        averageWeight=100
        maxWeight=100
        mostSimilarSentence1="Everything matches"
        mostSimilarSentence2 = "Everything matches"
        avgweight.append(str(averageWeight))  # appending every result in the empty list everytime
        maximumweight.append(str(maxWeight))
        mostsimsentence1.append(str(mostSimilarSentence1))
        mostsimsentence2.append(str(mostSimilarSentence2))
    else:
        string1=RemoveUnusedPunctuation(string1)
        string2= RemoveUnusedPunctuation(string2)


        listOfSentenceFromString1 = string1.lower().strip().split(".")          #splitting all content sentence wise; removing their trailing and starting whitespaces; changing them into lower cases
        listOfSentenceFromString2 = string2.lower().strip().split(".")



        for sentence1 in listOfSentenceFromString1:
            for sentence2 in listOfSentenceFromString2:

                listOfWords1 =sentence1.strip().split(" ")          #Splitting every word
                listofWords2 =sentence2.strip().split(" ")


            #Calculating similarity

                weight=SmithWaterman(listOfWords1, listofWords2)
                if weight > maxWeight:
                    maxWeight=weight
                    mostSimilarSentence1=str(sentence1)
                    mostSimilarSentence2=str(sentence2)
                totalWeight+= weight
                numOfComparison =numOfComparison+1

        averageWeight = format((totalWeight / float(numOfComparison)),'.2f')

        avgweight.append(str(averageWeight))                        #appending every result in the empty list everytime
        maximumweight.append(str(maxWeight))
        mostsimsentence1.append(str(mostSimilarSentence1))
        mostsimsentence2.append(str(mostSimilarSentence2))


# read files

def LoadFiles():

    sourcepath = './uploads'
    sourcefiles = os.listdir(sourcepath)
    destinationpath1 = './main'
    destinationpath2 = './others'
    for file in sourcefiles:
        if file.split('.', )[0].lower() == 'main':
            shutil.move(os.path.join(sourcepath, file), os.path.join(destinationpath1, file))
            print('main location changed')
        else:
            shutil.move(os.path.join(sourcepath, file), os.path.join(destinationpath2, file))
            print('other location changed')


    f1 = open('./main/main.txt','r')                           #reading main text as string 1
    string1 = ""
    while 1:
        line = f1.readline()
        if not line:break
        string1 += line
    f1.close()

    file_list = glob.glob(os.path.join(os.getcwd(), "./others", "*.txt"))        #path from where the folder for files is looked upon

    strings = []  # assigning empty list for all file content in the folder; each file is a new element inside of list
    allfile = []     #list to store the filename

    filename= os.listdir('./others')


    for file in filename:
        file= (str(file)).split(".")[0]                                                        #operation to split extensions and only take the filename
        allfile.append(file)


    for file_path in file_list:

        with open(file_path) as f_input:
            strings.append(f_input.read())                      #reading all files from the folder and storing them in a list

    # print(strings)

    count1=0
    for file in filename:
        string2=str(strings[count1])
        CalculateSimilarity(string1, string2)                   #passing each combinations of file via loop
        count1=count1+1


    count2=0
    for file in filename:                                               #printing out result
        print()
        print("Filename:"+allfile[count2])
        print("Calculated Similarity:"+avgweight[count2])
        print("Maximum Similarity between two sentences:"+maximumweight[count2])
        print("Most Similar sentence in main file:" + mostsimsentence1[count2])
        print("Most Similar sentence in file: "+allfile[count2]+":-"+mostsimsentence2[count2])
        print()
        print()
        count2=count2+1

    combo=zip(allfile,avgweight)

    other_location = glob.glob('./others/*')

    for f in other_location:
        os.remove(f)
        print('file deleted')

    main_location = glob.glob('./main/*')

    for f in main_location:
        os.remove(f)
        print('main file deleted')

    return (combo)

