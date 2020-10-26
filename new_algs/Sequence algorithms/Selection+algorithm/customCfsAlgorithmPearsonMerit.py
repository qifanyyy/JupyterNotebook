import numpy as np
import pandas as pd
import warnings

import math
import sys
from itertools import combinations


def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    xy_sum = 0
    x2_sum = 0
    y2_sum = 0
    x_sum = 0
    y_sum = 0
    for idx in range(n):
        xy_sum += x[idx] * y[idx]
        x2_sum += pow(x[idx], 2)
        y2_sum += pow(y[idx], 2)
        x_sum += x[idx]
        y_sum += y[idx]
    rxy = ((n * xy_sum) - ((x_sum) * (y_sum))) / (
            (math.sqrt((n * x2_sum) - pow(x_sum, 2))) * (math.sqrt((n * y2_sum) - pow(y_sum, 2))))
    return abs(rxy)


filename = sys.argv[1]

data = pd.read_csv('inputdata/' + filename)

with open('inputdata/' + filename) as f:
    first_line_head = f.readline().replace("\n", "").split(",")


corr_matrix = []
for i in (range(len(first_line_head))):
    row = []
    for j in range(len(first_line_head)):
        if j == i:
            row.append(1)
        elif i > j:
            row.append(None)
        else:
            row.append(pearson_def(data[first_line_head[i]], data[first_line_head[j]]))
    corr_matrix.append(row)


corr_matrix_df = pd.DataFrame(corr_matrix)
corr_matrix_df.columns = first_line_head

corr_matrix_df.insert(0, "column_name", first_line_head, True)

corr_matrix_df.set_index('column_name', inplace=True)

print("Correlation matrix DF")
print(corr_matrix_df)

F = []

M = []


features_to_select = first_line_head[:-1]
classifier = first_line_head[len(first_line_head)-1]

F = []
M = []

for c in range(len(features_to_select)+1):
    comb_attr = combinations(features_to_select, c)
    for i in list(comb_attr):
        if len(i) != 0:
            k = len(np.asarray(i))
            comb = combinations(np.asarray(i),2)
            sum_corrs = 0
            for n in list(comb):
                sum_corrs += corr_matrix_df.loc[np.asarray(n)[0], np.asarray(n)[1]]
            rff = sum_corrs/k
            rcf = corr_matrix_df.loc[np.asarray(i), classifier].mean()
            merit = (k*rcf)/(math.sqrt(k+k*(k-1)*rff))
            F.append(np.asarray(i))
            M.append(merit)

print("Selected features are:")

selectedFeatures = np.asarray(F[M.index(max(M))])
selectedFeatures2 = np.append(selectedFeatures,classifier)

print(data[selectedFeatures2])