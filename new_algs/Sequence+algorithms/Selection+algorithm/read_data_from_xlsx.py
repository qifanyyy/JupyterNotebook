__author__ = 'Nerya Yekutiel'

import xlrd
import os
import numpy as np

amount_of_criteria = 18
amount_of_alternatives = 49

def readMatrixFromSheet(startRow, startCol, rows, cols, sheet, datatype=None):
    if datatype is None:
        matrix = np.ndarray((rows, cols))
        for i in range(rows):
            for j in range(cols):
                data = sheet.cell_value(i + startRow, j + startCol)
                matrix[i][j] = sheet.cell_value(i + startRow, j + startCol)
    else:
        matrix = list()
        for i in range(rows):
            for j in range(cols):
                matrix.append(sheet.cell_value(i + startRow, j + startCol))

    return matrix


def normelizeDataFromXlsx(valueMatrix):
    dims = valueMatrix.shape
    normelizedValuesMatrix = valueMatrix.copy()
    for j in range(dims[1]):    # for each criteria
        maxVal = valueMatrix[:, j:j + 1].max()   # get the max of the column
        minVal = valueMatrix[:, j:j + 1].min()  # get the min of the column
        denominator = maxVal - minVal
        normelizedValuesMatrix[:, j:j + 1] = (valueMatrix[:, j:j + 1] - minVal) / denominator
    return normelizedValuesMatrix




def getValuesFromXlsx():
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    excelFile = os.path.join(BASE_PATH, 'data_excel.xlsx')
    wb = xlrd.open_workbook(excelFile)
    sheet = wb.sheet_by_index(0)
    criteriaPosNegVector = readMatrixFromSheet(0, 1, 1, amount_of_criteria, sheet)
    criteriaVector = np.array(readMatrixFromSheet(1, 1, 1, amount_of_criteria, sheet, np.unicode_))
    familyWeightVector = np.array(readMatrixFromSheet(2, 1, 1, amount_of_criteria, sheet, np.unicode_))
    teenagerWeightVector = np.array(readMatrixFromSheet(3, 1, 1, amount_of_criteria, sheet, np.unicode_))
    goldenAgeWeightVector = np.array(readMatrixFromSheet(4, 1, 1, amount_of_criteria, sheet, np.unicode_))
    carsVector = np.array(readMatrixFromSheet(6, 0, amount_of_alternatives, 1, sheet, np.unicode_))
    valueMatrix = normelizeDataFromXlsx(readMatrixFromSheet(6, 1, amount_of_alternatives, amount_of_criteria, sheet))
    return criteriaPosNegVector,\
           criteriaVector, \
           familyWeightVector,\
           teenagerWeightVector,\
           goldenAgeWeightVector, \
           carsVector,\
           valueMatrix




