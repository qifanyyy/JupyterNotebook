#!/usr/bin/python
from collections import defaultdict
import sys
row_of_M = 3
col_of_M = 3
row_of_N = 3
col_of_N = 1
ans=defaultdict(list)
for lines in sys.stdin:
	data = lines.strip().split('\t')
	if len(data)==4:
		matrix,row,col,val = data		
		if(matrix=='M' and col_of_N!=0):
			for k in range(0,col_of_N):
				key=str(row)+","+str(k)
				val2=[matrix,int(col),int(val)]
				
				ans[key].append(val2)
		elif (matrix=='N' and row_of_M!=0):
			for i in range(0,row_of_M):
				key=str(i)+","+str(col)
				val2=[matrix,int(row),int(val)]
				ans[key].append(val2)
					
for key in sorted(ans.iterkeys()):
	print str(key)+"\t"+str(ans[key])

	
	
