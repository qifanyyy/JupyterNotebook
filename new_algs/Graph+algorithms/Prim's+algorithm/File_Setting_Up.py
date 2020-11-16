from random import shuffle

def PrendiDaFile(grafo,G):

    with open(grafo + '.txt','r') as f:
            p = 0
            b = 0
            c = 0
            g = 0
            nn = []
            pp = []
            
            for line in f:
                line = line.rstrip()
                n = line.split(' ')
                if b == 1:
                    
                    for pesi in xrange(1, int(n[0]) + 1):
                        pp.append(pesi)
                    shuffle(pp) 
                    c = 1
                   
                if p == 1:
                    c = 2

                if c == 0:
                    for i in xrange(0,int(n[0])):
                        nn.append(G.insertNode(i))
                        
                    b = 1
                if c == 1:

                    global e
                    e = int(n[0])
                    b = 0
                    p = 1
                    
                if c == 2:
                    
                    if int(n[0]) != int(n[1]):
                        
                        G.insertArcW(nn[int(n[0])].index,nn[int(n[1])].index, float(pp[g]))
                        G.insertArcW(nn[int(n[1])].index,nn[int(n[0])].index, float(pp[g]))
                    
                    g += 1
                    

