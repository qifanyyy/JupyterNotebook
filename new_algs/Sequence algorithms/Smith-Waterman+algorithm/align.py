import sys, SmithWaterman, string


#get filenames from command line args
firstSequence = sys.argv[1]
secondSequence = sys.argv[2]
sequence=['']*2

#parse fasta file and strip header info.
def parse_fasta(fasta): 
        sequences=''
        sep=''
        with open(fasta) as f:
                        next(f)
                        for line in f:
                                
                                        sequences += (line.strip())
        return sequences
    
    
sequence[0]= parse_fasta(firstSequence)
sequence[1]= parse_fasta(secondSequence)

#run the algorithm
SmithWaterman.calculateAlignment(sequence[0], sequence[1])