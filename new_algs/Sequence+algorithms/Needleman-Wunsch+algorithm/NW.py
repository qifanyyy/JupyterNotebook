import sys
import getopt
import os
import math
import operator
#Used to convert the three-letter code in pdb files to one-letter code
ThreeToOne = {'ALA':'A','CYS':'C','ASP':'D','GLU':'E','PHE':'F','GLY':'G','HIS':'H','ILE':'I','LYS':'K','LEU':'L','MET':'M',
              'ASN':'N','PRO':'P','GLN':'Q','ARG':'R','SER':'S','THR':'T','VAL':'V','TRP':'W','TYR':'Y'}
class NW:
  def __init__(self):
    self.table = [[]]
    self.str1 = ""
    self.str2 = ""
    self.backtrace = []
    self.buff = []
    self.check_point = []
    self.check_count = []
    #Scoring matrix is hard-coded from BLOSUM62
    self.score_matrix = {'A': {'A': 4,'R':-1,'N':-2,'D':-2,'C': 0,'Q':-1,'E':-1,'G': 0,'H':-2,'I':-1,'L':-1,'K':-1,'M':-1,'F':-2,'P':-1,'S': 1,'T': 0,'W':-3,'Y':-2,'V': 0},
                        'R': {'A':-1,'R': 5,'N': 0,'D':-2,'C':-3,'Q': 1,'E': 0,'G':-2,'H': 0,'I':-3,'L':-2,'K': 2,'M':-1,'F':-3,'P':-2,'S':-1,'T':-1,'W':-3,'Y':-2,'V':-3}, 
                        'N': {'A':-2,'R': 0,'N': 6,'D': 1,'C':-3,'Q': 0,'E': 0,'G': 0,'H': 1,'I':-3,'L':-3,'K': 0,'M':-2,'F':-3,'P':-2,'S': 1,'T': 0,'W':-4,'Y':-2,'V':-3}, 
                        'D': {'A':-2,'R':-2,'N': 1,'D': 6,'C':-3,'Q': 0,'E': 2,'G':-1,'H':-1,'I':-3,'L':-4,'K':-1,'M':-3,'F':-3,'P':-1,'S': 0,'T':-1,'W':-4,'Y':-3,'V':-3}, 
                        'C': {'A': 0,'R':-3,'N':-3,'D':-3,'C': 9,'Q':-3,'E':-4,'G':-3,'H':-3,'I':-1,'L':-1,'K':-3,'M':-1,'F':-2,'P':-3,'S':-1,'T':-1,'W':-2,'Y':-2,'V':-1}, 
                        'Q': {'A':-1,'R': 1,'N': 0,'D': 0,'C':-3,'Q': 5,'E': 2,'G':-2,'H': 0,'I':-3,'L':-2,'K': 1,'M': 0,'F':-3,'P':-1,'S': 0,'T':-1,'W':-2,'Y':-1,'V':-2}, 
                        'E': {'A':-1,'R': 0,'N': 0,'D': 2,'C':-4,'Q': 2,'E': 5,'G':-2,'H': 0,'I':-3,'L':-3,'K': 1,'M':-2,'F':-3,'P':-1,'S': 0,'T':-1,'W':-3,'Y':-2,'V':-2}, 
                        'G': {'A': 0,'R':-2,'N': 0,'D':-1,'C':-3,'Q':-2,'E':-2,'G': 6,'H':-2,'I':-4,'L':-4,'K':-2,'M':-3,'F':-3,'P':-2,'S': 0,'T':-2,'W':-2,'Y':-3,'V':-3}, 
                        'H': {'A':-2,'R': 0,'N': 1,'D':-1,'C':-3,'Q': 0,'E': 0,'G':-2,'H': 8,'I':-3,'L':-3,'K':-1,'M':-2,'F':-1,'P':-2,'S':-1,'T':-2,'W':-2,'Y': 2,'V':-3}, 
                        'I': {'A':-1,'R':-3,'N':-3,'D':-3,'C':-1,'Q':-3,'E':-3,'G':-4,'H':-3,'I': 4,'L': 2,'K':-3,'M': 1,'F': 0,'P':-3,'S':-2,'T':-1,'W':-3,'Y':-1,'V': 3}, 
                        'L': {'A':-1,'R':-2,'N':-3,'D':-4,'C':-1,'Q':-2,'E':-3,'G':-4,'H':-3,'I': 2,'L': 4,'K':-2,'M': 2,'F': 0,'P':-3,'S':-2,'T':-1,'W':-2,'Y':-1,'V': 1}, 
                        'K': {'A':-1,'R': 2,'N': 0,'D':-1,'C':-3,'Q': 1,'E': 1,'G':-2,'H':-1,'I':-3,'L':-2,'K': 5,'M':-1,'F':-3,'P':-1,'S': 0,'T':-1,'W':-3,'Y':-2,'V':-2}, 
                        'M': {'A':-1,'R':-1,'N':-2,'D':-3,'C':-1,'Q': 0,'E':-2,'G':-3,'H':-2,'I': 1,'L': 2,'K':-1,'M': 5,'F': 0,'P':-2,'S':-1,'T':-1,'W':-1,'Y':-1,'V': 1}, 
                        'F': {'A':-2,'R':-3,'N':-3,'D':-3,'C':-2,'Q':-3,'E':-3,'G':-3,'H':-1,'I': 0,'L': 0,'K':-3,'M': 0,'F': 6,'P':-4,'S':-2,'T':-2,'W': 1,'Y': 3,'V':-1}, 
                        'P': {'A':-1,'R':-2,'N':-2,'D':-1,'C':-3,'Q':-1,'E':-1,'G':-2,'H':-2,'I':-3,'L':-3,'K':-1,'M':-2,'F':-4,'P': 7,'S':-1,'T':-1,'W':-4,'Y':-3,'V':-2}, 
                        'S': {'A': 1,'R':-1,'N': 1,'D': 0,'C':-1,'Q': 0,'E': 0,'G': 0,'H':-1,'I':-2,'L':-2,'K': 0,'M':-1,'F':-2,'P':-1,'S': 4,'T': 1,'W':-3,'Y':-2,'V':-2}, 
                        'T': {'A': 0,'R':-1,'N': 0,'D':-1,'C':-1,'Q':-1,'E':-1,'G':-2,'H':-2,'I':-1,'L':-1,'K':-1,'M':-1,'F':-2,'P':-1,'S': 1,'T': 5,'W':-2,'Y':-2,'V': 0}, 
                        'W': {'A':-3,'R':-3,'N':-4,'D':-4,'C':-2,'Q':-2,'E':-3,'G':-2,'H':-2,'I':-3,'L':-2,'K':-3,'M':-1,'F': 1,'P':-4,'S':-3,'T':-2,'W':11,'Y': 2,'V':-3}, 
                        'Y': {'A':-2,'R':-2,'N':-2,'D':-3,'C':-2,'Q':-1,'E':-2,'G':-3,'H': 2,'I':-1,'L':-1,'K':-2,'M':-1,'F': 3,'P':-3,'S':-2,'T':-2,'W': 2,'Y': 7,'V':-1}, 
                        'V': {'A': 0,'R':-3,'N':-3,'D':-3,'C':-1,'Q':-2,'E':-2,'G':-3,'H':-3,'I': 3,'L': 1,'K':-2,'M': 1,'F':-1,'P':-2,'S':-2,'T': 0,'W':-3,'Y':-1,'V': 4}}
  
  #initial the score table
  def initial_table(self,a,b):
    self.table = [[0]*(len(b)+1) for _ in range(len(a)+1)]
    self.La = len(a)
    self.Lb = len(b)
    self.str1 = a
    self.str2 = b
    self.buff = [[self.La,self.Lb]]
  #Build the score table forward, not using recursive for the sake of the running speed
  def Needleman(self):
    for j in range(0,self.Lb+1):
      self.table[0][j] = j*(-8)
    for i in range(0,self.La+1):
      self.table[i][0] = i*(-8)
    for i in range(1,self.La+1):
      for j in range(1,self.Lb+1):
        self.table[i][j] = max(self.table[i][j-1]-8,self.table[i-1][j]-8,self.table[i-1][j-1]+self.score_matrix[self.str1[i-1]][self.str2[j-1]])
    return None
  #Use a stack to store where the trace splits, if we have mutiple alignment results. 
  def TraceBack(self,i,j):
    if i==0 and j==0:
      buff_copy = self.buff[:]            #The buff is gonna store the route that has been traced so far
      self.backtrace.append(buff_copy)    #If it hits the origin, means this trace has been done. Append it to the final output.
      if self.check_point:
        temp = self.check_point[-1]       #And pop out the last recorded split-point, if any
        self.check_count[-1] -= 1
        if self.check_count[-1] == 0:
          del self.check_point[-1]
          del self.check_count[-1]
        self.buff = temp[:]
      return 0
    elif i ==0:
      self.buff.append([i,j-1])
      self.TraceBack(i,j-1)
    elif j ==0:
      self.buff.append([i-1,j])
      self.TraceBack(i-1,j)
    else:
      if ((self.table[i-1][j]-8 == self.table[i][j]) + (self.table[i][j-1]-8 == self.table[i][j]) +(self.table[i-1][j-1]+self.score_matrix[self.str1[i-1]][self.str2[j-1]] == self.table[i][j]))>=2:
        count = ((self.table[i-1][j]-8 == self.table[i][j]) + (self.table[i][j-1]-8 == self.table[i][j]) +(self.table[i-1][j-1]+self.score_matrix[self.str1[i-1]][self.str2[j-1]] == self.table[i][j]))
        temp = self.buff[:]
        self.check_point.append(temp)
        self.check_count.append(count-1)
      if self.table[i-1][j]-8 == self.table[i][j]:
        self.buff.append([i-1,j])
        self.TraceBack(i-1,j)  
      if self.table[i][j-1]-8 == self.table[i][j]:
        self.buff.append([i,j-1])
        self.TraceBack(i,j-1)
      if self.table[i-1][j-1]+self.score_matrix[self.str1[i-1]][self.str2[j-1]] == self.table[i][j]:
        self.buff.append([i-1,j-1])
        self.TraceBack(i-1,j-1)
