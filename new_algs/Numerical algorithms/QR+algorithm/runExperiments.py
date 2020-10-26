import subprocess
from pathlib import *
import matplotlib.pyplot as plt
import os
from xlwt import Workbook

def saveExperimentsToExelTable(sheet1, listSizes):
    sheet1.write(0, 0, 'Size of matrix')

    sheet1.write(0, 1, 'Simple version')
    sheet1.write(1, 1, 'Time of decomposition')
    sheet1.write(1, 2, 'Time of calculation Q')
    sheet1.write(1, 3, '||A - Q * R||')

    sheet1.write(0, 4, 'RowHouse version')
    sheet1.write(1, 4, 'Time of decomposition')
    sheet1.write(1, 5, 'Time of calculation Q')
    sheet1.write(1, 6, '||A - Q * R||')

    sheet1.write(0, 7, 'Reverse accumulation version')
    sheet1.write(1, 7, 'Time of decomposition')
    sheet1.write(1, 8, 'Time of calculation Q')
    sheet1.write(1, 9, '||A - Q * R||')

    sheet1.write(0, 10, 'Final version')
    sheet1.write(1, 10, 'Time of decomposition')
    sheet1.write(1, 11, 'Time of calculation Q')
    sheet1.write(1, 12, '||A - Q * R||')

    sheet1.write(0, 13, 'Parallel version (2 threads)')
    sheet1.write(1, 13, 'Time of decomposition')
    sheet1.write(1, 14, 'Time of calculation Q')
    sheet1.write(1, 15, '||A - Q * R||')

    sheet1.write(0, 16, 'Parallel version (4 threads)')
    sheet1.write(1, 16, 'Time of decomposition')
    sheet1.write(1, 17, 'Time of calculation Q')
    sheet1.write(1, 18, '||A - Q * R||')

    sheet1.write(0, 19, 'Parallel version (8 threads)')
    sheet1.write(1, 19, 'Time of decomposition')
    sheet1.write(1, 20, 'Time of calculation Q')
    sheet1.write(1, 21, '||A - Q * R||')

    sheet1.write(0, 22, 'Givens rotation')
    sheet1.write(1, 22, 'Time of decomposition')
    sheet1.write(1, 23, 'Time of calculation Q')
    sheet1.write(1, 24, '||A - Q * R||')

    sheet1.write(0, 25, 'Parallel Givens rotation (2 threads)')
    sheet1.write(1, 25, 'Time of decomposition')
    sheet1.write(1, 26, 'Time of calculation Q')
    sheet1.write(1, 27, '||A - Q * R||')

    sheet1.write(0, 28, 'Parallel Givens rotation (4 threads)')
    sheet1.write(1, 28, 'Time of decomposition')
    sheet1.write(1, 29, 'Time of calculation Q')
    sheet1.write(1, 30, '||A - Q * R||')

    sheet1.write(0, 31, 'Parallel Givens rotation (8 threads)')
    sheet1.write(1, 31, 'Time of decomposition')
    sheet1.write(1, 32, 'Time of calculation Q')
    sheet1.write(1, 33, '||A - Q * R||')


    for i in range(2, len(listSizes) + 2, 1):
        sheet1.write(i, 0, listSize[i - 2])


def saveExperimentForOneMode(listTimeDecompositionForOneMode, listTimeSelectionQForOneMode, listAccuracyForOneMode, mode):
    numberOfColumn = (mode - 1) * 3 + 1 # 3 = count or columns

    for i in range(2, len(listTimeDecompositionForOneMode) + 2, 1):
        sheet1.write(i, numberOfColumn, listTimeDecompositionForOneMode[i - 2])

    numberOfColumn += 1
    for i in range(2, len(listTimeSelectionQForOneMode) + 2, 1):
        sheet1.write(i, numberOfColumn, listTimeSelectionQForOneMode[i - 2])

    numberOfColumn += 1
    for i in range(2, len(listAccuracyForOneMode) + 2, 1):
        sheet1.write(i, numberOfColumn, listAccuracyForOneMode[i - 2])

