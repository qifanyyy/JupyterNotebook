# Selection sort by Alister 0340938

List = []                                    # \\
print("<-- Selection Sort by Alister -->")    # \\
print()                                        # || This is the part where user
a = int(input('Enter The Number 70: '))        # || inputs 70, and by iteration
List.append(a)                                 # || a list ranging from 70 - 10
for i in range(0, 6):                          # || is created and printed.
    a = a - 10                                 # ||
    List.append(a)                             # ||
print("Unsorted List = "+str(List))           # //
print()                                      # //

for j in range(0, 3):                                # \\
    Min = min(List[j:])                               # || This is the part of
    Min_pos = List.index(Min)                         # || the code where the
    List[j], List[Min_pos] = List[Min_pos], List[j]   # || main selection sort
    print("After Pass "+str(j+1)+" = "+str(List))     # || takes place.
    j = j+1                                           # ||
print()                                               # ||
print("Final Sorted List = "+str(List))              # //
