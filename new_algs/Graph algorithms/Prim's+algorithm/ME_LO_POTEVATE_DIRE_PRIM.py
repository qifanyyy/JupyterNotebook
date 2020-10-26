import Tkinter as tk
from Tkinter import tkinter,Tk, Label, Button, Menu, StringVar, IntVar, Spinbox, BOTH, LEFT, ACTIVE, Text, W
from ttk import Style, Frame
from File_Setting_Up import PrendiDaFile
import Graph_AdjacencyList
import tkFileDialog
from tkSimpleDialog import askinteger
import Tkconstants
import cProfile , pstats
from tkMessageBox import showinfo
import tkMessageBox
import time
from tkMessageBox import *


class App(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self,master)
        
        self.m = master
        self.initUI()
        
    
    def initUI(self):
        
       
        
        self.m.title("Me lo potevate dire Prim!")
        self.pack(fill=BOTH,expand=1)
        
        
        style = Style()
        style.configure("TFrame", highlightbackground='#389')
        
        self.img = tk.PhotoImage(file = "geo.gif")
        label = Label(self,image=self.img,background='white')
        label.image = self.img
        label.place(x=400,y=180)
        
        
        label3 = Label(self, text = "Selezionare il grafo e la struttura dati dalla", font = "Verdana 14 bold")
        label3.place(x=50,y=300)
        
        label6 = Label(self, text = "barra dei menu' e premere Execute prim.", font = "Verdana 14 bold")
        label6.place(x=50,y=330)
        
        label4 = Label(self, text = "Sono disponibili due grafi di prova", font = "Verdana 14 bold")
        label4.place(x=50,y=360)
        
        label7 = Label(self, text = "per valutare la correttezza dell'algoritmo.", font = "Verdana 14 bold")
        label7.place(x=50,y=390)
        
        
        
        self.m.title('Me lo potevate dire Prim!')
        menubar = Menu(self.m)
        self.m.config(menu=menubar)
        
        self.fileMenu = Menu(menubar)
     
        self.fileMenu.add_command(label='grafo_wordnet (1,7 MB)',command =lambda: self.a('grafo_wordnet (1,7 MB)',v,l1))
        self.fileMenu.add_command(label='grafo_AS (688,1 kB)',command =lambda: self.a('grafo_AS (688,1 kB)',v,l1))
        self.fileMenu.add_command(label='grafo_DutchElite (55,1 kB)',command =lambda: self.a('grafo_DutchElite (55,1 kB)',v,l1))
        self.fileMenu.add_command(label='grafo_Prova_Connesso',command =lambda: self.a('grafo_Prova_Connesso',v,l1))
        self.fileMenu.add_command(label='grafo_Prova_Non_Connesso',command =lambda: self.a('grafo_Prova_Non_Connesso',v,l1))
        self.fileMenu.add_command(label='grafo_DIC28 (1,1 MB)',command =lambda: self.a('grafo_DIC28 (1,1 MB)',v,l1))
        self.fileMenu.add_command(label='grafo_eatRS (3,9 MB)',command =lambda: self.a('grafo_eatRS (3,9 MB)',v,l1))
        self.fileMenu.add_command(label='grafo_email (94 kB)',command =lambda: self.a('grafo_email (94 kB)',v,l1))
        self.fileMenu.add_command(label='grafo_foldoc (1,4 MB)',command =lambda: self.a('grafo_foldoc (1,4 MB)',v,l1))
        self.fileMenu.add_command(label='grafo_PairsP (754 kB)',command =lambda: self.a('grafo_PairsP (754 kB)',v,l1))
        self.fileMenu.add_command(label='grafo_PGP (263 kB)',command =lambda: self.a('grafo_PGP (263 kB)',v,l1))
        self.fileMenu.add_command(label='grafo_Yeast (70 kB)',command =lambda: self.a('grafo_Yeast (70 kB)',v,l1))
        self.fileMenu.add_command(label='grafo_USpowerGrid (139 kB)',command =lambda: self.a('grafo_USpowerGrid (139 kB)',v,l1))
        menubar.add_cascade(label='GRAFI',menu=self.fileMenu)
        
        self.fileMenu2 = Menu(menubar)
        menubar.add_cascade(label='STRUTTURE DATI',menu=self.fileMenu2)
        self.fileMenu2.add_command(label='PQ_DHeap',command =lambda: self.b('PQ_DHeap',u,l2,v))
        self.fileMenu2.add_command(label='PQbinaryHeap',command =lambda: self.b('PQbinaryHeap',u,l2,v))
        self.fileMenu2.add_command(label='PQbinomialHeap',command =lambda: self.b('PQbinomialHeap',u,l2,v))
        
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'Selezionare un file'
        
        
        
        
            
        v = StringVar()
        l1 = Label(self.m,background = 'white',textvariable=v,font = "Verdana 14 bold")
        v.set('')
        l1.place(x=100,y=100)
        
        u =StringVar()
        l2 = Label(self.m,background = 'white',textvariable=u,font = "Verdana 14 bold") 
        u.set('')
        l2.place(x=100,y=130)
        
        
        
       
    def creaSpinbox(self):
        c = askinteger('Inserisci D tra : ' , '2,3,4,5,7,8,11')
        if c != 2 and c != 3 and c != 4 and c != 5 and c != 11 and c != 7 and c != 8 and c != None:
            d = tkMessageBox.askokcancel('Errore!', 'Scegliere un valore tra quelli indicati', type = "ok" )
            if d == True:
                return self.creaSpinbox()
            
                
        return c
   
        
    def a(self,i,v,l1):
        
        v.set(i)
    
    def b(self,p,u,l2,v):
        
        u.set(p)
        if p == 'PQ_DHeap':
            c = self.creaSpinbox()
        else:
            c = 0
      
        button1 = Button(self.m, text = 'Esegui Prim', command = lambda: self.avvio(v,u,c))
        button1.place(x=100,y=200)
        
    def close(self):
        self.quit()
    
    def aaskopenfile(self):
        filename = tkFileDialog.asksaveasfilename( **self.file_opt)
        if filename:
            return filename
        return None
        

             
    def avvio(self,v,u,c):
        global F
        gph = v.get()
        data = u.get()
        if not gph:
            t = tkMessageBox.askokcancel('Errore!', "Non e' stato selezionato il grafo!", type = "ok") 
            if t == True:
                return
        elif c == None:
            t = tkMessageBox.askokcancel('Errore!', "Non e' stato scelto il valore per il D Heap!", type = "ok")
            if t == True:
                c = self.creaSpinbox()
        label5 = Label(self, text = "Elaborazione in corso...", font = "Verdana 14 bold")
        label5.place(x=300,y=50)
        F = self.aaskopenfile() 
        if F == None:
            return
        else:
            
            Graph_AdjacencyList.main(gph, data, F, c)
            showinfo("Me lo potevate dire Prim!","Operazione Completata! Sono stati creati due file nella directory selezionata: uno per il MST e l'altro per il profiling.")
            App.close(self)
            
            
           

if __name__ == '__main__':
       
    root = Tk()
    root.resizable(0, 0)
    ws = 800
    hs = 600
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    x = (w/2) - (ws/2)
    y = (h/2) - (hs/2)
    root.geometry('%dx%d+%d+%d'%(800,600,x,y))
    app = App(root)
    
    profile = cProfile.Profile()
    profile.run("root.mainloop()")
    newf = F.replace('.txt', '')
    profile.dump_stats(newf + " cProfile.txt")
    out = open(newf + " Stats" + ".txt", "w")
    s = pstats.Stats(newf + " cProfile.txt" , stream = out)
    s.strip_dirs().sort_stats("time").print_stats()    
    out.close()
    
