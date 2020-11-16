import os

class SmithWater():
        
    def _file_check(self, n):
        if (n in os.listdir()):
            return True
        else:
            return False
     
        
    def file_names(self):
        "STEP 1: Provide a filenames of your sequences\nNO-ARGUMENT METHOD"
        
        print("==================================================")
        print("  The following object creates a local alignment")
        print("      based on Smith-Waterman algorithm")
        print("==================================================\n")
        
        while(True):
            check = 0
            print("Set working directory by typing a path:")
            path  = input()
            
            try:
                os.chdir(path)
                check = 1
                
            except FileNotFoundError:
                print("There is no such directory!")
                check = 0
                
            if check == 1:
                break;
            
        print("\nPlease make sure the FASTA files of your interest") 
        print("are in following directory")
        print(os.getcwd())
        
        print("\nType 1 if both sequences are in one FASTA file")
        print("Type 2 if the sequences are in two separate files")
        
        while(True):
            again = 1
            while(again == 1):
                self._answer = input()
                try:
                    self._answer = int(self._answer)
                    again = 0  
                except ValueError:
                   again = 1
                   print("Wrong! Choose either 1 or 2!")
                    
            if (self._answer != 1 and self._answer != 2):
                print("Wrong number!")
                
            elif (self._answer == 1 or self._answer == 2):
                break
            
        if (self._answer == 1):
            print("Provide the name of FASTA file")
            
            while(True):
                self._file_name = input()
                cond = self._file_check(self._file_name)  
                if cond == True:
                    break
                
                else:
                    print("ERROR! There is no such file!")
        
        if (self._answer == 2):
            print("Provide the name of the 1st FASTA file:")
            while(True):
                self._file_name_1 = input()
                
                cond = self._file_check(self._file_name_1)
                if (cond == True):
                    break
                elif (cond == False):
                    print("ERROR! There is no such file!")
                
            print("Provide the name of the 2nd FASTA fila:")
            
            check = 0
            while(True):
                self._file_name_2 = input()
                
                if (self._file_name_1 == self._file_name_2 and check == 0):
                    print("The filenames are the same!")
                    print ("Please re-type the name of the 2nd file!")
                    check = 1
                    
                cond = self._file_check(self._file_name_2)
               
                if(cond == True and check == 0):
                    break
                
                elif (cond == True and check == 1):
                    check = 0
                
                elif (cond == False and check == 0):
                    print("ERROR! There is no such file!")
                    
                else:
                    check = 0
                    
        self._seq1 = ""
        self._seq1_name = ""
        self._seq2 = ""
        self._seq2_name = ""   


    def reading(self):
        "STEP 2: Read sequences from the files\nNO-ARGUMENT METHOD"
        
        if (self._answer == 1):
            fp = open(self._file_name, "r")
            seq0 = fp.read()  
            fp.close()
            
            headers = ([pos for pos, char in enumerate(seq0) if char == ">"])
            
            self._seq1 = seq0[headers[0]:headers[1]]
            self._seq2 = seq0[headers[1]:]
            
            #remove blank characters if the sequence contains so
            for i in self._seq1:
                if (i != "\n"):
                    self._seq1_name = self._seq1_name + i
                else:
                    break
            self._seq1_name = self._seq1_name[1:]  
            
            for i in self._seq2:
                if (i != "\n"):
                    self._seq2_name = self._seq2_name + i   
                else:
                    break  
            self._seq2_name = self._seq2_name[1:]
            
            rm_header_1 = seq0[len(self._seq1_name)+1:headers[1]] #remove headers
            rm_header_2 = seq0[headers[1]+len(self._seq2_name)+1:] #remove headers
            
            self._seq1 = rm_header_1.replace("\n", "")
            self._seq2 = rm_header_2.replace("\n", "")
            
            
            print ("Original sequences: ")
            print (self._seq2_name)
            print (self._seq2, "\n")
            
            print(self._seq1_name)
            print(self._seq1)
            
            _rev1 = ReverseComplement(self._seq1)
            _rev2 = ReverseComplement(self._seq2)
            
            print("\nReverse complements: ")
            
            _seq1_rev = ""
            for i in _rev1:
                _seq1_rev += i
                
            
            _seq2_rev = ""
            for j in _rev2:
                _seq2_rev += j
                
                
            print ("\n", self._seq2_name)
            print (_seq2_rev, "\n")
            
            print(self._seq1_name)
            print(_seq1_rev)
            
            
        if (self._answer == 2):
            fp = open(self._file_name_1, "r")
            self._seq1 = fp.read()  
            fp.close()
            
            fp = open(self._file_name_2, "r")
            self._seq2 = fp.read()
            fp.close()
            
            new_line1 = self._seq1.find("\n")
            new_line2 = self._seq2.find("\n")
            self._seq1_name = self._seq1[0:new_line1] 
            self._seq2_name = self._seq2[0:new_line2]
            
            self._seq1 = self._seq1[new_line1:]
            self._seq1 = self._seq1.replace("\n", "")   #trimming
            
            self._seq2 = self._seq2[new_line2:]
            self._seq2 = self._seq2.replace("\n", "")
            
            print ("Original sequences: ")
            print ("\n", self._seq2_name)
            print (self._seq2, "\n")
            
            print(self._seq1_name)
            print(self._seq1)
            
            _rev1 = ReverseComplement(self._seq1)
            _rev2 = ReverseComplement(self._seq2)
            
            print("\nReverse complements: ")
            
            _seq1_rev = ""
            for i in _rev1:
                _seq1_rev += i
                
            _seq2_rev = ""
            for j in _rev2:
                _seq2_rev += j
                     
            print ("\n", self._seq2_name)
            print (_seq2_rev, "\n")
            
            print(self._seq1_name)
            print(_seq1_rev)
        

    def local_alignmet(self):       #create matrix for Smith and Waterman alignment
        "STEP 3: Create a local alignment and find the best one\nNO-ARGUMENT METHOD"
        
        self._full_seq_1 = self._seq1
        self._full_seq_2 = self._seq2
         
        #matrix of local alignment (scores)
        matrix_sw = [[0 for j in range(len(self._full_seq_2)+2)] for i in range(len(self._full_seq_1)+2)]
        
        #matrix of where-i-have-came-from values
        self._matrix_path = [[0 for j in range(len(self._full_seq_2)+2)] for i in range(len(self._full_seq_1)+2)]
        
        i = 2
        for char in self._full_seq_1:
            matrix_sw[i][0] = char
            self._matrix_path[i][0] = char
            i = i+1
         
        j = 2      
        for char in self._full_seq_2:
            matrix_sw[0][j] = char
            self._matrix_path[0][j] = char
            j = j+1
        
        
        #dynamic programming algorithm
        match = 2
        mismatch = -1
        gap = -1
        l_bound = 0
        
        backup = []
        
        for i in range(2, len(self._full_seq_1)+2):
            for j in range(2, len(self._full_seq_2)+2):
                val = []
                nt1 = matrix_sw[i][0] #take two nucleotides
                nt2 = matrix_sw[0][j]
                
                if nt1 == nt2:          #make a comparison
                    score = match
                    temp=[i,j]
                    backup.append(temp) #prepare stuff for further evaluation
                    
                elif nt1 != nt2:
                    score = mismatch
                
                v1 = matrix_sw[i-1][j-1] + score
                v2 = matrix_sw[i-1][j] + gap
                v3 = matrix_sw[i][j-1] + gap
                v4 = l_bound
                
                val = [v1, v2, v3, v4]
                
                cell = max(val) #take max from 4 values
                
                if cell == v1 and cell != 0:    #if the score comes from given value...
                    where = "z"                 #... then put specific letter in the path matrix
                elif cell == v2 and cell != 0:  
                    where = "y"
                elif cell == v3 and cell != 0:
                    where = "x"
                elif cell == v4:
                    where = "0"
                
                matrix_sw[i][j] = cell
                self._matrix_path[i][j] = where   
              
                
        for k in backup:
            i = k[0]
            j=k[1]
            k.insert(0, matrix_sw[i][j]) #extend list of all matches by a score in sw_matrix from that position
            
        backup.sort(reverse = True)
        
        value = backup[0][0]
        
        reps = 0
        for i in backup:            #how many times the highest value has been repeated
            if i[0] != value:
                break
            reps = reps+1

        
        self._list_of_best = []
        self._index_l = 0
        #create the alignment
        for element in backup:
            i = element[1]
            j = element[2]
            
            align_seq1 = []
            align_seq2 = []
            
            for char in self._full_seq_1:
                align_seq1.append(char)
                
            for char in self._full_seq_2:
                align_seq2.append(char)    
            
            cond = True    
            while(cond):
                letter = self._matrix_path[i][j]
        
                if letter == "x":
                    align_seq1.insert(j-2, "-")
                    j = j-1
                    #print("Going left")
                    
                if letter == "y":
                    align_seq2.insert(i-2, "-")
                    i = i-1
                    #print("Going up")
                    
                if letter == "z":
                    i = i-1
                    j = j-1
                    #print("Going corner")
                    
                if letter == "0" or letter == 0:
                    #print("End")              
                    break
        
            to_second = i-2 
            to_first = j-2
                
            if to_second < 0:
                to_second = 0
        
            if to_first < 0:
                to_first = 0
                
            for i in range(to_first):
                align_seq1.insert(0, " ")
                
            for i in range(to_second):
                align_seq2.insert(0, " ")
                
            seq1 = ""
            seq2 = ""
            
            for i in align_seq1:
                seq1 = seq1+i
                
            for i in align_seq2:
                seq2 = seq2+i    
                
            longest = max(len(align_seq1),len(align_seq2))
            sep = ""
            
            for i in range(longest):
                try:
                    nt1 = seq1[i]
                except IndexError:
                    nt1 = "(" #just random character
                    
                try:       
                    nt2 = seq2[i]
                except IndexError:
                    nt1 = ")" #same here
                        
                if (nt1 == nt2 and (nt1 != " " and nt1 != " ")):
                    sep = sep + "|"
            
                    
                elif (nt1 == nt2 and nt1 == " "):
                    sep = sep + " "
        
                elif (nt1 != nt2):
                    sep = sep + " "
                    
            
            #the following bits of code trims blank characters if are founded in both sequences
            #at the same position
            cond = True
            z = 0
            while (cond):
                if (seq1[z] == seq2[z] and (seq1[z] == " " and seq2[z])):
                    seq1 = seq1[1:]
                    seq2 = seq2[1:]
                    sep  = sep[1:]
                    
                else:
                    cond = False
                
                if cond != False:    
                    z = z+1
                    
                    
            tot_length = len(seq1) + len(seq2)
            scoring_line = ""
            
            score = 0
            for i in range(tot_length): #at most sum-of-the-sequences-number of iterations
                try:
                    nt1 = seq1[i]
                except IndexError:
                    break
            
                try:
                    nt2 = seq2[i]
                except IndexError:
                    break
                
                if nt1 in "ACTG-" and nt2 in "ACTG-": #local alignemnt, not global! therefore we're interesting in algin sequences only
                    if nt1 == nt2:                  #if there was a match
                        scoring_line = scoring_line + "+"
                        score = score + match
                        
                    if nt1 != nt2 and (nt1 in "ACTG" and nt2 in "ACTG"): #if there was a mismatch
                        scoring_line = scoring_line + "-"    
                        score = score + mismatch
                        
                    if nt1 != nt2 and (nt1 in "-" and nt2 in "ACTG"):
                        scoring_line = scoring_line + "-"  
                        score = score + mismatch
                        
                    if nt1 != nt2 and (nt1 in "ACTG" and nt2 in "-"):   
                        scoring_line = scoring_line + "-"
                        score = score + gap
       
                else:
                    scoring_line = " "
                
            max_score = str(score)                
                    
            if "|" in sep: #take only align sequences, discard those with no match    
                n_l = "\n"
        
                self._full = self._seq1_name + n_l + seq1 + n_l + sep + n_l + seq2 + n_l + scoring_line + n_l + self._seq2_name + n_l + "total score: " +  max_score + " \n" +("="*(longest+5)) + n_l
                

                

    def save_results(self, file_name):
        "STEP 5: Save results of S-W algorithm into a file\nARGUMENT: string\nexample: \"file_name.txt\""
        f = open(file_name, "a")
        f.write(self._full)
        f.close()      
    

class ReverseComplement(object):
    
    #the class is an implementation of the iterator it takes back reverse complement of the input sequence
    
    def __init__(self, DNA_sequence):
        self.upper_bound = len(DNA_sequence)
        self.full_seq = DNA_sequence
     
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.upper_bound == 0:
            raise StopIteration
            
        self.upper_bound = self.upper_bound - 1
        
        if self.full_seq[self.upper_bound] == "A":
            return "T"
        
        if self.full_seq[self.upper_bound] == "T":
            return "A"
        
        if self.full_seq[self.upper_bound] == "C":
            return "G"
        
        if self.full_seq[self.upper_bound] == "G":
            return "C"