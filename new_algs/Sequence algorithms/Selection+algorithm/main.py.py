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
import multiprocessing as mp
import time

##import my files
import prepare_data
import filter_part
import wrapper_part
import utils
import sys
from myClasses import ML_set
from myClasses import data_instance


dt_subset = [109, 136, 149, 188, 1023, 2134, 3039, 3238, 3290, 3293, 3359, 3800, 3977, 4348, 4670, 5806, 5985]
#n_proc = 16


def main():
    if __name__ == '__main__':
        start_t = time.time()
        
        print "Using ", n_proc, " processes"
        ##read data from file
        #data = prepare_data.import_data()
        ##detects and removes outliers on data
        
        #print "Took ", time.time() - start_t, " to read from obj file ", len(data)
        
        #start_t = time.time()
        data = prepare_data.import_data_csv("dataset.csv", "metadata.csv")
        
        #print "Took ", time.time() - start_t, " to read from csv files ", len(data)
        
        
        #quit()
        data = prepare_data.remove_and_correct_outliers(data)
        ##normalize data
        data = prepare_data.normalize_data_range(data)
        
        ##at this point all that is prepared
    
        ##filter the irrelevant features
        features = filter_part.filter_features(data)
        
        #just to test a smaller number of features
        fts = []
        for i in range(0,20):
            fts.append(features[i])
            
        
        
        ##call the wrapper part
        wrapper_part.wrapper(n_proc, data, fts)#features)#fts)
        
        print "program took: ", time.time() - start_t
        
    
    
    ##perform the wrapper part to find the best subset
    
    #    wrapper_part.test()
    #wrapper_part.wrapper(data, features)
    

n_proc = int(sys.argv[1])
    
main()