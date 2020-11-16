import os
import logging
from SimilarityScaledPosRec import *
from EDM_Dev_Analysis import *
from DimensionReduction import *
from Preprocessing_Patterns import *
import numpy as np
import pandas as pd
from time import time,strftime,gmtime
import matplotlib.pyplot as plt

# key_type =

# df_name =

layer_start = -18
layer_end = -19


start = time()
start_time = strftime("%m_%d_%H:%M:%S", gmtime())
load_time = start_time

# Load hdf5 and pull list of Events ##############
events_tree = pd.read_hdf(df_name, key=key_type)
dir_path = os.getcwd()
plot_path = dir_path+'/EDM_Support/'#+start_time+'/'
if not os.path.exists(plot_path+start_time+'/'):
    os.mkdir(plot_path+start_time+'/')
LOG_FILENAME = plot_path+start_time+'/'+'LogFile.log'
logging.basicConfig(filename=LOG_FILENAME, level =logging.INFO)
logging.warning('Abandon All Hope. There is no joy to be had here.')
logging.info('Initial Dataframe: '+df_name)
logging.info('Start Time: '+start_time)
logging.info('Layer Selection: '+str(layer_start)+' ->'+str(layer_end))
# Data Selection

events_tree = events_tree.loc[lambda df: df.int_a_z_3d_nn < layer_start, :]
events_tree = events_tree.loc[lambda df: df.int_a_z_3d_nn > layer_end, :]
print(len(events_tree))

events_tree = events_tree.loc[lambda df: df.s2_a > 8000, :]
events_tree = events_tree.loc[lambda df: df.s2_a < 30000, :]

# Preprocessing to reconstruct dead PMTS - Only necessary if you are using a raw dataframe and want to fill the dead pmts
# better_pmt_array = fix_dead_pmts(dead_pmts,comp_pmts, comp_pmts_check,events_tree)
# events_tree['s2_area_array'] = better_pmt_array
# events_tree.to_hdf(plot_path+start_time+'/'+'reincarnated_pmts.h5',key='df', mode='w')



# List Formatting
event_list = events_tree['s2_area_array'].tolist()  # [['area','channel','int_a_x_3d_nn','y','z','s2_a','s2_b']]
event_x = events_tree['int_a_x_3d_nn'].tolist()
event_y = events_tree['int_a_y_3d_nn'].tolist()
Events = list(zip(event_list, event_x, event_y))
# print(len(event_list))
del events_tree, event_list, event_x, event_y
weights = np.ones([127])
# weights = weighting_calc(20)



## Create EDM ##
############################################
print ('Begining EDM Construction')
tpc = TpcRep(plot_path)
tpc.give_events(Events, 100, weights)
tpc.cut_worse_5_percent()
tpc.save_edm(time=start_time)
tpc.save_distributions()

# Apply Dimensionality Reduction. Intrinsic dimension = ~2 #
############################################################
# print('Beginning Dimensional Reduction')
manifold = Reduction(plot_path)
manifold.load_edm(time=load_time)

manifold.sklearn_mds()
# manifold.sklearn_local_linear(50)


manifold.save_edm_distribution(start_time)

# Analysis of Reconstructed Distribution #
##########################################
print('Cuts and Orienting')
posrec_analysis = MC_EDM_Comp(plot_path)
posrec_analysis.load_distributions(load_time)
posrec_analysis.corrections()
posrec_analysis.save_corrected_distribution(start_time)

print('Errors and Plotting')
posrec_analysis.get_polar_errors()
posrec_analysis.get_edm_cart()
mean_err, std_err = posrec_analysis.get_cart_error()
print(mean_err, std_err)

# Visualization #
#################


posrec_analysis.plot_edm_nn('polar')
posrec_analysis.plot_edm_nn('polar_flipped')
posrec_analysis.get_radial_dist()
posrec_analysis.plot_edm()


print('Took '+ str(((time.time()-start)/60)) + ' minutes to complete')



