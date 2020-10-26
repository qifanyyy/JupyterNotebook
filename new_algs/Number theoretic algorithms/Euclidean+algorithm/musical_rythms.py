"""@package docstring
Documentation for this module.

Details, details, details..
"""
import argparse
import json

f = open('musical_rythms.json', 'r')
f.close()
musical_rythms = json.load(f)

def check_lengths(r):
    """#Called by euclid (k,n) in order to find the position of the first sequence whose length is shorter than that of the first sequence.
"""
    min_length=len(r[0])
    min_length_pos=0
    for i in range(1, len(r)):
        if (len(r[i])<min_length):
            min_length=len(r[i])
            min_length_pos=i
            break
    return min_length_pos

def euclid(k,n):
    """

    #Used to create the euclidean rhythm as a binary sequence.
    #Will do the first step once. (creation of the list of n sequences of 1 bit (represented as strings) and reposition of 0 and 1)
    #After the first step is done, the method calls check_lengths(r). If the shortest length was found in the last position (pos==len(r)-1)
    #or if there isn't any shorter sequence left (pos==0), the while loop will stop. In any other case it repeats the same step (repositioning of the shortest sequences)
    #Finally it creates the final rhythm as a string-sequence of 0 and 1."""
    r=[]
    for i in range (0,k):
        r.append("1")
    for j in range (k, n):
        r.append("0")
    done=False

    c0=k

    while True:
        c1=0
        while (c1<k and c0<len(r)):
            r[c1]+=r[c0]
            c1+=1
            c0+=1

        del r[k:c0]
        pos=check_lengths(r)

        if pos==len(r)-1 or pos==0:
            break
        else:
            c0=pos
            k=pos
    final_r=""
    for i in range(0, len(r)):
        final_r+=r[i]
    #final_r+=""
    return(final_r)

def spaces_vector(r):

    """#Creates the rhythm in the form of a space vector, by counting the spaces between each pulse(1).
    #Returns a list of the spaces(vector)."""
    list_vector=[]
    #str_vector="("
    counter=0
    for i in range(0, len(r)):
        if r[i]=="1":
            if counter>0:
                list_vector.append(counter)
            counter=0
        counter+=1
    list_vector.append(counter)
    return list_vector

#Checks if the given rhythm in the form of a spaces vector is  a Euclidean Sequence.
def isEuclidean(v):
    if len(v)==1:
        return False
    new_v=v
    rev_v=v[::-1]
    new_v[0]=int(new_v[0])+1
    new_v[-1]=int(new_v[-1])-1
    if rev_v==new_v:
        return True
    else:
        return False

#Called when the user gives -s and -p as inputs.
#Creates a final_output as a string in the exact format as requested.
def create_rythm(k,n):
    final_output='E('+str(k)+','+str(n)+') = '
    rythm=euclid(k,n)
    final_output+='['+rythm+']'
    final_output+=" = ("
    list_spaces_vector=spaces_vector(rythm)
    rev_list_spaces_vector=list_spaces_vector[::-1]
    str_spaces_vector=(''.join(map(str, list_spaces_vector)))
    final_output+=str_spaces_vector+')'
    if 'E('+str(k)+','+str(n)+')' in musical_rythms:
        final_output=final_output+" "+ musical_rythms['E('+str(k)+','+str(n)+')']
    print(final_output)
    if isEuclidean(list_spaces_vector)==True:
        print("It is a Euclidean string.")
    if isEuclidean(rev_list_spaces_vector)==True:
        print("It is a reverse Euclidean string.")
    return

#Checks if a given string is actually a Euclidean Rhythm and calculates the number of its pulses(k).
#Will return -1 if the string is not a binary sequence.
#Will return the valid value of the calculated pulses only if the given binary sequence(r) equals the output of the method euclid(k,n) (where n=the length of the given string and k=calculated pulses)
#Else it will return -1.
def isEuclideanRythm(r):
    flag=True
    k=0
    for i in range(0, len(r)):
        if (r[i] is not '1') and (r[i] is not '0'):
            flag=False
            return -1
        else:
            if(r[i] is '1'):
                k+=1
    if flag==True:
        if euclid(k,len(r))==r:
            return k
        else:
            return -1

#Called when the user gives -r as an input.
#At first check if the given string is a Euclidean Rhythm. If not then print message.
#If it is a Euclidean Rhythm, call create_rythm(k,n).
def recognize_rythm(r):
    k=isEuclideanRythm(r)
    if k>0:
        n=len(r)
        create_rythm(k,n)
    else:
        print("Not a Euclidean rythm.")
    return

#Algorithm to calculate the hamming distance as given.
def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(s1, s2))

#Called when the user gives -l as an input. Checks if the given input(r) is a Euclidean Rhythm and prints message if not.
#If it is a Euclidean Rhythm it will calculate the distance between the input(r) and every possible combination of (k,n), where n=len(r) and k [0,n).
#It stores the distance and the (k, n) pair in the form of list and then it sorts that list based on the distance.
#Finally print the output (calculated distance and create_rythm(k,n)) for each sub_list in the r_dist list.
def similar_rythms(r):
    r_dist=[]
    k=isEuclideanRythm(r)
    if k>0:
        n=len(r)
        for i in range(1, n):
            r_sim=euclid(i, n)
            d=hamming_distance(r,r_sim)
            rE=[i, n]
            r_dist.append([d, rE])

        r_dist.sort(key=lambda dist: dist[0])
        for d in r_dist:
            print("Distance = "+str(d[0]))
            create_rythm(d[1][0], d[1][1])
    else:
        print('Not a Euclidean rythm.')




#Store and handle the command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-s",  help="define if next argument is about the number of slots", action="store", dest='slots')
parser.add_argument("-p", help="define if next argument is about the number of pulses", action="store", dest='pulses')
parser.add_argument("-r", help="recognize rhythm",  action="store", dest='recognize')
parser.add_argument("-l", help="List of similar rhythms", action="store", dest='list_rythms' )
args = parser.parse_args()

#Check the arguments given and call the appropriate function.
if args.slots and args.pulses:
    n=int(args.slots)
    k=int(args.pulses)
    create_rythm(k, n)
if args.recognize:
    rythm=args.recognize
    recognize_rythm(rythm)
if args.list_rythms:
    rythm=args.list_rythms
    similar_rythms(rythm)
