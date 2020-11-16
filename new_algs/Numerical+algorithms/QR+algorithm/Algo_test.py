from Power_Iteration import PowerMethod
from QR_Algorithm import qr_Algorithm_HH, qr_Algorithm_GS, shiftedQR_Algorithm
from Inverse_Iteration import InverseMethod
from Inverse_Iteration_w_shift import InverseShift
import re
import numpy as np
import os
from numpy import linalg as LA
import operator
import ast
import csv
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def correctness_test(url, max_urls, func_list):

    url_w = url.replace('.', '_')
    url_w = url_w.replace('/', '')
    url_w = re.sub('https:', '', url_w)
    directory = f"test_result_july17/{url_w}/{max_urls}"
    result_folder_path = os.path.join(THIS_FOLDER, directory)
    stochastic_matrix_file = result_folder_path + "/prepared_matrix.npy"
    internal_url_dict_file = result_folder_path + "/internal_url_dict.txt"

    M = np.load(stochastic_matrix_file)
    f2 = open(internal_url_dict_file, "r")
    contents = f2.read()
    internal_url_dict = ast.literal_eval(contents)
    ###########################################
    # correctness test
    f = open(result_folder_path + "/july_30_Linalg_page_rank.csv", "w", newline='')
    w, v = LA.eigh(M)
    val_list = w.tolist()
    idx = val_list.index(max(val_list))
    eigenvec_np = v[:,idx]
    eigenvec_np = eigenvec_np/LA.norm(eigenvec_np)
    page_rank_dict = {}
    for i, page in enumerate(internal_url_dict):
        page_rank_dict[page] = eigenvec_np[i]

    page_rank_dict = sorted(page_rank_dict.items(), key=lambda x: x[1], reverse=True)

    fields = ['Link', 'Page Rank Score']
    writer = csv.writer(f)
    writer.writerow(fields)
    for item in page_rank_dict:
        writer.writerow(item)

    print(f"dominant eigenvector: {eigenvec_np}", file=f)
    print(f"dominant eigenvalue: {max(val_list)}", file=f)

    # for new funcs

    converge_range = 0.0001
    for func in func_list:
        try:
            if func in [qr_Algorithm_GS, qr_Algorithm_HH, shiftedQR_Algorithm]:
                eigenvec, eigenval = func(M, converge_range=converge_range)
                eigenval = max(np.abs(eigenval))
                eigenvec = eigenvec[[0][0]]
                eigenvec = eigenvec/np.linalg.norm(eigenvec)

            else:
                eigenvec, eigenval = func(M, converge_range=converge_range, file_path=result_folder_path)

            f.write(f"\n {func.__name__} eigenvalue is {eigenval}")
            f.write(f"\n {func.__name__} eigenvector is {eigenvec}")
            dist = np.linalg.norm(eigenvec - eigenvec_np)
            f.write(f"\nDistance for np and {func.__name__}: {dist}")
        except:
            pass

    ###########################################
    f.close()


if __name__ == '__main__':
    url = "https://icerm.brown.edu/"
    max_urls = 50
    func_list = [PowerMethod, qr_Algorithm_HH, qr_Algorithm_GS, shiftedQR_Algorithm, InverseMethod, InverseShift]
    correctness_test(url, max_urls, func_list)