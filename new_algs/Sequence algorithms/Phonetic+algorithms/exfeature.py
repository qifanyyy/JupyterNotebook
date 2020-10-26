from gensim.models.word2vec import Word2VecKeyedVectors
import jieba
import numpy as np

class Feature_extract(object):
    # construction function
    def __init__(self):
        self.wv = Word2VecKeyedVectors.load(
            '/Users/linjliang/Learning/PROJECT/workspace/functional/Tencent_AILab_smallEmbedding/1M.bin', mmap='r')

    # extract feature: time span
    def timedetect(self,sentences):
        for i in range(len(sentences)-1):
            time_span = sentences[i+1].getbg() - sentences[i].geted()
            if time_span >= 1: sentences[i+1].settinterval(1)
            else: sentences[i+1].settinterval(0)
        sentences[0].settinterval(0)
        return 0

    # compute similarity between strings
    def compute_string(self,s1,s2):
        # string to word lists
        list1 = list(jieba.cut(s1))
        list2 = list(jieba.cut(s2))
        # preserve existing words
        wlist1 = [item for item in list1 if item in self.wv]
        wlist2 = [item for item in list2 if item in self.wv]
        # compute similarity
        len1,len2 = len(wlist1),len(wlist2)
        sim_matrix = np.zeros((len1,len2))  # similarity matrix
        for i in range(len1):
            for j in range(len2):
                sim_matrix[i,j] = self.wv.similarity(wlist1[i],wlist2[j]) # similarity between words
        sim = ( sum(sim_matrix.max(axis=0)) + sum(sim_matrix.max(axis=1)) ) / (len1 + len2)
        return sim

    # extract feature: similarity score
    # Text Tiling
    def compute_simscore(self,sentences,k):
        length = len(sentences)
        # former k-1
        for i in range(k):
            str1, str2 = '', ''
            for j in range(i+1):
                str1 += sentences[j].getonebest()
                str2 += sentences[i+1+j].getonebest()
            sim = self.compute_string(str1,str2)
            sentences[i+1].setsimscore(sim)
        # middle
        for i in range(k,length-k):
            str1, str2 = '', ''
            for j in range(k):
                str1 += sentences[i-j].getonebest()
                str2 += sentences[i+1+j].getonebest()
            sim = self.compute_string(str1, str2)
            sentences[i + 1].setsimscore(sim)
        # latter
        for i in range(length-k, length-1):
            str1, str2 = '', ''
            for j in range(length-1-i):
                str1 += sentences[i-j].getonebest()
                str2 += sentences[i+1+j].getonebest()
            sim = self.compute_string(str1, str2)
            sentences[i + 1].setsimscore(sim)
        return 0

    # the difference of local maximum
    def local_maximum(self,sentences,pos):
        length = len(sentences)
        init = sentences[pos].getsimscore() # current sim-score
        left, right = pos, pos
        result = 0
        # left
        max = init
        while (left-1!=0) and (left!=0) and (sentences[left-1].getsimscore() >= sentences[left].getsimscore()):
            max = sentences[left-1].getsimscore()
            left -= 1
        result += (max-init)
        # right
        max = init
        while (right+1!=length) and (sentences[right+1].getsimscore() >= sentences[right].getsimscore()):
            max = sentences[right+1].getsimscore()
            right += 1
        result += (max-init)
        return result

    # extract feature: deep score
    def compute_deepscore(self,sentences):
        for i in range(len(sentences)):
            sentences[i].setdeepscore(self.local_maximum(sentences,i) )
        return 0