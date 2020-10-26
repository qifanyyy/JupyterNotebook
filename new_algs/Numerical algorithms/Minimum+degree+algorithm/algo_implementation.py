#===========================IMPLEMENTATION OF NAGAMOCHI-IBARAKI ALGORITHM====================

import random


def critical_edges(n, l):
    cnt = 0                                     
    for i in range(1,n):
        for j in range(0,i):
            if(adj[i][j]>0):                    
                adj[i][j]-=1                  
                localdegree = nagamochi(adj, n)
                adj[i][j]+=1                    
                if(localdegree<l):              
                    cnt+=1                     
    return cnt                                 


def get_nextnode(nag_matrix, src_list, tot):
    edge_adj = 0                                
    for i in range(tot):
        if(i in src_list):
            continue                           
        edge = 0
        for j in src_list:                     
            edge += nag_matrix[i][j]
        if (edge>=edge_adj):                    
            edge_adj= edge
            nxt_node = i
    return nxt_node                             


def get_MAOrder(nag_matrix, tot):
    choosenode = random.randint(0,tot-1)        
    ma_order = [choosenode]                     
    while(len(ma_order) <tot):                 
        ma_order.append(get_nextnode(nag_matrix,ma_order,tot)) 
    return ma_order                             

-
def get_degree(nag_matrix, n):
    return sum(nag_matrix[n])                   



def merge_node(src_mat,s,t):
    src_mat[s][t]= src_mat[t][s]= 0             
    new_len = len(src_mat)-1                    
    tgt_mat = [[0 for i in range(new_len)] for j in range(new_len)]
    p=0
    for i in range(new_len+1):
        q=0
        flag=0
        for j in range(0,i+1):
            if(i==max(s,t)):                   
                flag=1
                break
            if(i==min(s,t)):                    
                tgt_mat[p][q] = tgt_mat[q][p] = src_mat[min(s,t)][j]+src_mat[max(s,t)][j]
            else:                               
                if(j!=s and j!=t):
                    tgt_mat[p][q] = tgt_mat[q][p] = src_mat[i][j]
                else:
                    if(j==max(s,t)):
                        continue
                    tgt_mat[p][q] = tgt_mat[q][p] = src_mat[i][s]+src_mat[i][t]
            if(p==q):
                tgt_mat[p][q]=0
            q+=1
        if(flag==0):
            p+=1    
    return tgt_mat
                

def nagamochi(nag_matrix, tot):
    if(tot==2):                                
        return get_degree(nag_matrix,0)      
    ma_order = get_MAOrder(nag_matrix,tot)      
    last_ind = len(ma_order)-1                 
    lambda_g = get_degree(nag_matrix,ma_order[last_ind])
    nag_matrix=merge_node(nag_matrix,ma_order[last_ind],ma_order[last_ind-1]) 
    return (min(lambda_g,nagamochi(nag_matrix, tot-1))) 

def genearate_graph(n, maxedges):
    global adj
    cnt = 0                                     
    while(cnt<maxedges):                        
        for i in range(n):                      
            for j in range(n):
                if (i == j):                    
                    adj[i][j] = adj[j][i] = 0
                else:
                    x = random.randint(0,1)    
                    if (x == 1):                
                        adj[i][j] = adj[j][i] = adj[i][j]+1
                        cnt+=x                  
                        if (cnt >= maxedges):  
                            break
            if (cnt >= maxedges):
                break

n=22                                            
print("No. OF EDGES\tDEGREE\tLAMBDA\tCRITICAL EDGES")
print("============\t======\t======\t==============")
for m in range(40,405,5):                       
    adj=cpy=[[0 for i in range(n)] for j in range(n)]
    di = 2*m/n                                  
    generate_graph(n,m)                         
    l = nagamochi(adj, n)                       
    criticaledges = critical_edges(n,l)                 
    print(str(m)+"\t\t"+str(di)+"\t"+str(l)+"\t"+str(criticaledges)) 
