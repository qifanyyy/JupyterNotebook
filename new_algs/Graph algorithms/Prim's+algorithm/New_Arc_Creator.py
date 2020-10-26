import Graph_AdjacencyList
from tkMessageBox import *
import time
'''
* Checking for connected components:
* max_cc(G,G1) call simpleSearch to verify if the graph is connected. 
* If it isn't, iterative version of connect component function find the biggest connected component.
'''

def max_cc(G,G1):

    l = G.simpleSearch(0)                     
    if len(l) == len(G.nodes.keys()):         
        print 'The Graph is connected'        
        return 1, 0
    else:
        instant = time.time()
        showinfo('GrafoInfo',"Il grafo non e' connesso, verra' estratta la componente connessa piu' grande ed eseguito l'algoritmo di Prim. E' possibile controllare l'avanzamento da terminale. La finestra verra' chiusa automaticamente al termine dell'esecuzione.")
        elapsed = time.time() - instant
        print ''
        print ''
        print 'Estrazione componente connessa maggiore'
        print ''
        print ''
        c = 0
        h = 1
        n1 = len(G.nodes.keys())-1
        for i in G.nodes.keys():
        
            if not i in l:
                
                l1 = G.simpleSearch(i)
                if len(l1) > len(l):
                    
                    l = l1
            
            if c == 100*h:
                prog = 100*float(G.nodes.keys().index(i))/float(n1) 
                print round(prog,2), '%'
                h += 1
            c += 1
        BuildGraph(G,G1,l)
        return 0, elapsed
        

def BuildGraph(G,G1,l):
    n = len(l)-1
    print ''
    print 'Costruzione nuovo grafo'
    print ''
    c = 0
    h = 1
    for i in l:
        
        G1.insertNode(i)
        curr = G.adj[i].getFirstRecord()
        while curr != None:
            peso = curr.next
            G1.insertArcW(i,curr.elem,peso.elem)
            G1.insertArcW(curr.elem,i,peso.elem)
            curr = curr.next
            curr = curr.next
        
        if c == 100*h or i == l[n]:
            prog = 100*float(l.index(i))/float(n) 
            print round(prog,2), '%'
            h += 1
        c += 1
        

            

    








