from DoubleLinkedList import ListaDoppiamenteCollegata as Lista
from elements import Node
from File_Setting_Up import PrendiDaFile
from Algoritmo_Prim import MST
import time
import tkSimpleDialog
from File_Setting_Up import PrendiDaFile
from LinkedList import ListaCollegata
from tkMessageBox import *
from New_Arc_Creator import max_cc

class DFSinfo:
    def __init__(self):
        self.t=0
        self.pre=dict()
        self.post=dict()
    
    def stampa(self):
        print ("Preorder numbering")
        for i,p in self.pre.iteritems():
            print (i,":",p)
        print ("Postorder numbering")
        for i,p in self.post.iteritems():
            print (i,":",p)

class GraphAdjacencyList:
    def __init__(self):
        self.nodes = None
        self.adj = None
        self.nextId = 0
        self.weight = 0.0
        
        
    def isAdj(self, tail, head):
        if not head in self.nodes or not tail in self.nodes:
            return False
        
        curr = self.adj[tail].getFirstRecord()
        while curr != None:
            a = curr.elem
            if a == head:
                return True
            curr = curr.next
        
        return False
    
    def insertNode(self, e):
        newnode = Node(self.nextId, e)
        self.nextId += 1
        if self.nodes == None:
            self.nodes = {newnode.elem : newnode}
            self.adj = {newnode.elem : Lista()}
        else:
            self.nodes[newnode.elem] = newnode
            self.adj[newnode.elem] = Lista()
        
        return newnode

    def deleteNode(self, index):
        
        try:
            del self.nodes[index]
            del self.adj[index]
        except KeyError:
            pass
        
        # Controlla TUTTE le liste di adiacenza e cancella gli archi che puntano al nodo eliminato.
        
        for adj in self.adj.itervalues():
            if isinstance(adj,int):
                curr = adj.getFirstRecord()
                while curr != None:
                    if curr.elem == index:
                        adj.deleteRecord(curr)
                    curr = curr.next
    
    def insertArc(self, tail, head):
        if head in self.nodes and tail in self.nodes:
            self.adj[tail].addAsLast(head)

            
    def insertArcW(self, tail, head, weight):
        if head in self.nodes and tail in self.nodes:
            self.adj[tail].addAsLast(head)
            self.adj[tail].addAsLast(weight)
            
    def deleteArcW(self, tail, head, weight):
        if head in self.nodes and tail in self.nodes:
            curr = self.adj[tail].getFirstRecord()
            while curr != None:
                if curr.elem == head:
                    self.adj[tail].deleteRecord(curr)
                    self.adj[tail].popLast()
                curr=curr.next
    
    def deleteArc(self, tail, head):
        if head in self.nodes and tail in self.nodes:
            curr = self.adj[tail].getFirstRecord()
            while curr != None:
                if curr.elem == head:
                    self.adj[tail].deleteRecord(curr)
                curr=curr.next
    
    def simpleSearch(self, root): 
        if root not in self.nodes:
            return
        
        #state of node at the beginning 
        state = dict()
        
        state[root] = 1  # open node if = 1
        #if a node index is not in the dictionary, as a key, it means its state is 'waiting'.
        #If nodes have consecutive ids starting from 0 and no node has been delete, you can use an array
        # of n elements, where n is the number of nodes, initializing its cells to 0, meaning 'waiting'.
        
        nodesVisited = [] #ordered list of visitated nodes
        s = set()
        s.add(root)
        
        while len(s) > 0:
            # random pop
            currind = s.pop()
            if isinstance(currind,int):

                state[currind] = -1  # closed state

                nodesVisited.append(self.nodes[currind])
                curr = self.adj[currind].getFirstRecord()
            
                while curr != None:
                    a = curr.elem
                    # Insert neigh. only if is a node in waiting state.
                    if a not in state:
                        state[a] = 1 #open
                        s.add(a)
                    curr = curr.next
                    if isinstance(curr,int):
                        continue
                    else:
                        curr = curr.next
        a = []
        for x in nodesVisited:
            a.append(x.index)

        return a

    def dfs(self):
        dfsInfo=DFSinfo()
        
        for v in G.nodes.iterkeys():
            
            if v not in dfsInfo.pre:
                self.DFSrec(v,dfsInfo)
        return dfsInfo
    
    def DFSrec(self,v,dfsInfo):
        dfsInfo.t+=1
        dfsInfo.pre[v]=dfsInfo.t
        
        curr = self.adj[v].getFirstRecord()
        while curr != None:
            if curr.elem not in dfsInfo.pre:
                self.DFSrec(curr.elem,dfsInfo)
            curr = curr.next
        
        dfsInfo.t+=1
        dfsInfo.post[v]=dfsInfo.t
        
    
    
    def stampa(self):
        for p in self.adj.iteritems():
            print (str(p[0]) + ":")
            l = p[1]
            if l.first == None:
                print ("[]")
            else:
                s = "["
                current = l.first
                while current != None:
                    if len(s) > 1:
                        s += ", "
                    s += "(" + str(current.elem)+ ")"
                    current = current.next
                s += "]"
                print (s)
    def stampa_dict(self):
        d = {}
        for p in self.adj.iteritems():
            lo = []
            l = p[1]
            current = l.first
            while current != None:
                lo.append(current.elem)
                current = current.next
                current = current.next
            d[p[0]] = lo
        
        return d
        
    def stampasufile(self, out_file):
        for p in self.adj.iteritems():
            out_file.write(str(p[0]) + ": \n")
            l = p[1]
            if l.first == None:
                out_file.write("[] \n")
            else:
                s = "["
                current = l.first
                while current != None:
                    if len(s) > 1:
                        s += ", "
                    s += "(" + str(current.elem)+ ")"
                    current = current.next
                s += "] \n \n"
                out_file.write(s)
    
    
