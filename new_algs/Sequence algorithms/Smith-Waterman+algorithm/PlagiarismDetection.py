import difflib
import glob
import smith_waterman as sw
import numpy as np
import json
import collections as cl

class PlagiarismDetection(object):
    """ Plagiarism Detection class

    Parameters
    ------------
    alpha : int
        Threshold at traceback starting point of Smith-Waterman algorithm

    Attributes
    ------------
    rpart_ : list
        Plagiarized part of each reports
    wpart_ : list
        Plagiarize part of each website
    rate_ : list
        Plagiarized rate of each reports

    """

    def __init__(self, alpha=5, docx_paths=[]):
        self.alpha = alpha
        self.fname = docx_paths

    def compare(self, corpus, webinfo):
        """ Compare document and web info

        Parameters
        ------------
        corpus : list
            Document group of each report
        webinfo : Two-dimensional list
            Website information of each report

        Returns
        ------------
        self : object

        """
        self.rpart_ = []
        self.wpart_ = []
        self.rate_ = []

        fr = open('result.json', 'r')
        result_json = json.load(fr)
        fr.close()

        fw = open('result.json', 'w')
        r_i = 0
        for repo in corpus:
            repo_similar_part = ""
            repo_index_stack = np.zeros(len(repo))
            web_stack = []
            w_j = 0
            result_json[self.fname[r_i]]['repo_txt'] = repo
            for wi in webinfo[r_i]:
                result_json[self.fname[r_i]]['./data/webinfo/'+str(r_i)+'-'+str(w_j)+'.txt']['web_txt'] = wi
                print("----------------------------------------------------------------")
                repo_subrate_part = ""
                web_similar_part = ""
                web_similar_part_index, repo_similar_part_index = self.smith_waterman(wi, repo)
                repo_index_stack = np.array(np.logical_or(repo_index_stack, repo_similar_part_index), dtype=int)
                for i in np.where(repo_similar_part_index == 1)[0]:
                    repo_subrate_part += repo[i]
                result_json[self.fname[r_i]]['./data/webinfo/'+str(r_i)+'-'+str(w_j)+'.txt']['rate'] = len(repo_subrate_part) / len(repo)

                result_json[self.fname[r_i]]['./data/webinfo/'+str(r_i)+'-'+str(w_j)+'.txt']['repo_similar'] = repo_subrate_part
                for i in np.where(web_similar_part_index == 1)[0]:
                    web_similar_part += wi[i]
                result_json[self.fname[r_i]]['./data/webinfo/'+str(r_i)+'-'+str(w_j)+'.txt']['web_similar'] = web_similar_part
                web_stack.append(web_similar_part)
                w_j += 1
            for j in np.where(repo_index_stack == 1)[0]:
                repo_similar_part += repo[j]
            self.rpart_.append(repo_similar_part)
            self.wpart_.append(web_stack)
            self.rate_.append(len(repo_similar_part) / len(repo))
            result_json[self.fname[r_i]]['tot_rate'] = len(repo_similar_part) / len(repo)
            result_json[self.fname[r_i]]['tot_repo_similar'] = repo_similar_part
            r_i += 1
            print("----------------------------------------------------------------")
        json.dump(result_json, fw, ensure_ascii=False, indent=4)
        fw.close()

        return self

    def smith_waterman(self, row, column):
        """ Smith Waterman algorithm """
        return sw.calculate(row, column, self.alpha)

