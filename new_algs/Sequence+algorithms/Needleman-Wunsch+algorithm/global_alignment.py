import numpy as np
import json

#structure section
class AlignedSequence:
    def __init__(self):
        self.index = -1
        self.seq1 = []
        self.seq2 = []
        self.relation = []
        self.score = []
        return

    def add(self, index, char_seq1, char_seq2, relation, score):
        self.seq1.insert(index, char_seq1)
        self.seq2.insert(index, char_seq2)
        self.relation.insert(index, relation)
        self.score.insert(index, score)

    def add_first(self, char_seq1, char_seq2, relation, score):
        self.add(0, char_seq1, char_seq2, relation, score)

    
    def append(self, char_seq1, char_seq2, relation, score):
        self.seq1.append(char_seq1)
        self.seq2.append(char_seq2)
        self.relation.append(relation)
        self.score.append(score)

    def getTotalScore(self):
        total = 0
        for val in self.score:
            total = total + val
        return total

    def getSeq1(self):
        return self.seq1

    def getSeq2(self):
        return self.seq2


    def getRelation(self):
        return self.relation

    def getScore(self):
        return self.score

    def printSequence(self, idx):
        line0 = 'Alignment - ' + str(idx)
        line1 = ''
        line2 = ''
        line3 = ''
        line4 = ''
        for i in range(0, len(self.score)):
            line1 = line1 + self.seq1[i]
            line2 = line2 + self.relation[i]
            line3 = line3 + self.seq2[i]
            strScore = ''
            if self.score[i] >= 0:
                strScore = '+' + str(self.score[i])
            else:
                strScore = str(self.score[i])
            line4 = line4 + strScore
        print(line0)
        print(line1)
        print(line2)
        print(line3)
        print(line4)
        print("Total Score : " + str(self.getTotalScore()) + "\n")

class Node:
    def __init__(self, i, j):
        self.p = []
        self.dir = []
        self.score = -99999
        self.i = i
        self.j = j
        return
        
    def add(self, Node, d):
        #self.p.insert(len(self.p), Node)
        self.p.append(Node)
        self.dir.append(d)

    def setScore(self, score):
        self.score = score

    def getLength(self):
        return len(self.p)

    def getI(self):
        return self.i

    def getJ(self):
        return self.j

    def getId(self):
        return str(self.i) + str(self.j)

    def getListOfDirection(self):
        tmp = ""
        if len(self.p) > 0:
            i = 0
            for p in self.p:
                #tmp = tmp + "[" + str(p.j) + "," + str(p.i) + "]" + str(self.dir[i])
                tmp = tmp + str(self.dir[i])
                i = i + 1
        else:
            tmp = tmp + "[NA]"
        return tmp

    def getScore(self):
        return self.score

    def getDirection(self):
        return self.dir

    def getSourceCoord(self):
        tmp = ""
        #i = 0
        for p in self.p:
            #tmp = tmp + "[" + str(p.j) + "," + str(p.i) + "]" + str(self.dir[i])
            tmp = tmp + str(p.getId()) + "#"
            #i = i + 1
        return tmp


#global variable section
table = None
backtrace = None
m = 0 #length information of sequence 1
n = 0 #length information of sequence 2
s1 = ''
s2 = ''
match = 0
missmatch = 0
gap = 0