def main(q,l, F, c):
        
        global G
        
        start = time.time()

        G1 =  GraphAdjacencyList()

        
        G =  GraphAdjacencyList()
        
        PrendiDaFile(q,G)
                    
        s, elapsed2 = max_cc(G,G1)
        
        if s == 1:
           
            instant = time.time()
            showinfo("GrafoInfo","Il Grafo e' connesso, avvio l'esecuzione dell'algoritmo di Prim. E' possibile controllare l'avanzamento da terminale. La finestra verra' chiusa automaticamente al termine dell'esecuzione.")
            elapsed = time.time() - instant
            w, mst, d = MST.prim(G, 0, l,c)                             
            end = time.time() - elapsed - start
            end2 = round(end,3)
            print ('tempo impiegato: ', end2, 's')
            print ('Peso totale: ', w)
            out_file = open(str(F), "w")
            if q == 'grafo_Prova_Connesso':
                out_file.write("Grafo utilizzato: \n \n")
                G.stampasufile(out_file)
            out_file.write("Struttura dati utilizzata: " + l + "   ") 
            if l == 'PQ_DHeap':
                out_file.write("D = " + str(d) + "\n")
            out_file.write("Tempo impiegato: "+ str(end2) + " s \n \nPeso totale: " + str(w) + "\n \nMST: \n \n") 
            for elee in mst:
                out_file.write(str(elee)+'\n')
               
            out_file.close()
            
        else:
            
            w , mst, d = MST.prim(G1,G1.nodes.keys()[0], l, c)
            end = time.time() - elapsed2 - start
            end2 = round(end,3)
            print ('tempo impiegato: ', end2, 's')
            print ('Peso totale: ', w)
            out_file = open(str(F), "w")
            if q == 'grafo_Prova_Non_Connesso':
                out_file.write("Componente connessa maggiore: \n \n") 
                G1.stampasufile(out_file)   
            out_file.write("Grafo utilizzato: " + q + "\n" + "Struttura dati utilizzata: " + l + "   ") 
            if l == 'PQ_DHeap':
                out_file.write("D = " + str(d) + "\n")
            out_file.write("Tempo impiegato: "+ str(end2) + " s \n \nPeso totale: " + str(w) + "\n \nMST: \n \n") 
            for elee in mst:
                out_file.write(str(elee)+'\n')
               
            out_file.close()

