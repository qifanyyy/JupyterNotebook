'''
Copyright (C) <2015>  <Jorge Silva> <up201007483@alunos.dcc.fc.up.pt>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

This work was partially supported by national funds through project VOCE 
(PTDC/EEA-ELC/121018/2010), and in the scope of R&D Unit UID/EEA/50008/2013, 
funded by FCT/MEC through national funds and when applicable cofunded
by FEDER/PT2020 partnership agreement.
'''

from __future__ import division
import matplotlib
#matplotlib.use('Agg')
import numpy as np
import math

##my files
import utils


base_dir = "/home/jorge/scripts/MachineLearning/"


##returns the frequency of an array
def get_frequency(data, n_bins):
    bins = np.linspace(0,1, n_bins)  ##creates the bins to divide data
    array_data = np.array(data)  ##convert data to np array
    digitized = np.digitize(array_data, bins) ##count occurances for each binary
    freq = {}
    for i in digitized:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    return freq

##gets the probability distribution on a more efficient way than the other method
def get_probability_distribution(data):
    freq = get_frequency(data)
    for i in freq:
        freq[i] = freq[i]/len(data)
    return freq
    
def get_entropy(data):
    freqs = get_probability_distribution(data)
    entropy = 0.0
    n_classes = len(freqs.keys())
    ##print n_classes
    if n_classes <= 1:  ##if vector only has one class then it is easy predictable
        return 0.0
    for x in freqs:
        entropy -= freqs[x] * (math.log(freqs[x], n_classes))
    return entropy


##based on this website http://nlp.stanford.edu/IR-book/html/htmledition/mutual-information-1.html
def calculate_mi(data_1, data_2, bins):
    ##get the frequencies of stress and not stress data
    freq_1 = get_frequency(data_1, bins)
    freq_2 = get_frequency(data_2, bins)
    total = len(data_1) + len(data_2)
    
    mi = 0
    
    for i in freq_1:
        p = freq_1[i] / total ##get probability
        ## aux = total number of i bin on the total dataset
        aux = freq_1[i]
        if i in freq_2:
            aux += freq_2[i]
        ##calculate the part to perform the log
        log_part = (total * freq_1[i]) / (aux * len(data_1))
        
        mi += p * math.log(log_part, 2)
    
    for i in freq_2:
        p = freq_2[i] / total ##get probability
        ## aux = total number of i bin on the total dataset
        aux = freq_2[i]
        if i in freq_1:
            aux += freq_1[i]
        ##calculate the part to perform the log
        log_part = (total * freq_2[i]) / (aux * len(data_2))
        
        mi += p * math.log(log_part, 2)
        
    return mi
        
    
def filter_features(data):
    features = {}    
    useless_features = []
    bins = [50, 100, 250, 500, 1000]
    mis = [[],[],[],[],[]]
    
    for index in range(0,6125): ##iterate through all 6125 features
         
        feature_values_no_stress, feature_values_stress, min, max = utils.get_utterance_values_of_ith_utterance(data, index)
        
        if max - min == 0:
            useless_features.append(index)
        
        for i in range(0,len(bins)):
            mi = calculate_mi(feature_values_no_stress, feature_values_stress, bins[i])
            mis[i].append(mi)
            if i == 0:
                features[index] = []
            features[index].append(mi)
    
    ##thresholds for each bin
    thresholds = []
    for m in mis:
        t = np.percentile(m, 75) # return 75th percentile
        thresholds.append(t)
    
    ##create lis to check if feature was selected for each bin
    selections = [[],[],[],[],[]]
    fts = []
    hist = []
    for i in range(0,6125):
        fts.append(0)
        for j in range(0, len(bins)):
            if features[i][j] >= thresholds[j]:
                selections[j].append(1)
                fts[i] += 1
                hist.append(i)
                
            else:
                selections[j].append(0)
    
    most_selected_fts = [] ##stores the utterances that were selected in all tests
    
    ##mudar para fazer histograma pela contagem e nao pela frequencia
    hist_scatter = {}
    for i in range(0,6125): ##initiates list with all 0
        hist_scatter[i] = 0
    for i in hist:
        hist_scatter[i] += 1
    
    for i in hist_scatter:
        if hist_scatter[i] == 5:
            most_selected_fts.append(i)
    
    return most_selected_fts
    
    
        
        