import sys, os
import Page_Rank_Utils as pru
from Power_Iteration import PowerMethod
from QR_Algorithm import qr_Algorithm_HH, qr_Algorithm_GS, shiftedQR_Algorithm
from Inverse_Iteration import InverseMethod
from Inverse_Iteration_w_shift import InverseShift
import matplotlib.pyplot as plt
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
web_scraper_folder = THIS_FOLDER[:-21] + "webCrawler/"
sys.path.append(web_scraper_folder)
import web_scraper
import networkx as nx
import csv
import time
import numpy as np
import ast
import re


def Stochastic_matrix_test():
    diG = nx.DiGraph()
    #3 is a dangling node
    diG.add_edge(1,2)
    diG.add_edge(1,3)
    diG.add_edge(1,4)
    diG.add_edge(2,3)
    diG.add_edge(4,3)

    M = pru.stochastic_transition_matrix_from_G(diG, False, 0.15)
    #print(M)

def web_scrawler_application(url, max_urls,  func_list, recal, weight=0.15):
    url_w = url.replace('.', '_')
    url_w = url_w.replace('/', '')
    url_w = re.sub('https:', '', url_w)
    directory = f"test_result_july30/{url_w}/{max_urls}"
    result_folder_path = os.path.join(THIS_FOLDER, directory)
    if not os.path.exists(result_folder_path):
        print("make it!")
        os.makedirs(result_folder_path)

    logf = open(result_folder_path + "/error.log", "w")
    f1 = open(result_folder_path + "/page_rank_algorithms_comparison.txt", "w")

    raw_adjacency_matrix_file = result_folder_path + "/raw_adjacency_matrix.npy"
    stochastic_matrix_file = result_folder_path + "/prepared_matrix.npy"
    internal_url_dict_file = result_folder_path + "/internal_url_dict.txt"
    recalculate = recal
    if not os.path.exists(stochastic_matrix_file) or not os.path.exists(internal_url_dict_file)  or recalculate:
        A, diG, internal_url_dict = web_scraper.scraper(url, max_urls)
        plt.spy(A)
        plt.title(f'Adjacency Matrix for {url} with {max_urls} urls')
        plt.savefig(result_folder_path+f'/{max_urls}_adhMatrix')
        plt.close()
        np.save(raw_adjacency_matrix_file , A)
        M = pru.stochastic_transition_matrix_from_G(diG, False, weight)
        np.save(stochastic_matrix_file, M)
        f_d = open(internal_url_dict_file, "w")
        f_d.write(str(internal_url_dict))
        f_d.close()
    else:
        A = np.load(raw_adjacency_matrix_file)
        plt.spy(A)
        plt.savefig(result_folder_path + f'/{max_urls}_adhMatrix')
        M = np.load(stochastic_matrix_file)
        f2 = open(internal_url_dict_file, "r")
        contents = f2.read()
        internal_url_dict = ast.literal_eval(contents)
        f2.close()

    converge_range = 0.0001
    for func in func_list:

        try:
            t_start = time.time()
            if func in [qr_Algorithm_GS, qr_Algorithm_HH, shiftedQR_Algorithm]:
                eigenvec, eigenval = func(M, converge_range=converge_range)
                eigenval = max(np.abs(eigenval))
                eigenvec = eigenvec[[0][0]]
                eigenvec = eigenvec/np.linalg.norm(eigenvec)
            else:
                eigenvec, eigenval = func(M, converge_range=converge_range, file_path=result_folder_path)
            t_end = time.time()
            time_length = t_end - t_start

            f1.write(f"algo: {func.__name__}   time:{time_length}\n")

            page_rank_dict = {}
            for i, page in enumerate(internal_url_dict):
                page_rank_dict[page] = eigenvec[i]

            try:
                page_rank_dict = sorted(page_rank_dict.items(), key=lambda x: x[1], reverse=True)
                fields = ['Link', 'Page Rank Score']
                with open(result_folder_path + f"/{func.__name__}_page_rank.csv", "w", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)
                    for item in page_rank_dict:
                        writer.writerow(item)
                    print(f"dominant eigenvector: {eigenvec}", file=f)
                    print(f"dominant eigenvalue: {eigenval}", file=f)
            except:
                logf.write(f'\nalgorithm {func.__name__} cannot give out right eigenvector format')
        except:
            logf.write(f'\nalgorithm {func.__name__} doesnt work when solving the eigenvector')
            pass


    f1.close()

if __name__ == '__main__':
    print("###Page Ranking###")
    #another good attemp: https://mathworld.wolfram.com/
    filename = sys.argv[-1]
    file1 = open(filename, 'r')
    lines = file1.readlines()
    url = lines[0].strip()
    max_urls = int(lines[1].strip())
    recal = int(lines[2].strip())
    print(url)
    """
    import argparse

    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("-u", "--url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)

    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls
    
    #comment bove out if you don't want to use shell
    url = "https://icerm.brown.edu/"
    max_urls = 30
    """

    func_list = [PowerMethod, qr_Algorithm_HH, qr_Algorithm_GS, shiftedQR_Algorithm, InverseMethod, InverseShift]
    print(max_urls)
    web_scrawler_application(url, max_urls, func_list, recal)
    Stochastic_matrix_test()