def savePng(name='', fmt='png'):
    pwd = os.getcwd()
    iPath = './pictures/{}'.format(fmt)
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    os.chdir(iPath)
    plt.savefig('{}.{}'.format(name, fmt), fmt='png')
    os.chdir(pwd)

def averageInList(floatList):
    return sum(floatList) / len(floatList)

def runExperiment(mode, size):
    command = f"{mode} {size}"
    output = subprocess.check_output(f"{path} {command}", shell=True, universal_newlines=True)
    _, outputDecomposition = output.split("Time for simple version of decomposition: ")
    outputDecomposition, outputSelectionQ = outputDecomposition.split("Time for simple version of Q: ")

    print(f"Time for decomposition = {outputDecomposition}")

    outputSelectionQ, outputMaxAbs = outputSelectionQ.split("Check result matrices...")
    print(f"Time for selection = {outputSelectionQ}")

    _, outputMaxAbs = outputMaxAbs.split("max abs = ")
    if " OK" in outputMaxAbs:
        outputMaxAbs, _ = outputMaxAbs.split(" OK", maxsplit=1)
    else:
        outputMaxAbs, _ = outputMaxAbs.split(" ERR", maxsplit=1)

    print(f"Accuracy = {outputMaxAbs}")

    return float(outputDecomposition), float(outputSelectionQ), float(outputMaxAbs)

if __name__ == "__main__":
    path = PurePath(r'C:\Users\Julia\source\repos\Householder\x64\Release\Householder.exe')
    listSize = [3, 5, 10, 50, 100, 300, 500, 800, 1000, 1500, 2000, 2500, 3000]
    listTimeDecompositionForOneMode = []
    listTimeSelectionQForOneMode = []
    listAccuracyForOneMode = []

    # Workbook is created
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('May 2020 - MS')
    saveExperimentsToExelTable(sheet1, listSize)
    '''
    command = "7 1000"
    output = subprocess.check_output(f"{path} {command}", shell=True, universal_newlines=True)
    _, outputDecomposition = output.split("Time for simple version of decomposition: ")

    '''
    for mode in range(3, 12, 1):
        listTimeDecompositionForOneMode.clear()
        listTimeSelectionQForOneMode.clear()
        listAccuracyForOneMode.clear()
        for size in listSize:
            if mode < 3 and size > 800:
                continue
            print("---------------------------------------------------------------- \n")
            print(f"mode = {mode}; size = {size} \n")
            decompositionList = []
            selectionQList = []
            accuracyList = []
            rangeEnd = 10
            if mode < 3 and size > 300:
                rangeEnd = 3

            for iter in range(0, rangeEnd, 1):
                outputDecomposition, outputSelectionQ, outputMaxAbs = runExperiment(mode, size)
                decompositionList.append(outputDecomposition)
                selectionQList.append(outputSelectionQ)
                accuracyList.append(outputMaxAbs)

            averageInDecompList = averageInList(decompositionList)
            listTimeDecompositionForOneMode.append(float(averageInDecompList))

            averageInSelectionQList = averageInList(selectionQList)
            listTimeSelectionQForOneMode.append(float(averageInSelectionQList))

            averageInAccuracyList = averageInList(accuracyList)
            listAccuracyForOneMode.append(float(averageInAccuracyList))


        saveExperimentForOneMode(listTimeDecompositionForOneMode, listTimeSelectionQForOneMode, listAccuracyForOneMode, mode)



    wb.save('May2020-experiments.xls')
    '''   fig = plt.figure()
    grid1 = plt.grid(True)
    graph1 = plt.plot(listSize, listTimeDecomposition, label="Insert in avl tree", color='red')


    #save("Insert", 'png')
    plt.show()
    
    '''