#Alignment algorithm section
# T(j,i) = max{
#   T(i-1,j-1) + Sim(S1(i), S2(j))
#   T(i-1,j) + gap (row ref)
#   T(i,j-1) + gap (column ref)
#   0 for local alignment
def FindMax(type, i, j):
    #global s1, s2
    global match, missmatch, gap, table, backtrace
    a = 0
    b = 0
    c = 0

    if i-1 >= 0 and j-1 >= 0:
        if s2[i-1] == s1[j-1]:
            a = table[i-1][j-1] + match
        elif s2[i-1] != s1[j-1]:
            a = table[i-1][j-1] + missmatch

    if i-1 >= 0:
        b = table[i-1][j] + gap
    else:
        a = -999999
        b = -999999

    if j-1 >= 0:
        c = table[i][j-1] + gap
    else:
        a = -999999
        c = -999999
    if type == 'NW':
        max_value = np.max(np.array([a,b,c]))
    elif type == 'SW':
        max_value = np.max(np.array([a,b,c,0]))

    if max_value == a:
        backtrace[i][j].add(backtrace[i-1][j-1], "D")
    if max_value == b:
        backtrace[i][j].add(backtrace[i-1][j], "U")
    if max_value == c:
        backtrace[i][j].add(backtrace[i][j-1], "L")
    backtrace[i][j].setScore(max_value)
    table[i][j] = max_value


def DoAlignment(p_s1, p_s2, p_match, p_missmantch, p_gap, type):
    global s1, s2
    global m, n
    global table, backtrace
    global match, missmatch, gap
    match = p_match
    missmatch = p_missmantch
    gap = p_gap
    s1 = p_s1
    s2 = p_s2

    #length check
    '''
    if len(s1) != len(s2):
        if len(s1) > len(s2):
            for i in range(len(s2), len(s1)):
                s2 = s2 + '-'
        else:
            for i in range(len(s1), len(s2)):
                s1 = s1 + '-'
    '''

    m = len(s1)+1 # column # j
    n = len(s2)+1 # row # i
    table = np.zeros((n, m))
    
    #print(len(table))
    #print(len(table[0]))
    #init
    table[0][0] = 0
    backtrace = []
    
    
    for i in range(0, n):
        row = []
        for j in range(0, m):
            node = Node(i, j)
            node.setScore(0)
            row.append(node)
        backtrace.append(row)


    for i in range(1, n):
        FindMax(type, i, 0)

    for j in range(1, m):
        FindMax(type, 0, j)


    for i in range(1, n):
        for j in range(1, m):
            FindMax(type, i, j)
    DoBacktrace()
    #print(table)
    



def ShowNode(withCoord, withScore, withDirection, withSourceCoord):
    global backtrace
    for i in range(0, len(backtrace)):
        tmp = ""
        for j in range(0, len(backtrace[i])):
            c = ''
            s = ''
            d = ''
            sc = ''
            if withCoord == True:
                c = backtrace[i][j].getId()
            if withScore == True:
                s = backtrace[i][j].getScore()
            if withDirection == True:
                d = backtrace[i][j].getDirection()
            if withSourceCoord == True:
                sc = backtrace[i][j].getSourceCoord()
            tmp = tmp + str(c) + " " + str(s) + " " + str(d) + " " + str(sc) + " ** "
            #tmp = tmp + str(backtrace[i][j].getListOfDirection()) + " ** "
        print(tmp)
    print('\n')
    

def ShowReverseNode():
    global backtrace
    for i in reversed(xrange(len(backtrace))):
        tmp = ""
        for j in reversed(xrange(len(backtrace[i]))):
            tmp = tmp + backtrace[i][j].getId() + "|" + str(backtrace[i][j].getSourceCoord()) + " " + str(backtrace[i][j].getDirection()) + " ** "
            #tmp = tmp + str(backtrace[j][i].getId()) + " ** "
        print(tmp)
    print("\n")

def FindSourceNode(listNode, node):
    n = None
    for i in range(0, len(listNode)):
        for j in listNode[i].p:
            if j.getId() == node.getId() and len(listNode[i].p) > 1:
                n = listNode[i]
    return n

#nodeSequences = []
alignedSeq = []
def alignCheck(dir, i, j):
    global alignedSeq
    if dir == "L":
        alignedSeq[len(alignedSeq)-1].add_first('-', s1[j-1], ' ', gap)
    elif dir == "U":
        alignedSeq[len(alignedSeq)-1].add_first(s2[i-1], '-', ' ', gap)
    else:
        if s2[i-1] == s1[j-1]:
            alignedSeq[len(alignedSeq)-1].add_first(s1[j-1], s2[i-1], '|', match)
        else:
            alignedSeq[len(alignedSeq)-1].add_first(s1[j-1], s2[i-1], ' ', missmatch)

