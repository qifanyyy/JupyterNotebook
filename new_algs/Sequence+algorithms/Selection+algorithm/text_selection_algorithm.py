#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 12:01:19 2018

TEXT SELECTION ALGORITHM SCRIPT

@author: marlene
"""
#IMPORTS
import re
import numpy as np
import matplotlib.pyplot as plt

#################
# CONFIGURATION #
#################


DEBUG = 1000
ARCTIC = 60000
FULL = 581905
corpus_size = DEBUG #flexible corpus size; set to DEBUG, ARCTIC (use as many 
#sentences as in the ARCTIC paper) or FULL (use all available sentences)
num_sentences = 10 #the number of sentences to be selected. set to the size of ARCTIC A
#input and output files
utt_file = "example_utts.txt" #the file containing flat festival utterances
text_file = "example_text.txt" #the file containing the original sentences
#in the same order as utt_file
out_file = "selected_text.txt" #the file to write the selected output to
utts_out = "selected_utts.txt" #keep the selected utterances also in a file

#names of the different wishlists/base type configurations
names = ["phones", "diphones", "triphones", "phones_stress", "diphones_stress", "triphones_stress"]
#choose a base type and wishlist
base_unit = "diphones" # "phones", "diphones" or "triphones"
stress = True #True/False; set true to consider stress as a factor
scoring_type = 2 #1 or 2; choose 2 for negative log-prob weights

#keep track of the sentences selected, to avoid selecting duplicates 
#(in case score drops to 0)
selected_sentence_ids = set()
selected_zeros = 0


##################
# CORE FUNCTIONS #
##################


def utt_to_phonesets(line):
    """find the phones/stressed phones in a flattened festival utterance"""
    #strip the utterance number away
    line = re.sub("utt[0-9]+", "", line)
    #replace the break symbols by silence; here I just assume silence for 
    #either a small (B) or big break (BB)
    line = re.sub("BB?", "(0 sil )", line)
    #words = line.split("}{")
    syllables = re.findall("\(([0-9] (?:[a-z@!\^]+ *)+)\)", line)
    #pad the phones with an extra 'sil' in the beginning
    phonlist = ["sil"] + re.findall("[a-z@!\^]+", line)
    stressed_phones = ["sil"]
    for syl in syllables:
        #find the stress for that syl, either 0,1,2 or 3
        syl_tmp = syl.split()
        stress = syl_tmp[0]
        #add the stress to every vowel, add them to the list of stressed phones
        for p in syl_tmp[1:]:
            if re.match("[aeiou@]", p): 
                stressed_phones.append(stress + p)
            else:
                stressed_phones.append(p)
    return phonlist, stressed_phones


#turn every sentence into a binary numpy array, indicating the base types present
def prepare_sentences(base_type, wishlist_ids, stress=False):
    """
    pass over the corpus and turn every sentence into a binary array of length wishlist.
    base_type: phone, diphone or triphone, type: str
    wishlist_ids: np.array containing all the base types, type: str
    corpus_size: number of (input) sentences to be used for selection
    stress: whether stress is taken into account or not
    returns: array of arrays, i.e. dataset
    """
    #initialize an empty np.array to store the sentences
    #shape is defined by the number of sentences and the length of the wishlist
    #the latter gives the dimensionality to each sentence array
    sentences = np.zeros((corpus_size, wishlist_ids.shape[0]))
    i = 0 #keep a counter, to index into the np.array above
    with open(utt_file, "r") as corpus:
        for line in corpus.readlines()[:corpus_size]:
            if line.startswith("utt"):
                phones, stressed_phones = utt_to_phonesets(line)
                
                #get the right units from the phones, depending on unit type and stress
                #stress or no stress
                phonlist = phones if stress == False else stressed_phones
                
                #unit type
                if base_type == "phones":
                    units = phonlist
                
                if base_type == "diphones":
                    units = ["{}_{}".format(phonlist[i], phonlist[i+1]) for i in\
                             range(len(phonlist)-1)]
                        
                if base_type == "triphones":
                    #add extra padding
                    pad_phones = phonlist + ["sil"]
                    units = ["{}^{}+{}".format(pad_phones[i], pad_phones[i+1],\
                             pad_phones[i+2])for i in range(len(pad_phones)-2)]
                
                #binarize them
                for unit in units: 
                    idx = np.where(wishlist_ids==unit)[0][0]
                    sentences[i][idx] = 1
            i += 1
            
    return sentences


#scoreing function: dot each sentence with the wishlist
def score_dataset(dataset, wishlist):
    """
    takes in a binarized data set array of sentences, where every sentence is an array).
    returns the index of the highest scoring sentence. in case of tie, the first
    sentence in the list is selected.
    """
    global selected_zeros
    scores = []
    for sentence in dataset:
        #do the dot product; append to scores
        scores.append(np.dot(sentence, wishlist))
    i=0 #use the first match in case of tie; iterate to avoid duplication in case
    #they all drop to 0
    while True:
        best_sentence_id = np.where(scores==np.max(scores))[0][i]
        if best_sentence_id in selected_sentence_ids:
            i+=1 #go to the next sentence
        else:
            if np.max(scores) == 0:
                selected_zeros +=1
            selected_sentence_ids.add(best_sentence_id)
            return best_sentence_id


#main algorithm
def text_selection(base_type, stress=False, scoring_type=1):
    """
    greedy selection of highest-scoring sentences, according to a wishlist.
    wishlist is a numpy array of either all 1s or weights/probabilities (for each
    base type). num_sentences is the number to be selected. writes the selected
    sentences to a file and returns the distribtuion of base types in the selected 
    corpus (for plotting).
    base type: "phones", "diphones", "triphones"
    stress: consider stress or not
    scoring_type: 1 for vanilla, scoring each unit equally, 2 for weighted scores
    num_sentences: the number of sentences selected
    """
    #load the wishlist and unit ids
    name_extension = "_stress" if stress == True else ""
    name = base_type + name_extension
    wishlist = np.load("{}_wishlist{}.npy".format(name, scoring_type))
    ids = np.load("{}_ids.npy".format(name))

    #load the data set
    dataset = prepare_sentences(base_type, ids, stress=stress)
    
    #distribution = np.zeros(wishlist.shape)
    for it in range(num_sentences): #select as many sentences as specified
        best_sentence_id = score_dataset(dataset, wishlist)
        #print(best_sentence_id)
        #select the sentence from the original dataset and write to a file
        with open(text_file, "r") as text:
            outstring = text.readlines()[best_sentence_id]
        with open(out_file, "a") as output:
            output.write(outstring)
        with open(utt_file, "r") as text:
            outstring = text.readlines()[best_sentence_id]
        with open(utts_out, "a") as output:
            output.write(outstring)
        best_sentence_arr = dataset[best_sentence_id]
        #delete the selected sentence from the wishlist    
        wishlist[np.where(best_sentence_arr != 0)] = 0
        #add the new sentence to the distribution
        #distribution = distribution + best_sentence_arr
        
    #return distribution


#plot the resulting distributions
def plot_dist(dist_array, name, plotname):
    f = plt.figure()
    plt.bar(range(dist_array.shape[0]), dist_array.sort_values(ascending=False))
    plt.xlabel("Rank", size=17)
    plt.ylabel("Frequency", size=17)
    plt.title("Distribution of {}".format(plotname), size=20)
    plt.xticks(size=15)
    plt.yticks(size=15)
    f.savefig("{}.pdf".format(name), format="pdf")



########
# MAIN #
########


def main():
    #baseline: randomly sample 5XX sentences, measure coverage
    #call text_selection for different base types/wishlists
    #wishlist1 gives equal weight to all new base units
    text_selection(base_unit, stress=stress, scoring_type=scoring_type)

    #measure the resulting coverage of phones/diphones/triphones

if __name__ == "__main__":
    main()
    print(selected_zeros)