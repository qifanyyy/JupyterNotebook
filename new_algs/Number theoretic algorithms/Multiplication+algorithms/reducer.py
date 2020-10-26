#!/usr/bin/python
import sys
row_of_M = 3
col_of_M = 3
row_of_N = 3
col_of_N = 1
for lines in sys.stdin:
	data = lines.strip().split('\t')
	#print data[0]
	t = data[1]
	strs = t.replace('[','').split('],')
	lists = [map(str, s.replace(']','').split(',')) for s in strs]
	val=0;
	l1=[]
	l2=[]
	for asf in lists:		
		if(asf[0]=="'M'" or asf[0]==" 'M'"):
			l1.append(asf[2])
		else:
			l2.append(asf[2])
	for i in range (0,len(l1)):
		val=val+int(l1[i])*int(l2[i])
	print data[0],val	
