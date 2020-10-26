# Bubble sort by Alister 0340938

List = []                                    # \\
print("<-- Bubble Sort by Alister -->")       # \\
print()                                        # || This is the part where user
a = int(input('Enter The Number 70: '))        # || inputs 70, and by iteration
List.append(a)                                 # || a list ranging from 70 - 10
for i in range(0, 6):                          # || is created and printed.
    a = a - 10                                 # ||
    List.append(a)                             # ||
print("Unsorted List = "+str(List))           # //
print()                                      # //

List_len = len(List)-1                                        # \\
sorted = False                                                 # \\
while not sorted:                                               # || This is the part of the code
    sorted = True                                               # || where the main
    for k in range(1, 7):                                       # || bubble sort takes
        for j in range(0, List_len):                            # || place.
            if List[j] > List[j+1]:                             # ||
                sorted = False                                  # ||
                List[j], List[j+1] = List[j+1], List[j]         # ||
                print("After Pass "+str(k) + ", Inner Loop " +  # ||
                      str(j+1)+" = "+str(List))                 # ||
            j = j+1                                             # ||
print()                                                        # //
print("Final Sorted List = "+str(List))                       # //
