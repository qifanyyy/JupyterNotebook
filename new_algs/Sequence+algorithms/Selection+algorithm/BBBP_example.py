# -*- coding: utf-8 -*-
"""
Created on Tue May 26 18:35:38 2020

@author: Murat Cihan Sorkun

Feature Selection be Genetic Algorithm: An example on BBBP dataset 
"""

from sklearn.model_selection import train_test_split
from sklearn import linear_model
import genetic
from rdkit import Chem
import pandas as pd
import mordred
from mordred import Calculator, descriptors


def get_mordred_descriptors(smiles_list):
       
    calc = mordred.Calculator()  
        
    calc.register(mordred.AtomCount)        #16
    calc.register(mordred.RingCount)        #139
    calc.register(mordred.BondCount)        #9   
    calc.register(mordred.HydrogenBond)     #2  
    calc.register(mordred.CarbonTypes)      #10
    calc.register(mordred.SLogP)            #2
    calc.register(mordred.Constitutional)   #16    
    calc.register(mordred.TopoPSA)          #2
    calc.register(mordred.Weight)           #2
    calc.register(mordred.Polarizability)   #2
    calc.register(mordred.McGowanVolume)    #1
    
    name_list=[]
    for desc_name in calc.descriptors:
        name_list.append(str(desc_name))
        
    descriptors_list=[]    
    for smiles in smiles_list:
        # print(smiles)
        mol=Chem.MolFromSmiles(smiles)
        mol=Chem.AddHs(mol)
        calculated_descriptors = calc(mol)
        descriptors_list.append(calculated_descriptors._values)      
    
    descriptors_df=pd.DataFrame(descriptors_list,columns=name_list)
    descriptors_df = descriptors_df.select_dtypes(exclude=['object'])        
        
    return descriptors_df

    
data_name =  "BBBP"  
data_df = pd.read_csv("data/"+data_name+".csv")

print("\nGenerating features from SMILES...")
descriptors_data=get_mordred_descriptors(data_df["smiles"].values)

X_train, X_test, y_train, y_test = train_test_split(descriptors_data.values, data_df["p_np"].values, train_size=0.75, test_size=0.25, random_state=0)

population_size=20
num_of_generations=50
mut_ratio=0.5

#select features from genetic algorithm
selected_features=genetic.select_features(X_train,y_train,population_size,num_of_generations,mut_ratio,"clf",verbose=1)

X_train_selected=genetic.transform_data(X_train,selected_features)
X_test_selected=genetic.transform_data(X_test,selected_features)

print("\nTotal generated features:",descriptors_data.shape[1])
print("\nTotal selected features from genetic algorithm:",X_train_selected.shape[1])

print("\nTraining models by logistic regression..")
model= linear_model.LogisticRegression(solver="liblinear", multi_class="ovr")   

model.fit(X_train, y_train)
default_score=model.score(X_test, y_test)
print("\nTest score(accuarcy) without feature selection:",default_score)

model.fit(X_train_selected, y_train)
genetic_score=model.score(X_test_selected, y_test)
print("Test score(accuarcy) with genetic selection:",genetic_score)



