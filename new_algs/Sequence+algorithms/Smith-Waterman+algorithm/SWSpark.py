# python --version 2.7.12
from pyspark import SparkContext
from Bio.SubsMat import MatrixInfo
import time
import SW_align
import numpy as np
import time
def alignment(dbs,query,sub_mat, gap_o=5, gap_e=1):
    '''
    dbs :[sequence_name,sequence];
    gap_o: gap opening
    gap_e: gap extension
    '''
    db = dbs[1]

    m = len(db)
    n = len(query)
    score_matrix = np.zeros(shape=(m+1,n+1))
    # fill in the M_{i,j},here M is the score matrix
    for i in range(1,m+1):
        for j in range(1,n+1):
            temp_score = [0]
            I_list = [score_matrix[i][j-ele]-(gap_o+(ele-1)*gap_e) for ele in range(1,j)]
            J_list = [score_matrix[i-ele][j]-(gap_o+(ele-1)*gap_e) for ele in range(1,i)]
            if len(I_list)>0:
                temp_score.append(max(I_list))
            if len(J_list)>0:
                temp_score.append(max(J_list))
            if (db[i-1],query[j-1]) in sub_mat:
                temp_score.append(score_matrix[i-1,j-1]+sub_mat[(db[i-1],query[j-1])])
            else:
                temp_score.append(score_matrix[i-1,j-1]+sub_mat[(query[j-1],db[i-1])])
            score_matrix[i,j] = max(temp_score)
    #find the max element in the score matrix
    max_dict = {}
    max_temp = 0
    for i in range(score_matrix.shape[0]):
        for j in range(score_matrix.shape[1]):
            if score_matrix[(i,j)]<max_temp:
                pass
            else:
                max_temp = score_matrix[(i,j)]
                max_dict[(i,j)] = max_temp
    M = max(max_dict.values())
    max_dict_update = {}# {(1,2):4} i.e.{coordinates:value}
    for ele in max_dict:
        if max_dict[ele] == M:
            max_dict_update[ele]=M
    #Traceback:define the traceback function
    def traceback(index,traceback_list):
        'recursive trace back'
        indexes = dict(
        left = (index[0]-1,index[1]),
        up  = (index[0],index[1]-1),
        left_up  = (index[0]-1,index[1]-1)
        )
        values = {}
        for ele in indexes:
            values[ele]=(score_matrix[indexes[ele]])
        max_key = max(values,key=values.get)
        #max_value = max(values.values())
        if score_matrix[indexes['left_up']] > 0:
            traceback_list.append(indexes[max_key])
            traceback(indexes[max_key],traceback_list)
    # running the trace back function
    traceback_result = {}  # {source_index:[indexes]}
    for ele in max_dict_update:
        traceback_result[ele] = [ele]
        traceback(ele,traceback_result[ele])
        traceback_result[ele] = list(reversed(traceback_result[ele]))
     # obtain aligned sequences
    seq1_index = []
    seq2_index = []
    for ele in traceback_result:
        for elem in traceback_result[ele]:
            if elem[0]>0:
                seq1_index.append(elem[0]-1)
            else:
                seq1_index.append(elem[0])
            if elem[1]>0:
                seq2_index.append(elem[1]-1)
            else:
                seq2_index.append(elem[1])
    aligned_seq1 = ''
    last_num = ''
    for num in seq1_index:
        if num == last_num:
            aligned_seq1+='-'
        else:
            aligned_seq1+=db[num]
        last_num = num
    aligned_seq2 = ''
    last_num = ''
    for num in seq2_index:
        if num == last_num:
            aligned_seq2+='-'
        else:
            aligned_seq2+=query[num]
        last_num = num
    return dbs[0],M,aligned_seq1,aligned_seq2 # M the max element in score Matrix
    
'''
if __name__ == "__main__":
    start_time = time.time()
    dbfile = open('db.file')
    DB = []
    lines = dbfile.readlines()
    for line in lines:
        line = line.split(',')
        line[1] = line[1][:-1]
        DB.append(line)
    queryfile = open('query.file')
    query = queryfile.readline()
    sub_mat = MatrixInfo.blosum50
    sequences_result = []
    for dbs in DB:
        single_seq = alignment(dbs,query,sub_mat)
        sequences_result.append(single_seq)
    write_to = open('single_machine.txt','w')
    sequences_result = sorted(sequences_result,key=lambda x:x[1],reverse=True)
    top_k = sequences_result[0:7]
    for ele in top_k:
        write_to.write(str(ele)+'\n')
    used_time = time.time()-start_time
    write_to.write('single_machine used: '+str(int(used_time))+'seconds')
'''
'''
test for sw example
if __name__ == "__main__":
    seq1 = ['testseq','GGTTGACTA']
    seq2 = 'TGTTACGG'
    print('primary sequences:')
    print((seq1,seq2))
    bases = ["A","T","C","G"]
    sub_mat = {}
    for i in range(len(bases)):
        for j in range(i,len(bases)):
            if i==j:
                sub_mat[(bases[i],bases[j])] =3
            else:
                sub_mat[(bases[i],bases[j])] =-3
    result = alignment(seq1,seq2,sub_mat,gap_o=1)
    print(result)
'''
start_time = time.time()
sc =SparkContext()
# substitute matrix blosum50
sub_mat = MatrixInfo.blosum50
#sub_mat = sc.broadcast(sub_mat)
# read files and 
db = sc.textFile('db.file')
db =db.map(lambda x: x.split(','))
#print(db.take(20))
query = sc.textFile('query.file')
query = query.collect()[0]
#query = sc.broadcast(query)
aligned = db.map(lambda x:alignment(dbs=x,query=query,sub_mat=sub_mat))
aligned = aligned.sortBy(lambda x:x[1],ascending=False)
#element in this rdd looks like:(seq_name,max_score,aligned_db,aligned_query)
#ks = [3,5,7]
#for k in ks:
aligned.persist()
aligned_csv = aligned.map(lambda x:','.join(str(d) for d in x))
aligned_csv.saveAsTextFile('aligned.csv')
#$top_k = aligned.sortBy(lambda x:x[1],ascending=False).take(k)
#top_k = sc.parallelize(top_k)
#top_k.persist()
#    file_name = 'top_'+str(k)+'_result'
#    f = open(file_name,'w')
#    f.write('#seq_name, #max_score, #aligned_db ,#aligned_query\n')
#    for ele in top_k:
#        f.write(str(ele))
'''
def del_change_line(s):
    s[1]=s[1][0:-1]
    return[s[0],s[1]]
db = db.map(del_change_line)
print(db.collect())
'''
