#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import generate_HMM_model as ghm
import random
def CALCULATE_INIT_DETECTOR_SET(normal_set,r_self,r_ab,e_max,init_iter):
	print('CALCULATE_INIT_DETECTOR_SET')
	dim=normal_set.shape
	num_hits=0
	m=0
	e=float("inf") 
	unit_v=np.sum(np.eye(dim[0]),axis=1)
	unit_v.shape=(dim[0],1)
	print(dim[0])
	mat=normal_set
	volum_s=0
	while (m<=init_iter)|(e>=e_max):
		m+=1
		x=np.random.rand(1,dim[1])#random vector
		min_dis=np.min(np.sqrt(np.sum(((np.dot(unit_v,x)-normal_set)**2),axis=1)))#min distance with elem in normal set
		print(min_dis)
		if min_dis<=r_self:
			num_hits+=1
		volum_s=num_hits/m
		e=(((volum_s-np.sqrt(volum_s))/m)**(1/3))
	print('%s          %s        %s'%(volum_s,dim[1],r_ab))
	num_ab=int((1-volum_s)/(2*r_ab/(dim[1]**(1/2))**dim[1]))#number of detector
	print('Abnorm sample number is %s'%num_ab)
	D_set=[]
	for i in range(0,num_ab):
		x=np.random.rand(1,dim[1])#random vector
		min_dis=np.min(np.sqrt(np.sum(((np.dot(unit_v,x)-normal_set)**2),axis=1)))#min distance with elem in normal set
		while min_dis<r_self:
			x=np.random.rand(1,dim[1])#random vector
			min_dis=np.min(np.sqrt(np.sum(((np.dot(unit_v,x)-normal_set)**2),axis=1)))#min distance with elem in normal set
		D_set.append(x.tolist()[0])
	print('All %s abnorm sample init well!'%num_ab)
	return D_set
def OPTIMIZE_DETECTOR_DISTRIBUTION(D_set,r_ab,normal_set,r_self,num_iter,theta_min,alpha,alpha_pert,beta):
	r_pert=2*r_ab
	num_ab=len(D_set)
	T=CALCULATE_INIT_T(D_set,r_ab,normal_set,r_self,r_pert,beta)
	for i in range(0,num_iter):
		receive_num=0
		steps=0
		random_receive=0
		while (receive_num<num_ab*theta_min)&(steps<=2*num_ab*theta_min):
			index=int(random.random()*num_ab)
			x=np.random.rand(1,len(D_set[0]))
			while distance_two_vector(x,D_set[index])>r_pert:
				x=np.random.rand(1,len(D_set[0]))
				deta_c=CALCULATE_COST_DIFFERENCE(D_set,index,x,r_ab,normal_set,r_self,beta)
				# print('deta_c   is %s'%deta_c)
				if deta_c<0:
					receive_num+=1
					D_set[index]=x
					print('receive_num   %s'%receive_num)
				elif np.exp((-1*deta_c)/T)>random.random():
					receive_num+=1
					random_receive+=1
					D_set[index]=x
					print('receive_num   %s'%receive_num)			
		print('num_iter     %s'%i)
		print('random_receive   %s'%random_receive)
		print('receive_num  %s'%receive_num)
		T=alpha*T
		r_pert=alpha_pert*r_pert
	return D_set

def distance_two_vector(array1,array2):
	return np.sqrt(np.sum((array1-array2)**2))

def CALCULATE_INIT_T(D_set,r_ab,normal_set,r_self,r_pert,beta):
	over_lapping=0
	self_covering=0
	for i in range(0,D_set.shape[0]-1):
		over_lapping+=Overlapping_v_D(D_set[i],D_set[i+1:],r_ab)
	print('overlapping is %s'%over_lapping)
	for i in D_set:
		self_covering+=selfcovering(i,normal_set,r_ab,r_self)
	print('selfcovering is %s'%self_covering)
	return over_lapping+beta*self_covering

def CALCULATE_COST_DIFFERENCE(D_set,index,d,r_ab,normal_set,r_self,beta):
	pre_value=Overlapping_v_D(D_set[index],D_set,r_ab)+beta*selfcovering(D_set[index],normal_set,r_ab,r_self)
	cur_value=Overlapping_v_D(d,D_set,r_ab)+beta*selfcovering(d,normal_set,r_ab,r_self)
	return cur_value-pre_value
def Overlapping_v_D(v,D_set,r_ab):
	dim=D_set.shape
	unit_v=np.sum(np.eye(dim[0]),axis=1)
	unit_v.shape=(dim[0],1)
	v.shape=(1,dim[1])
	return sum(np.exp(np.sum((-1*(np.dot(unit_v,v)-D_set)**2),axis=1)/(r_ab**2)))
def selfcovering(v,normal_set,r_ab,r_self):
	dim=normal_set.shape
	unit_v=np.sum(np.eye(dim[0]),axis=1)
	unit_v.shape=(dim[0],1)
	v.shape=(1,dim[1])
	return sum(np.exp(np.sum((-1*(np.dot(unit_v,v)-normal_set)**2),axis=1)/(((r_ab+r_self)/2)**2)))

if __name__ == '__main__':
	_set=pd.read_csv('likelihood_vector/normal_set.csv',header=None)
	# ghm.random_generate_vector(800,10)
	# D_set=CALCULATE_INIT_DETECTOR_SET(_set,r_self=0.6,r_ab=0.5,e_max=0.1,init_iter=20)
	# print('save all %s abnorm detector'%len(D_set))
	# for d in D_set:
	# 	ghm.save_abnormal_sample_likeli(d)
	D_set=pd.read_csv('likelihood_vector/abnormal_set.csv',header=None)
	# T=CALCULATE_INIT_T(np.array(D_set),0.8,_set,0.6,1.6,2)
	D_set=OPTIMIZE_DETECTOR_DISTRIBUTION(np.array(D_set),0.5,_set,0.6,10,0.05,0.7,0.8,20)
	# print('T is  %s'  %T )
	print('save all %s OPTIMIZED abnorm detector'%len(D_set))
	for d in D_set:
		ghm.save_abnormal_sample_likeli(d,'OPTIMIZED_abnormal.csv')
