# PROGRAMMING ASSIGNMENT 3 - VHAIJAIYANTHISHREE VENKATARAMANAN
# THIS PROGRAM USES PYTHON VERSION 3 (3.6.4)
# TO EXECUTE THIS PROGRAM PLEASE USE THE FOLLOWING COMMAND ON TERMINAL/COMMAND PROMPT:
#			python3 Vhaijaiyanthi_pa3.py
# KINDLY ENSURE THAT THIS PROGRAM AND ITS REQUIRED INPUT FILES <piper.txt> and <wsj-clean.txt> ARE PLACED ON THE SAME FOLDER FROM WHERE YOU INTENT TO RUN THE PROGRAM
# *THANK YOU FOR YOUR TIME*


import sys
from collections import defaultdict

# OPENING THE REQUIRED INPUT TESTING AND TRAINING FILES
print("\n\nUniversity of Central Florida \nCAP6640 Spring 2018 - Dr. Glinos \nDependency Parser by <Vhaijaiyanthishree Venkataramanan>\n\n")

test = 'piper.txt'
train = 'wsj-clean.txt'
test = open(test, 'r')
train = open(train, 'r')
test_Data = test.read()
train_Data = train.read()
trainingList = train_Data.split("\n\n")



# IDENTIFYING WHETHER THE GIVEN SENTENCES YEILD A LEFT OR RIGHT SHIFT
def LR_shift(teach):

    count = 0
    POS_tags = []
    left = 0
    right = 0
    for x in teach:
        y = x.split("\n")
        count += len(y)
        for z in y:
            a = z.split()
            if len(a) > 0:
                if int(a[0]) < int(a[3]):
                    left += 1
                else:
                    right += 1
                POS_tags.append(a[2])

    POS_tags = sorted(set(POS_tags))
    return count-1, len(POS_tags), left, right-len(teach), POS_tags
m = LR_shift(trainingList)
POS_tags = m[4]

# PRINTING THE CORPUS STATISTICS 
print("Corpus Statistics:\n")
print("\t# sentences  : {:>6}".format(len(trainingList)))
print("\t# tokens     : {:>6}".format(m[0]))
print("\t# POS tags   : {:>6}".format(m[1]))
print("\t# Left-Arcs  : {:>6}".format(m[2])) 
print("\t# Right-Arcs : {:>6}".format(m[3]))
print("\t# Root-Arcs  : {:>6}".format(len(trainingList)))


def treeShift(teach):
    l1 = []
    l2 = []
    for x in teach:
        y = x.split()
        l1.append(y)
    for l in l1:
        l3 = []
        swap = []
        count = 0
        for z in range(len(l)):
            l3.append(l[z])
            count += 1
            if count == 4:
                l3[3], l3[0] = int(l3[0]), int(l3[3])
                swap.append(l3)
                l3 = []
                count = 0
        l2.append(sorted(swap))

    return l2

y = treeShift(trainingList)



# FINDING THE COUNT OF THE DIFFERENT OCCURENCES OF EACH TAG
def tagCount(teach):

    l2 = []
    for h in teach:
        q = defaultdict(list)
        for k in h:
            if k[2] in q:
            	q[k[2]].extend([k[0],k[3]])
            else:
                q[k[2]] = [k[0],k[3]]
        l2.append(dict(q))

    return l2
tag = tagCount(y)



# FINDING THE LEFT ARC ARRAY NON-ZERO COUNTS
def leftArc(all, tag_group):

    allLeft = []
    for h in all:
        stay = defaultdict(list)
        for i in h:
            j = h[i][::2]
            k = h[i][1::2]
            # ELEMENTS WITH AN INDEX VALUE GREATER THAN THE INDEX NUMBER IN A SENTENCE
            # ARE COLLECTED AND APPENDED TO A LIST
            for l in range(len(j)):
                if j[l] > k[l]:
                    stay[i].append(j[l])
        allLeft.append(dict(stay)) #LIST

    allList_left = {}

    for h in tag_group:

        leftTag = []
        for i in all:
            if h in i:
                leftTag.append(list(i[h][1::2]))
            else:
                leftTag.append(["null"])

        allList_left[h] = leftTag # DICTIONARY

    left_tree = {}
    for tup in tag_group:

        count = 0
        stay = {}
        for sentence in allLeft:
            if tup in sentence:
                j = sentence[tup]
                for diff_tags in allList_left:
                    i = allList_left[diff_tags]
                    l = i[count]
                    for h in range(len(j)):
                        if j[h] in l or j[h] == l:
                            if diff_tags in stay:
                                stay[diff_tags] = stay[diff_tags] + 1
                            else:
                                stay[diff_tags] = 1
            count += 1

        left_tree[tup] = stay

    return left_tree
