if __name__ == "__main__":
    
    N_str = np.empty(0,dtype=float)
    N_fin = np.empty(0,dtype=float)
    Dur = np.empty(0,dtype=float)
    with open('Edges','r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            N_str = np.concatenate((N_str,[int(row[0])]))
            N_fin = np.concatenate((N_fin,[int(row[1])]))
            Dur = np.concatenate((Dur,[float(row[2])]))
    file.close()
    # import the data from the "Edges" file.

    wei = calcWei(N_str,N_fin,Dur)
    # compute the initial weight matrix for the directed graph
    ist = 26 
    isp = 27 
    # define the indices of the virtual start and finish node
    
    C1 = []
    dic = {}
    for i in range(13):
        col = wei[:,i]
        row = wei[i+13,:]
        c1 = 0
        c3 = []
        for j in range(28):
            if row[j] != 0:
                c1 += 1
                c3.append(j)
            else:
                pass
        c3 = c3[:-1]
        if c1 > 2:
            C1.append(i)
            dic[i] = c3
        else:
            pass
    
    lp = BellmanFord(ist,isp,-wei)
    # using B-F algorithm to compute the longest path from the virtual start node
    # to the virtual finish node
    lp_new=lp[1:-1]
    # get the path free of the virtual start and finish node
    L = len(lp_new)-1
    time = 0
    for i in range(0,L,2):
        # calculating the duration of the longest path
        p=N_str==lp_new[i]
        q=N_fin==lp_new[i+1]
        time += int(Dur[p&q])
    
    # Initialisations
    V = []   # the list of visited nodes, updated after each loop below      
    P = []   # the list of the paths computed below
    tp = []  
    # the list of the durations of the iterated longest paths computed below
    while len(V)!=13:
        # the iteration terminates after we have visited all nodes
        T = np.zeros(13,dtype=int)
        # list of the durations of all paths computed
        for i in range(13):
            # compute the paths from every unvisted start nodes then compute
            # their durations and store them in the list T
            if i in V:
                pass
            else:
                path = BellmanFord(i,isp,-wei)
                l = len(path)-1
                t = 0
                for j in range(0,l,2):
                    p=N_str==path[j]
                    q=N_fin==path[j+1]
                    # obtaining the job executed in the path, p and q are the 
                    # corresponding start and finish node of the job
                    t += Dur[p&q]
                    # adding the duration of the job to the duration of the path
            T[i] = t
        
        m=T.argmax()
        # obtain the index of the longest path in this iteration
        tp.append(T[m])
        # add the duration of the longest path in this iteration to the list tp
        path2=BellmanFord(m,isp,-wei)
        P.append(path2)
        # add the longest path in this iteration to the list P

	for k in range(0,len(path2)-1,2):
	    # update the weight matrix by setting the weights of the edges from
	    # the start nodes to the finish nodes of the jobs in the longest path
	    # in this iteration and adding the start nodes of the jobs in the 
	    # longest path in this iteration to the list of visited nodes, V
	    wei[int(path2[k]), int(path2[k+1])] = 0
	    V.append(path2[k])
    
    P = [P[i][:-1] for i in range(len(P))]
    P_new = [np.zeros((1, 6))]
    # the new P list consist of the sequence of the jobs
    for i in range(len(P)):
        p1 = P[i]
        l = int(len(p1)/2)
        p2 = []
        if l != 0:
            for j in range(l):
                p2 += [p1[2*j]]
        else:
            p2 = [p1[0]]
        P_new.append(p2)
    P_new = P_new[1:]
    
    dur = [41,51,50,36,38,45,21,32,32,49,30,19,26]
    # list of durations of the jobs
    IS = np.zeros(13,dtype=int)
    for i in range(len(C1)):
        c = C1[i]
        # the list of nodes need to be processed before multiple other jobs
        d =dic[c] 
        # compute a dictionary of the information of the nodes with multiple
        # dependencies
        for j in range(len(P_new)):
            p = P_new[j]
            if c in p:
                ind = p.index(c)
                d.remove(p[ind+1])
    for c in C1:
        if c != 1:
            # solve the issue for the case when the job with multiple dependency is 
            # job 1
            d = dic[c]
            for i in range(len(d)):
                IS[d[i]] += dur[c]
        else:
            # add the duration of job 0
            IS[12] = 41 + dur[c]
            
        
    P_new[4] = P_new[5]+P_new[4]
    P_new = P_new[:-1]
    P[4]= P[5]+P[4]
    P = P[:-1]
    tp[4] += tp[5]
    tp = tp[:-1]
    
    S = np.zeros(13,dtype=int)
    for p in P_new:
        S[p[0]] = 0
        if len(p) == 2:
            S[p[1]] = dur[p[0]]
        elif len(p) == 3:
            S[p[1]] = dur[p[0]]
            S[p[2]] = S[p[1]] + dur[p[1]]
        else:
            pass

            
    SS = [max(S[i],IS[i]) for i in range(13)]
    SS[11] += 21 # special case job 11
    # compute the final optimal start times list
    F = np.zeros(13, dtype=int)
    F = [SS[i] + dur[i] for i in range(13)]
    # compute the optimal finish times list
        
    # report the outcome
    print 'The longest path through this graph from the virtual start node to the virtual finish node is',lp,'with duration',time
    print 'The list of the longest path and the remaining shorted paths:'
    for i in range(len(P)):
        print 'The path',[ist]+P[i],'where expressed in the form of strings of jobs is:', P_new[i]
    print 'The number of processes in parallel is',len(tp)
    for i in range(13):
        print 'The optimal startand finish time for job',i,'are',SS[i],'and',F[i],'respectively.'
