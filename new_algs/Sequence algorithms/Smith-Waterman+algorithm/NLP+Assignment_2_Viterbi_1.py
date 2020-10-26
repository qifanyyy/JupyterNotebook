
# coding: utf-8

# In[1]:

def initial_dist(new, sent):
    global init_dist_lst
    for k in sorted(new):
        init_dist = distributions(new[k], len(sent)) #Contains initial probabilities
        if not init_dist == 0:
            init_dist_lst.append([k, init_dist])
            print("start [",k," |  ] %6f" %init_dist)
    return init_dist_lst


# In[2]:

def merge_list(list1, list2, list3):
    a = []
    j = 0
    k = 0
    for i in range(0, len(list3)):
        a.append([list1[j], list2[k], list3[i]])
        j += 1
        k += 1
    return a


# In[3]:

def sum_elements(list1):
    sum_ele = 0
    for i in range(0, len(list1)):
        if not i >= len(list1):
            if list1[i][0] == list1[i+1][0]:
                sum_ele = list1[i][2] + list1[i+1][2]
            elif list1[i][2] == 1:
                return 1.0
            else:
                return sum_ele


# In[4]:

def sep_bef_aft(data):
    after = []
    before = []
    for line in data.split('\n'):
        bef, sep, aft = line.partition(' ')
        before.append(bef)
        after.append(aft)
    return before, after


# In[5]:

def replace_string(pat, sub, string):
    if string.endswith(pat):
        return string[:-len(pat)] + sub
    else:
        return string


# In[6]:

def distributions(a, b):
    dist = a/b
    return dist


# In[7]:

def sum_init_dist(init_dist_lst):
    a = 0
    for i in range(0, len(init_dist_lst)):
        a += init_dist_lst[i][1]
    return a


# In[8]:

def HMM_Model(before, after, after_new, sent, dtags, counter):
    i = 1
    print("All tags observed:\n")
    for d in dtags:
        print(i, d, "\n")
        i += 1
    
    #Initial Distribution
    new = {} #contains count of tags that appeared at the start of the sentence
    count = 0
    for tag in dtags:
        for i in range(0, len(after_new)):
            if tag == after_new[i][0]:
                count += 1
                i += 1
        new[tag] = count
        count = 0
    init_dist_lst = initial_dist(new, sent)
    sum_init = sum_init_dist(init_dist_lst)

    
    
    #Emission probabilities
    lst_after = [] 
    for i in range(0, len(after)):
        if not after[i] == '':
            lst_after.append(after[i])
    
    lst_before = []
    for i in range(0, len(before)):
        if not before[i] == '':
            lst_before.append(before[i])
    
    j = 0
    global word_tag  #word_tag is a list of lists, with each individual list containing "[word, tag]"
    for i in range(0, len(lst_before)):
        word_tag.append([lst_before[i], lst_after[j]])
        j += 1
    
    #wordtag_lst is a list of dictionaries
    #Each dictionary has key = word and value = corresponding tag
    temp_dict = {}
    global wordtag_lst
    wtc_lst = []
    j = 0
    k = 0
    for i in range(0, len(word_tag)):
        temp_dict = {}
        temp_dict[lst_before[j]] = lst_after[k]
        if not temp_dict in wordtag_lst:
            wordtag_lst.append(temp_dict)
            wtc_lst.append(1)
        else:
            a = wordtag_lst.index(temp_dict)
            wtc_lst.insert(a, wtc_lst.pop(a)+1)
        j += 1
        k += 1
    
    new_tags = []
    for each in wordtag_lst:
        for i in each:
            new_tags.append(each[i])
    
    #Calculate emissioin probabilities and append all probabilities to a list
    emiss_lst = [] #Contains emission probabilities
    j = 0
    for i in range(0, len(new_tags)):
        emiss_prob = distributions(wtc_lst[j], counter[new_tags[i]])
        emiss_lst.append(emiss_prob)
        j += 1
    
    #Seperate the list of dictionaries into two lists
    bf = []
    af = []
    for i in range(0, len(wordtag_lst)):
        for w in wordtag_lst[i]:
            bf.append(w)
            af.append(wordtag_lst[i][w])
    #Append the two lists with the values of emissioin probabilities in the right order
    global emiss_final 
    j = 0
    k = 0
    for i in range(0, len(emiss_lst)):
        emiss_final.append([bf[j], af[k], emiss_lst[i]])
        j += 1
        k += 1
    
    emiss_final = sorted(emiss_final)
    
    j = 0
    print("Emission Probabilities:\n")
    for i in range(1, len(emiss_final)):
        print(emiss_final[i][j], emiss_final[i][j+1],"%6f" % emiss_final[i][j+2], "\n")
    
    
    #Transition Probabilities
    prev_val = ''
    global trans_lst
    trans_count = []
    count = 0
    for a in lst_after:
        trans_dict = {}
        trans_dict[a] = prev_val
        prev_val = a
        if not trans_dict in trans_lst:
            trans_lst.append(trans_dict)
            trans_count.append(1)
        else:
            b = trans_lst.index(trans_dict)
            trans_count.insert(b, trans_count.pop(b)+1)
    
    del trans_lst[0]
    del trans_count[0]
    
    lst1 = []
    lst2 = []
    i = 0
    for i in range(0, len(trans_lst)):
        for t in trans_lst[i]:
            lst1.append(t)
            lst2.append(trans_lst[i][t])
    
    trans_prob_lst = [] #Contains all transition prob
    j = 0
    for i in range(0, len(lst2)):
        trans_prob = distributions(trans_count[j], counter[lst2[i]])
        trans_prob_lst.append(trans_prob)
        j += 1
    global test_trans
    test_trans = merge_list(lst2, lst1, trans_prob_lst)
    test_trans = sorted(test_trans)
    
    print("[",sum_init,"] ", end = ' ')
    j = 0
    for k in sorted(new):
        if not new[k] == 0:
            print("[", k, "|", " ]", "%6f" %init_dist_lst[j][1], end = '')
            j += 1
    
    for i in range(0, len(test_trans)):
        if not i == len(test_trans)-1:
            if test_trans[i][0] == test_trans[i+1][0]:
                print("[",sum_elements(test_trans),"] ","[",test_trans[i][1],"|",test_trans[i][0],"] ","%6f"%test_trans[i][2], end = ' ')
            else:
                print("\n[", sum_elements(test_trans),"] ","[",test_trans[i][1],"|",test_trans[i][0],"] ","%6f"%test_trans[i][2])


