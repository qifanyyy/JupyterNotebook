import sys
import os
import numpy as np
from utils import CreateOutputFile, execute_test
from algorithms.CreateMatrix import CreateTensor


def CreateAllTensors(dimensions,clusters,noises,data_path,partial_name_tensor,partial_name_target):
    '''
    Create 3D tensors and save them in txt files named '{partial_name_tensor}_{d[0]}_{d[1]}_{d[2]}_{c[0]}_{c[1]}_{c[2]}_{n}.txt' and '{partial_name_target}_{d[0]}_{d[1]}_{d[2]}_{c[0]}_{c[1]}_{c[2]}_{n}.txt'
    Parameters:
    ----------
    dimensions: list of dimensions of the 3D tensors. Ex: [(10,10,10), (20,20,5)]
    clusters: list of cluster numbers. Ex: [(5,5,5), (2,2,3)]
    noises: list of noises. Ex [.05, .1, .15]
    data_path: directory of the output files
    partial_name_tensor: Ex. 'Tensor'
    partial_name_target: Ex. 'Target'
    
    '''
        
    for d in dimensions:
            for n in noises:
                for c in clusters:
                        V,x,y,z = CreateTensor(d[0],d[1],d[2],c[0],c[1],c[2],noise=n)
                        file_V = f'{partial_name_tensor}_{d[0]}_{d[1]}_{d[2]}_{c[0]}_{c[1]}_{c[2]}_{n}.txt'
                        file_target = f'{partial_name_target}_{d[0]}_{d[1]}_{d[2]}_{c[0]}_{c[1]}_{c[2]}_{n}.txt'
                        V_file = open(data_path + file_V, 'w+')
                        V_file.write(''.join([str(x) for x in list(V.reshape(d[0]*d[1]*d[2]))]))
                        target_file = open(data_path + file_target, 'w+')
                        target_file.write(''.join([str(i) for i in list(x)]) + '\n')
                        target_file.write(''.join([str(i) for i in list(y)]) + '\n')
                        target_file.write(''.join([str(i) for i in list(z)]))
                        V_file.close()
                        target_file.close()

if __name__ == '__main__':

    '''
    Create synthetic tensors, save them and run the model n_test times on each tensor. 
    parameters:
            1. n_test: integer
            2. dimensions: list of tuples, separated by '-'. Ex: [(100,100,30)-(50,50,50)]
            3. clusters: list of tuples, separated by '-'.
            4. noise: float.
            5. algorithm: string. One of {'ALT', 'AVG', 'AGG', 'ALT2', 'AGG2'}
    '''
    
    if sys.argv[1] == '-h':
        print('''
        Create synthetic tensors, save them and run the model n_test times on each tensor. 
        parameters:
                1. n_test: integer
                2. dimensions: list of tuples, separated by '-'. Ex: [(100,100,30)-(50,50,50)]
                3. clusters: list of tuples, separated by '-'.
                4. noise: float.
                5. algorithm: string. One of {'ALT', 'AVG', 'AGG', 'ALT2', 'AGG2'}
            ''')
        quit()
    
    n_test = int(sys.argv[1])
    
    dimensions = [tuple(map(int, x.strip('()').split(','))) for x in list(sys.argv[2].strip('[]').split('-'))]
    clusters = [tuple(map(int, x.strip('()').split(','))) for x in list(sys.argv[3].strip('[]').split('-'))]
    noise = float(sys.argv[4])
    noises = [noise]
    alg = sys.argv[5]

    f, dt = CreateOutputFile("CoClust_3D", own_directory = True)
    data_path = "./output/_CoClust_3D/" + dt[:10] + "_" + dt[11:13] + "." + dt[14:16] + "." + dt[17:19] + "/"
    CreateAllTensors(dimensions,clusters,noises,data_path,"Tensor","Target")

    for i in range(n_test):
            for d in dimensions:
                    for n in noises:
                            for c in clusters:
                                    file_V = f'Tensor_{d[0]}_{d[1]}_{d[2]}_{c[0]}_{c[1]}_{c[2]}_{n}.txt'
                                    file_target = f'Target_{d[0]}_{d[1]}_{d[2]}_{c[0]}_{c[1]}_{c[2]}_{n}.txt'
                                    V_file = open(data_path + file_V, 'r+')
                                    target_file = open(data_path + file_target, 'r+')
                                    T = [int(x) for x in V_file.read()]
                                    V = np.array(T).reshape(d)
                                    t = []
                                    for line in target_file:
                                            target = [int(x) for x in line if x != '\n']
                                            t.append(np.array(target))
                                    V_file.close()
                                    target_file.close()
                                    execute_test(f,V,t[0],t[1],t[2], noise = n, algorithm = alg)
			

    f.close()
	    
		
		
		
    
    
    