#Calculate the percent identity
def getIdentity(alignments):
  aln1 = alignments[0][0]
  aln2 = alignments[0][1]
  L = len(aln1)
  iden = 0
  for i in range(0,L):
    if aln1[i] == aln2[i]:
      iden +=1
  print('The identity = %3.3f percent' % (float(iden)/L*100))
  return None
#Get the alignments from the trace(s) and print out
def printAlignments(traces,a,b):
  output = []
  for trace in traces:
    print("==================================")
    print("The Alignment:")
    output_A = ""
    output_B = ""
    trace_t = trace[::-1]
    for i in range(1,len(trace_t)):
      if trace_t[i][0]-trace_t[i-1][0] !=0:
        output_A += a[trace_t[i][0]-1]
      else:
        output_A += "_"
      if trace_t[i][1]-trace_t[i-1][1] !=0:
        output_B += b[trace_t[i][1]-1]
      else:
        output_B += "_"
    output.append([output_A, output_B])
    print(output_A)
    print("|"*len(output_A))
    print(output_B)
    print("Alignment length = ",len(output_A))
  print("==================================")
  return output
#Read given PDB file, obtain the protein sequences
def readPDB(fileName):
  sequence = ""
  res_index = 0
  f = open(fileName)
  for line in f:
    temp = line.split()
    if temp[0] == 'ATOM' and int(temp[5])!=res_index:
      sequence += ThreeToOne[temp[3]]   #convert the three-letter to one-letter code
      res_index = int(temp[5])
  f.close()
  return sequence
def main():
  (options, args) = getopt.getopt(sys.argv[1:], 'fbm')
  if not len(args[0]) or not len(args[1]):
    print("============================================|")
    print("Please give two PDB files with valid path !!|")
    print("============================================|")
    return 0
  seq_A = readPDB(args[0])
  seq_B = readPDB(args[1])
  print('-----------------------------')
  print('The first sequence: ', seq_A)
  print('Length = ',len(seq_A))
  print('The second sequence: ',seq_B)
  print('Length = ',len(seq_B))
  print('-----------------------------')
  alignment = NW()
  alignment.initial_table(seq_A,seq_B)
  alignment.Needleman()
  print('             RESULT               ')
  print('=================================')
  print("The alignment score is ",alignment.table[len(seq_A)][len(seq_B)])
  print('=================================')
  alignment.TraceBack(len(seq_A),len(seq_B))
  alignments = printAlignments(alignment.backtrace,seq_A,seq_B)
  print("The total number of final alignments : ", len(alignments))
  getIdentity(alignments)
 
  return 0

if __name__ == "__main__":
    main()