def DoBacktrace():
    global m, n, alignedSeq
    #print(str(m) + ' ' + str(n))
    nodeSeq = ""
    node = backtrace[n-1][m-1]
    #print(node.getId())
    openNode = []
    openNode.append(node)
    closedNode = []
    alignedSeq = []
    
    while len(openNode) > 0:
        currentNode = openNode.pop()
        closedNode.append(currentNode)
        nodeSeq = nodeSeq + currentNode.getId()
        for p in currentNode.p:
            openNode.append(p)
    alignedSeq.append(AlignedSequence())
    
    dir_idx = 0
    for i in range(0, len(closedNode)):
        dir_idx = len(closedNode[i].p) - 1
        next_idx_of_alt = dir_idx - 1
        if closedNode[i].getI() != 0 or closedNode[i].getJ() != 0:
            alignCheck(closedNode[i].getDirection()[dir_idx], closedNode[i].getI(), closedNode[i].getJ())
            
        if closedNode[i].getI() == 0 and closedNode[i].getJ() == 0 and i != len(closedNode) - 1:
            alignedSeq.append(AlignedSequence())
            prevNode = FindSourceNode(closedNode, closedNode[i+1])
            while prevNode != None:
                alignCheck(prevNode.getDirection()[next_idx_of_alt], prevNode.getI(), prevNode.getJ())
                prevNode = FindSourceNode(closedNode, prevNode)
             
    #print(len(alignedSeq))
    for i in range(1, len(alignedSeq)):
        startIdx = len(alignedSeq[i].relation)
        for j in range(startIdx, len(alignedSeq[0].relation)):
            alignedSeq[i].add_first(alignedSeq[0].seq1[j], alignedSeq[0].seq2[j], alignedSeq[0].relation[j], alignedSeq[0].score[j])



def ShowAlignedSequence():
    for val in range(0, len(alignedSeq)):
        alignedSeq[val].printSequence(val+1)


def ConvertToJSON():
    score_raw = []
    direction_raw = []
    for i in range(0, len(backtrace)):
        score_raw_tmp = []
        direction_raw_tmp = []
        for j in range(0, len(backtrace[i])):
            score_raw_tmp.append(backtrace[i][j].getScore())
            direction_raw_tmp.append(backtrace[i][j].getDirection())
        score_raw.append(score_raw_tmp)
        direction_raw.append(direction_raw_tmp)
    

    a = {}
    a['score'] = score_raw
    a['direction'] = direction_raw
    result = []


    for val in range(0, len(alignedSeq)):
        tmp = {}
        tmp['seq1'] = alignedSeq[val].getSeq1()
        tmp['seq2'] = alignedSeq[val].getSeq2()
        tmp['relation'] = alignedSeq[val].getRelation()
        tmp['score'] = alignedSeq[val].getScore()
        tmp['total_score'] = alignedSeq[val].getTotalScore()
        result.append(tmp)
        #alignedSeq[val].printSequence()
    
    a['result'] = result
    return a
    #js_d = json.dumps(a)
    #js_d = json.loads('[' + js_d + ']')
    #return js_d
    #print(js_d)
    #print('\n')


a_match = 1
a_missmatch = -1
a_gap = -2

#s1 = raw_input('Enter First Sequence: ')
a_s1 = "ATTGCCCATTTG"
#s2 = raw_input('Enter Second Sequence: ')
a_s2 = "ACTGCAACTTGA"


#DoAlignment(a_s1, a_s2, a_match, a_missmatch, a_gap)

#ShowNode(True, False, False, False)
#ShowNode(False, True, False, False)
#ShowNode(False, False, True, False)
#ShowNode(False, False, False, True)
#ConvertToJSON()
#ShowReverseNode()
#ShowAlignedSequence()
#print(nodeSeq)
#print(s1[3])
