#This file allow to perform a learning task from problems loaded in
#Load_Data, using the Problem class with the epm model.

import Problem
import Load_Data
import epm
import Selector
import Statistic
ALGORITHMS = ["(1+(lda_lda))","(1+1)EA","(1+10)EA1","(1+10)EA3","(1+10)FGA","(1+2)EA","1hill","2hill","RandomSearch"]
filename="../DATA_PERFORMANCES/Algorithms_Performances_compact.csv"
features_file="../DATA_PERFORMANCES/features_ordered.csv"
#number_of_features = 29 features + 1 dimension + 1 target
#
number_of_features=29
number_of_parameters=4
filter_target=[0.5,0.75,0.90,0.95]
#filter_target=[0.5,0.75]


def Main(filename,features_file,Algorithms,number_of_features,filter_target):
  print("\n---------------------------------\n")
  print("Load Data",end="")
  DATA=Load_Data.load_data(filename,ALGORITHMS,filter_target=filter_target)
  print("  [OK]\nLoad ELA Features",end="")
  P,D,F=Load_Data.load_ELA_features(features_file)
  print("  [OK]\nLink ELA Features to problems",end="")
  Problem.link_all_features(DATA,P,D,F)
  print("  [OK]\nInitialize Empirical Performance Model",end="")
  model=epm.EmpiricalPerformanceModel(number_of_parameters,number_of_features, len(ALGORITHMS),input_type="parameters",selector=Selector.Random_selector(probability=0.7))
  print("  [OK]\nFix Training and Testing sets",end="")
  model.build_training_and_testing_sets(DATA)
  print("  [OK]\nTrain EPM",end="")
  model.train_model()
  print("  [OK]\nTest EPM",end="")
  model.test_model()
  print("  [OK]\n")

  print("\nNumber of problems : "+str(len(model.get_results()))+"\n")
  SBS=Statistic.SingleBestSolver(model)
  VBS=Statistic.VirtualBestSolver(model)
  RS=Statistic.RealSolver(model)
  Merit=Statistic.Merit(SBS,VBS,RS)
  print("SBS "+str(SBS))
  print("VBS "+str(VBS))
  print("RS "+str(RS))
  print("Merit "+str(Merit))
  model.reset_model()
  model.set_input_type('features')
  model.train_model()
  model.test_model()
  SBS=Statistic.SingleBestSolver(model)
  VBS=Statistic.VirtualBestSolver(model)
  RS=Statistic.RealSolver(model)
  Merit=Statistic.Merit(SBS,VBS,RS)
  print("SBS "+str(SBS))
  print("VBS "+str(VBS))
  print("RS "+str(RS))
  print("Merit "+str(Merit))
  
Main(filename,features_file,ALGORITHMS,number_of_features,filter_target)