arcLeft_count = leftArc(tag, POS_tags)

print("\n\nLeft Arc Array Nonzero Counts:\n")


    
# FINDING THE RIGHT ARC ARRAY NON-ZERO COUNTS
def rightArc(all, tag_group):

    allRight = []
    for h in all:
        stay = defaultdict(list)
        for i in h:
            j = h[i][::2]
            k = h[i][1::2]
            # ELEMENTS WITH AN INDEX VALUE GREATER THAN THE INDEX NUMBER IN A SENTENCE
            # ARE COLLECTED AND APPENDED TO A LIST
            for l in range(len(j)):
                if j[l]< k[l] and j[l] != 0:
                    stay[i].append(j[l])
        allRight.append(dict(stay)) #LIST

    allList_Right = {}

    for h in tag_group:

        rightTag = []
        for i in all:
            if h in i:
                rightTag.append(list(i[h][1::2]))
            else:
                rightTag.append(["null"])

        allList_Right[h] = rightTag # DICTIONARY

    right_tree = {}
    for tup in tag_group:

        count = 0
        stay = {}
        for sentence in allRight:
            if tup in sentence:
                j = sentence[tup]
                for diff_tags in allList_Right:
                    i = allList_Right[diff_tags]
                    l = i[count]
                    for h in range(len(j)):
                        if j[h] in l or j[h] == l:
                            if diff_tags in stay:
                                stay[diff_tags] = stay[diff_tags] + 1
                            else:
                                stay[diff_tags] = 1
            count += 1

        right_tree[tup] = stay

    return right_tree
arcRight_count = rightArc(tag, POS_tags)



# FINDING THE ARC CONFUSION ARRAY
def confusionArc(left,right):

    allconfusion_List = {}
    for tag in left:
        tag_list = left[tag]
        blank = {}
        for n_tags in tag_list:
            i = right[tag]
            if n_tags in i:
                blank[n_tags] = [tag_list[n_tags],i[n_tags]]

        allconfusion_List[tag] = blank

    count = 0
    for one in allconfusion_List:
        two = allconfusion_List[one]
        three = two.keys()
        count = count + len(three)

    return allconfusion_List, count
    
arcConfusion_count = confusionArc(arcLeft_count,arcRight_count)

# TRAINING THE ORACLE
def trainOracle(teach):

    d1 = {}
    train = teach.split()
    for each in train:
        h = each.split("/")
        d1[h[0]] = h[1]
    y = ""
    for x in train:
    	y = y + x + " "

    print("\nInput Sentence:")
    print(y)
    print("\n\nParsing Actions and Transitions:\n")

    global stack
    stack_list = []
    buffer_list = train
    print('[%s]'% ', '.join(map(str,stack_list)),'[ %s]'% ', '.join(map(str,buffer_list)),"SHIFT")
    stack_list.append(buffer_list[0])
    del buffer_list[0]
    print('[ %s]'% ', '.join(map(str,stack_list)),'[ %s]'% ', '.join(map(str,buffer_list)),"SHIFT")
    stack_list.append(buffer_list[0])
    del buffer_list[0]
    bar = 1
    return [buffer_list, stack_list, bar]
    