# In[9]:

import nltk
from collections import Counter


# In[10]:

input1 = input("Enter the train file: ")
f = open(input1, 'r')

# In[11]:

data = f.read()


# In[12]:

before, after = sep_bef_aft(data)


# In[13]:

before = [x.lower() for x in before]


# In[14]:

new = []
sent = []
j = 0
for i in range(0, len(before)):
    if not before[i] == '':
        new.append(before[i] + " "+ after[j])
        j += 1
    elif before[i] == '':
#         new.append(before[i]+" "+after[j])
        sent.append(new)
        new = []
        j += 1
#Before has all words
#After has all tags


# In[15]:

del sent[-1]


# In[16]:

def lemmatize(word):
    word = replace_string("sses", "ss", word)
    word = replace_string("xes", "x", word)
    word = replace_string("ses", "se", word)
    word = replace_string("zes", "ze", word)
    word = replace_string("ches", "ch", word)
    word = replace_string("shes", "sh", word)
    word = replace_string("men", "an", word)
    word = replace_string("ies", "y", word)
    return word


# In[17]:

for i in range(0, len(before)):
    before[i] = lemmatize(before[i])


# In[18]:

after_new = []
temp = []
j = 0
for i in range(0, len(after)):
    if not after[i] == '':
        temp.append(after[i])
        j += 1
    elif after[i] == '':
        after_new.append(temp)
        temp = []
        j += 1


# In[19]:

dtags = set(after)
counter = Counter(after)


# In[20]:

del after_new[-1]


# In[21]:

dtags = list(sorted(dtags))


# In[22]:

del dtags[0]


# In[23]:

print("University of Central Florida\nCAP6640 Spring 2018 - Dr. Glinos\n\nViterbi Algorithm HMM Tagger by Shashank Subramanian")


# In[24]:

init_dist_lst = []
word_tag = []
emiss_final = []
test_trans = []
wordtag_lst = []
trans_lst = []
HMM_Model(before, after, after_new, sent, dtags, counter)


# In[25]:

print("Corpus Features:\n\n")
print("Total # tags: ", len(dtags),"\n")
print("Total # sentences: ", len(sent), "\n")
print("Total # bigrams: ", len(trans_lst), "\n")
print("Total # lexicals: ", len(wordtag_lst), "\n")


# In[26]:

input2 = input("Enter test file: ")
f = open(input2, 'r')

# In[27]:

data = f.read().lower().split()


# In[28]:

data


# In[29]:

test_word_tag = []
for i in range(0, len(data)):
    for j in range(0, len(word_tag)):
        if data[i] == word_tag[j][0]:
            test_word_tag.append(word_tag[j])


# In[30]:

for i in range(0, len(data)):
    data[i] = lemmatize(data[i])


# In[31]:

bef = []
aft = []
for i in range(0, len(test_word_tag)):
    bef.append(test_word_tag[i][0])
    aft.append(test_word_tag[i][1])


# In[32]:

print("\nTest set found in Corpus:\n\n")
emission_list = []
for i in range(0, len(data)):
    for j in range(0, len(emiss_final)):
        if data[i] == emiss_final[j][0]:
            emission_list.append([data[i], emiss_final[j][1], emiss_final[j][2]])
            print(data[i], " ", emiss_final[j][1], "( %6f"%emiss_final[j][2],")",end = ' ')
    print("\n")


# In[33]:

d_aft = set(aft)


# In[34]:

d_aft = list(d_aft)


# In[35]:

init_values = []
for i in range(0, len(d_aft)):
    for j in range(0, len(init_dist_lst)):
        if d_aft[i] == init_dist_lst[j][0]:
            init_values.append([d_aft[i], init_dist_lst[j][1]])


# In[36]:

emission_val = []
temp = []
for d in range(0, len(data)):
    for i in range(0, len(emission_list)):
        if data[d] == emission_list[i][0]:
            temp.append(emission_list[i][2])
    emission_val.append(temp)
    temp = []


# In[37]:

max_vals = []
for i in range(0, len(emission_val)):
    max_vals.append(max(emission_val[i]))


# In[38]:

print("Viterbi Tagger Output:\n")
k = 0
for i in range(0, len(max_vals)):
    for j in range(0, len(emission_list)):
        if max_vals[i] == emission_list[j][2]:
            print(data[k], emission_list[j][1])
    k += 1


# In[ ]:



