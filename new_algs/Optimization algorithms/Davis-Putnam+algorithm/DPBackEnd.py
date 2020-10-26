

def back_out(solution,atoms,val_stop,assign_stop,k):

	sol_val = []
	sol_assg = []
	for i in range(0,len(solution)):
		if solution[i] > 0:
			if i<val_stop:
				sol_val.append(atoms[i])
			else :
				sol_assg.append(atoms[i])

	out_string = ''
	i=0
	j=0	
	#print()
	#print(sol_assg)
	#print(sol_val)
	sol_val.pop(0)
	for t in range(0,k):
		out_string += ('\nT='+str(t)+'\n')
		while i < len(sol_val) and sol_val[i][2] == t:
			out_string += ('Value('+str(sol_val[i][0])+','+str(sol_val[i][1]) + ','+str(t)+') ')
			#print ('Value( '+str(sol_val[i][0])+', '+str(sol_val[i][1]) + ', '+str(t))
			i+=1
		out_string +=('\n')
		while j < len(sol_assg) and sol_assg[j][2] == t:
			out_string += ('Assign('+str(sol_assg[j][0])+',' +str(sol_assg[j][1])+','+str(t) + ') ')
			#print (' Assign( '+str(sol_assg[i][0])+', ' +str(sol_assg[i][1])+', '+str(t))
			j+=1
	out_string+= '\nT=' +str(k) + '\n'
	while i < len(sol_val):
		out_string += ('Value('+str(sol_val[i][0])+','+str(sol_val[i][1]) + ','+str(t) +') ')
		#print ('Value( '+str(sol_val[i][0])+', '+str(sol_val[i][1]) + ', '+str(t))
		i+=1

	text_file = open('DPSolution.txt',"w")
	text_file.write(out_string)
	text_file.close()