# PARSING ACTIONS AND TRANSITIONS
def oracle(left_arc,right_arc,confusion_arc,buffer_volume,stack_volume):

    buffer_list = buffer_volume
    stack_list = stack_volume

    if len(stack_list) == 1 and len(buffer_list) != 0:
        print('[ %s]'% ', '.join(map(str,stack_list)),'[ %s]'% ', '.join(map(str,buffer_list)),"SHIFT")
        stack_list.append(buffer_list[0])
        del buffer_list[0]

    if len(buffer_list) == 0 and len(stack_list) == 1:
        print('[ %s]' % ', '.join(map(str, stack_list)), '[ %s]' % ', '.join(map(str, buffer_list)), "ROOT -->", stack_list[0])
        del stack_list[0]


    if len(stack_list) > 1:
        jth = stack_list[-1].split("/")[1]
        ith = stack_list[-2].split("/")[1]

        # FIRST RULE
        if ith[0] == 'V' and (jth[0] == '.' or jth[0] == 'R'):
            print('[ %s]' % ', '.join(map(str, stack_list)), '[ %s]' % ', '.join(map(str, buffer_list)), "Right-Arc:", stack_list[-2],"-->", stack_list[-1])
            del stack_list[-1]

        # SECOND RULE
        elif ith[0] == 'I' and jth[0] == '.':
            print('[ %s]' % ', '.join(map(str, stack_list)), '[ %s]' % ', '.join(map(str, buffer_list)), "SWAP")
            buffer_list.append(stack_list[-2])
            del stack_list[-2]

        # THIRD RULE
        elif (ith[0] == 'V' or ith[0] == 'I') and (jth[0] == 'D' or jth[0] == 'I' or jth[0] == 'J' or jth[0] == 'P' or jth[0] == 'R') and len(buffer_list) != 0:
            print('[ %s]' % ', '.join(map(str, stack_list)), '[ %s]' % ', '.join(map(str, buffer_list)), "SHIFT")
            if len(buffer_list) > 0:
                stack_list.append(buffer_list[0])
                del buffer_list[0]

        # CONFUSION ARC
        elif ith in confusion_arc and jth in confusion_arc[ith]:
            conf = confusion_arc[ith][jth]
            if conf.index(max(conf)) == 1:
                print('[ %s]' % ', '.join(map(str, stack_list)), '[ %s]' % ', '.join(map(str, buffer_list)), "Right-Arc:",stack_list[-2], "-->", stack_list[-1])
                del stack_list[-1]
            elif conf.index(max(conf)) == 0:
                print('[ %s]' % ', '.join(map(str, stack_list)), '[ %s]' % ', '.join(map(str, buffer_list)), "Left-Arc:", stack_list[-2],"<--", stack_list[-1])
                del stack_list[-2]

        # EXCLUSIVELY LEFT ARC
        elif ith in left_arc and jth in left_arc[ith]:
            print(stack_list,buffer_list,"Left-Arc:",stack_list[-2],"<--",stack_list[-1])
            del stack_list[-2]

        # EXCLUSIVELY RIGHT ARC
        elif jth in right_arc and ith in right_arc[jth]:
            print('[ %s]' % ', '.join(map(str, stack_list)), '[ %s]' % ', '.join(map(str, buffer_list)), "Left-Arc:", stack_list[-2],"<--", stack_list[-1])
            del stack_list[-1]

        else:
            print('[ %s]' % ', '.join(map(str, stack_list)), '[ %s]' % ', '.join(map(str, buffer_list)), "SHIFT")
            if len(buffer_list) > 0:
                stack_list.append(buffer_list[0])
                del buffer_list[0]

    if len(stack_list) == 0:
        bar = 0
    else:
        bar = 1

    return [buffer_list, stack_list, bar]
    
    
# PRINTING THE LEFT ARC ARRAY, RIGHT ARC ARRAY AND ARC CONFUSION ARRAY VALUES    
for tag in POS_tags:
    p = ""
    q = arcLeft_count[tag]
    r = 4 - len(tag)
    for next_tag in POS_tags:
        if next_tag in q:
            q_1 = q[next_tag]
            p = p + "[" + " " +'{:>4}'.format(str(next_tag)) + ", " +'{:>3}'.format(str(q_1)) + "] "
    print(" "*r,tag,":",p)
    
print("\n\nRight Arc Array Nonzero Counts:\n")
for tag in POS_tags:
    p = ""
    q = arcRight_count[tag]
    r = 4 - len(tag)
    for next_tag in POS_tags:
        if next_tag in q:
            q_1 = q[next_tag]
            p = p + "[" + " " +'{:>4}'.format(str(next_tag)) + ", " +'{:>3}'.format(str(q_1)) + "] "
    print(" "*r,tag,":",p)
    
print("\n\nArc Confusion Array:\n")
for tag in POS_tags:
    p = ""
    q = arcConfusion_count[0][tag]
    r = 4 - len(tag)
    for next_tag in POS_tags:
        if next_tag in q:
            q_1 = q[next_tag]
            p = p + "[" + " " +'{:4}'.format(str(next_tag)) + ", " + '{:>3}'.format(str(q_1[0])) + ", " +'{:>3}'.format(str(q_1[1])) + "] "
    print(" "*r,tag,":",p)
print("\n\tNumber of confusing arcs =", arcConfusion_count[1])


final_l = trainOracle(test_Data)


while final_l[2] == 1:
    out = oracle(arcLeft_count,arcRight_count,arcConfusion_count[0],final_l[0],final_l[1])
    final_l[0] = out[0]
    final_l[1] = out[1]
    final_l[2] = out[2]
