
#Create Matrice
def CreateMatrice():
    f = open('input.txt')
    Matrice=[]
    for i in f.readlines():
        if '\n' in i:
            i=i[0:-1]
        Matrice.append([int(j) for j in i.split(' ')])
    return Matrice

#Validating the input
def Validate(Mat):
    validate_counter=1
    for i in Mat:
        if len(i) != len(Mat):
            validate_counter=0
            Mat = standardize(Mat)

    for i in Mat:
        for j in i:
            if j<0:
                validate_counter=0
                Mat= positify(Mat)


    return Mat

'''adds dummy rows or columns in order to make a matrix 
which has equal length of rows and columns'''
def standardize(Mat):
    maximum=max([max(i) for i in Mat])
    while len(Mat)!=len(Mat[0]):
        if len(Mat)<len(Mat[0]):
            Mat.append([maximum for i in range(len(Mat[0]))])
        elif len(Mat)>len(Mat[0]):
            for i in range(len(Mat)):
                Mat[i].append(maximum)
    else:
        return Mat


#Makes All elements nonnegetive
def positify(Mat):
    minimum = abs(min([min(i) for i in Mat]))
    print(minimum)
    for i in Mat:
        for j in range(len(i)):
            i[j]+=minimum
    Show(Mat)
    return Mat

#Show
StepNo=0
def Show(Mat):
    global StepNo
    print('*'*25+'Step '+str(StepNo)+'*'*25)
    Workers = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    Jobs = [' '+str(j) for j in range(27)]
    for i in range(len(Mat)):
        Line = Workers[i]+'  '
        for j in Mat[i]:
            if len(str(j))==1:
                Line+='| '+str(j)+'  '
            else:
                Line+='|'+str(j)+' '
        #print(Line)
    s = [[str(e) for e in row] for row in Mat]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print '\n'.join(table)
    print('*'*50)
    StepNo+=1

#subtract minimun of each row from all elements of row
def reduce_min_row(Mat):
    #step1
    for i in Mat:
        for j in range(len(i)):
            i[j]-=min(i)
    return(Mat)

#turn the matrix by 90 degrees
def turn_by_90(Mat):
    turned=[[j[i] for j in Mat]for i in range(len(Mat))]
    return(turned)

#draws minimum lines (shown by '()') to cover all zeros
def line_drawer(Mat):
    counter=0
    mat = Mat
    rmat=turn_by_90(mat)
    a = max([f.count(0)]for f in mat)[0]
    b = max([f.count(0)]for f in rmat)[0]
    while (a,b)!=(0,0):
        if  a>=b:
            for i in mat:
                if i.count(0)==a:
                    for j in range(len(i)):
                        i[j]='('+str(i[j])+')'
                    counter+=1
            rmat=turn_by_90(mat)
            Show(mat)
        elif b>a:
            for j in rmat:
                if j.count(0)==b:
                    for i in range(len(j)):
                        j[i]='('+str(j[i])+')'
                    counter += 1
            mat=turn_by_90(rmat)
            Show(mat)

        a = max([f.count(0)] for f in mat)[0]
        b = max([f.count(0)] for f in rmat)[0]
    else:
        Show(Mat)
        return [mat,counter]

'''adds the minimum element which is not covered by any line
to the elements which are covered by lines (elements which
are covered twice, would be added twice'''
def add_min_ncovered(Mat):
    minimum=99
    for i in Mat:
        for j in range(len(i)):
            if type(i[j])==int:
                if i[j]<minimum:
                    minimum=i[j]
    for i in Mat:
        for j in range(len(i)):
            if type(i[j])==str:
                if '((' in i[j]:
                    i[j]=int(i[j][2:i[j].index(')')])+minimum*2
    for i in Mat:
        for j in range(len(i)):
            if type(i[j])==str:
                if '(' in i[j]:
                    i[j]=int(i[j][1:i[j].index(')')])+minimum
    Show(Mat)
    return Mat

#subtracts the minimum element of matrix from all elements
def subtract_min_all(Mat):
    minimum=min(min(i) for i in Mat)
    for i in Mat:
        for j in range(len(i)):
            i[j]-=minimum

    Show(Mat)
    return Mat

#removes ),( from elements
def normalize(Mat):
    for i in Mat:
        for j in range(len(i)):
            if type(i[j])==str:
                if '((' in i[j]:
                    i[j]=i[j][2:i[j].index(')')]
    for i in Mat:
        for j in range(len(i)):
            if type(i[j])==str:
                if '(' in i[j]:
                    i[j]=i[j][1:i[j].index(')')]
    return(Mat)

#deletes the possiblity to acquire for other workers
def acquire(Mat,j):
    rmat=turn_by_90(Mat)
    for i in rmat:
        if '%' in i:
            for j in range(len(i)):
                if i[j]=='0':
                    i[j]='N'
    mat=turn_by_90(rmat)
    Show(mat)
    return(mat)

#assigns zeros to rows which have only one zero and acquires the job
def assign(Mat):
    mat=Mat
    for i in mat:
        if i.count('0')==1:
            for j in range(len(i)):
                if i[j]=='0':
                    i[j]='%'
                    mat = acquire(mat,j)
            Show(mat)
            assign(mat)

    return(mat)

#picks a job for a worker which has a dillema :)
def pick(Mat):
    a='@'
    for i in range(len(Mat)):
        if Mat[i].count('0')>1:
            for j in range(len(Mat[i])):
                if Mat[i][j]=='0':
                    Mat[i][j]='%'
                    a=i
                    break
            break
    if a!='@':
        for i in range(len(Mat[a])):
            if Mat[a][i]=='0':
                Mat[a][i]='U'
    Show(Mat)
    return(Mat)

#Decides where to stop the algorithm
def Decide(Mat,lines):
    Finished=1
    for i in Mat:
        for j in i:
            if j=='0' or j=='(0)' or j=='((0))':
                Finished=0

    if Finished==0:
        if len(Mat)==lines:
            Mat=normalize(Mat)
            Mat=assign(Mat)
            Mat=pick(Mat)
            Decide(Mat,lines)

        else:
            Mat=add_min_ncovered(Mat)
            Mat=subtract_min_all(Mat)
            lines=line_drawer(Mat)[1]
            Mat=line_drawer(Mat)[0]
            Decide(Mat,lines)
    else:
        print('Solved')

#is designed to keep the order of process
def OrdSteps(Mat):
    Mat=Validate(Mat)
    Show(Mat)
    Mat=reduce_min_row(Mat)
    Show(Mat)
    Mat=turn_by_90(reduce_min_row(turn_by_90(Mat)))
    Show(Mat)
    lines=line_drawer(Mat)[1]
    Mat=line_drawer(Mat)[0]
    Decide(Mat,lines)

#runs :)
if __name__ == '__main__':
    OrdSteps(CreateMatrice())
