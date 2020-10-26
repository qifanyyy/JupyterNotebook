#Set Score Values
gap = -1
miss = -1
match = 1

def score(X,Y): #Function to determine whether match or miss
    if X == Y:
        return match
    else:
        return miss

text1 = input().upper() #Keep all letters uppercase
text2 = input().upper() #For Homogeneity
l1 = len(text1)
l2 = len(text2)
NW = [[0 for x in range(len(text1)+1)] for y in range(len(text2)+1)] #Initializae Matrix with 0s
NW[0][0] = 0 #Initialize the value in the first cell
path_up = [] #List storing the first word
path_down = [] #List storing the second word

#Build the score table
for j in range(1,l1+1):
    NW[0][j] = gap*j
for i in range(1,l2+1):
    NW[i][0] = gap*i
for i in range(1,l2+1):
    for j in range(1,l1+1):
        #Find max value to put in the cell
        SM1 = NW[i-1][j] + gap
        SM2 = NW[i][j-1] + gap
        SM3 = NW[i-1][j-1] + score(text1[j-1],text2[i-1])
        if SM1 > SM2:
            if SM1 > SM3:
                maxi = SM1
            else:
                maxi = SM3
        else:
            if SM2 > SM3:
                maxi = SM2
            else:
                maxi = SM3
        NW[i][j] = maxi
print(NW)

i = l2
j = l1
s = 0
while i > 0 and j > 0:
    if NW[i][j] == NW[i-1][j-1] + score(text2[i-1], text1[j-1]): #Check Diagonal Element
        s += score(text2[i-1], text1[j-1])
        path_down.append(text2[i-1])
        path_up.append(text1[j-1])
        i -= 1
        j -= 1
    elif NW[i][j] == NW[i-1][j] + gap: #Check Left Element
        s += gap
        path_down.append(text2[i-1])
        path_up.append('_')
        i -= 1
    elif NW[i][j] == NW[i][j-1] + gap: #Check Above Element
        s += gap
        path_down.append('_')
        path_up.append(text1[j-1])
        j -= 1
while i > 0: #Add remaining letters of the second word
    s += gap
    path_down.append(text2[i-1])
    path_up.append('_')
    i -= 1
while j > 0: #Add remaining letters of the first word
    s += gap
    path_down.append('_')
    path_up.append(text1[j-1])
    j -= 1

print(list(reversed(path_up)))
print(list(reversed(path_down)))
print("Score =",s)