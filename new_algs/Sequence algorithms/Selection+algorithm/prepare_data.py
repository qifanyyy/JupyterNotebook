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
from sklearn.preprocessing import Imputer
import numpy as np
np.set_printoptions(threshold='nan')
import pickle
import os

##import my files
#import machine_learning_db as myDB
import utils
from myClasses import ML_set
from myClasses import data_instance


##myDB function was removed...



##imports data either from a file with a python object or from the database in case the file doesnt exist        
def import_data():
    file = "save_obj.txt"
    if os.path.isfile(file):  ##if the file exists import from file
        print "importing data from file..."
       	with open(file, "rb") as myFile:
            total_set = pickle.load(myFile)
    else: ##we havee to create the file again
        print "creating load file data... (need to test this approach...)"
        total_set = []
        ids = myDB.getIds()
        for id in ids:
            if id not in ids_new_tag:
                continue
            print id
            info = myDB.getStressedUts(id, 1, "Stress_based_on_hf_10sec_window") ##returns event, starttime for each utterance
            for i in info:
                ut = myDB.getUtterancesFeatures(i[0], id, int(i[1])) ##receives event, id, starttime and returns 6125 values for that utterance
                if ut == []:  ##if there is no utterace features proceed to next one
                    continue
                f = data_instance(id, i[0], int(i[1]), 0, ut, 1)  ##0 is for the duration im not reading it from the db   
                total_set.append(f)
            info = myDB.getStressedUts(id, 0, "Stress_based_on_hf_10sec_window") ##returns event, starttime for each utterance
            for i in info:
                ut = myDB.getUtterancesFeatures(i[0], id, int(i[1])) ##receives event, id, starttime and returns 6125 values for that utterance
                if ut == []:  ##if there is no utterace features proceed to next one
                    continue
                f = data_instance(id, i[0], int(i[1]), 0, ut, 0)    
                total_set.append(f)
        #for i in total_set:
        #    print i.id, " ", i.start_time, " ", i.stress
        with open(file, "wb") as myFile:
            pickle.dump(total_set, myFile)
    #for i in data["stress"]:
     #   print i
    #print "________________________________________________"    
    #for i in data["no_stress"]:
    #    print i
    return total_set


##importa o dataset de ua file csv com as features ea ultima coluna a classificacao, se tiver uma info fileo tenta ler a info de outro ficheiro
def import_data_csv(data_file, info_file):
    total_set = []
    f_data = open(data_file, "r") ##ler file
    data = f_data.readlines()
    if info_file != "": ##abrir file de info se necessario
        f_info = open(info_file, "r")
        info = f_info.readlines()
    for i in range(0,len(data)):
        line = data[i].split(", ")
        ft_values = []
        for j in range(0, len(line)-1): ##read the values for the line, the last collumn represents the class 
            ft_values.append(float(line[j]))
        line_class = int(line[len(line)-1])
        id = 0
        event = ""
        startTime = 0
        duration = 0
        if info_file != "": ##if we have an info file lets update the fields
            line_info = info[i+1].split(", ") ##info file starts with the headers... must add +1
            id = int(line_info[0])
            event = line_info[1]
            startTime = int(line_info[2])
            duration = int(line_info[3])
        instance = data_instance(id, event, startTime, duration, ft_values, line_class) ##now that we have all info lets save the info
        total_set.append(instance)
    return total_set 




##normalize all data set with deviation and median
def normalize_data_mean(data):
    for i in range(0, len(data[0].values)): ##for all features
        values = []
        total = 0
        for inst in data:  ##iterate through all instances
            values.append(inst.values[i])
            total += inst.values[i]
        mean = total / len(values) ## mean
        total_dif = 0
        for v in values: ##calculate diferences for deviation
            dif = v - mean
            dif = dif ** 2
            total_dif += dif
        deviation = total_dif / len(values)
        ##now that we have mean and deviation we should update data values
        for inst in data:  
            #subtract mean and divide by deviation
            val = inst.values[i]
            val = val - mean
            val = val / deviation
            inst.values[i] = val
    return data

##normalize all data withint 0 and 1 range
def normalize_data_range(data): 
    for i in range(0, len(data[0].values)): ##for all features
        values = []
        for inst in data:  ##iterate through all instances
            values.append(inst.values[i])
        #print values
        min_x = min(values)
        max_x = max(values)
        diff = max_x - min_x
        if diff == 0:
            diff = max_x
            if max_x == 0:
                diff = 1
        #print i, " ", min_x, " ", max_x, " ", diff
        for inst in data:  
            val = inst.values[i]
            val = (val - min_x) / (diff)
            inst.values[i] = round(val,6)
    return data
    
## detects outliers and corrects them using sklearn
def remove_and_correct_outliers(data):
    ##is data in a normal distribution??
    b_constant = 1.4826  ##constant used for normal distribution
    factor = 10 #3 ##factor to multiply for the range
    for i in range(0, len(data[0].values)):  ##iterate through all features, in voce case 6125
        d_s, d_ns, _, _ = utils.get_utterance_values_of_ith_utterance(data, i)  ##get all feature values
        d = d_s + d_ns ##join them together, since the fucntion returns different arrays for stress or not stress
        f_vals = np.array(d, dtype=float) ##transform list into np array
        median = np.median(f_vals) ##get the median
        diff = (f_vals - median)**2 ##subtract median to every element and **2 to get all values to positive
        diff = np.sqrt(diff) ## eliminate the **2 trick to avoid negatives
        med_abs_deviation = np.median(diff) ##get the new mean
        threshold = med_abs_deviation * b_constant ##raange of value to be accepted
        max_range = median + threshold * factor
        min_range = median - threshold * factor
        for j in range(0, len(f_vals)):  ##mark values that are outside the bounderies as outliers
            if f_vals[j] < min_range or f_vals[j] > max_range:
                f_vals[j] = np.nan
        imp = Imputer(missing_values=np.nan, strategy='mean', axis=1)
        f_vals = imp.fit_transform(f_vals)[0]
        for j in range(0, len(f_vals)):
            data[j].values[i] = round(f_vals[j],6)
    return data
    
    
    