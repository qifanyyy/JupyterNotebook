import Tkinter as tk     # python 2
import tkFont as tkfont  # python 2
from algoritam_i_vizualizacija import*
import copy


a=False
global pairs
pairs=list([])
global objekat 
objekat = PrimovAlgoritam()
global nazad
nazad=True
global br_cvorova
br_cvorova=5
global img,img1,graf,graf1,graf2,graf3


def dek():
    global pairs
    global objekat
    global nazad
    #print('nazad klinuto')
    nazad=False
    pairs=list()
    objekat = PrimovAlgoritam()


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.font = tkfont.Font(family='Helvetica', size=13)

        container = tk.Frame(self,  width=800, height=600, background="white")
        container.pack(side="top", fill="both", expand=True)
        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Pocetna_stranica, Stranica_1, Korak, Unos, Brzina, Animacija):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Pocetna_stranica")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class Pocetna_stranica(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,  background="white")
        self.controller = controller

        global img
        img = tk.PhotoImage(file='etf.png') 
        self.lbl=tk.Label(self, image=img)
        self.lbl.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        
        
        label = tk.Label(self, text="Vizualizacija Primovog algoritma", font=controller.title_font, bg='white')
        label.pack(side="top", fill="x", pady=110, padx=100)
        

        button1 = tk.Button(self, text="Slucajno generisati graf", bg='white')
        button1.bind('<Button 1>', self.generisi_graf)

        button2 = tk.Button(self, text="Rucni unos grafa", command=lambda: controller.show_frame("Unos"), bg='white')

        button1.pack()
        button2.pack()
        self.entry_1 = tk.Entry(self)
        self.entry_1.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        button3 = tk.Button(self, text="OK",  command=lambda: self.broj(), bg='white')
        button3.place(relx=0.7, rely=0.7, anchor=tk.CENTER)


        label_1 = tk.Label(self, text="Broj cvorova:",bg='white' )
        label_1.place(relx=0.27, rely=0.7, anchor=tk.CENTER) 

    def broj(self):
        global br_cvorova
        global objekat
        br_cvorova=int(self.entry_1.get())
        self.entry_1.delete(0, tk.END)
        objekat.setuj_broj_cv(br_cvorova)

    def generisi_graf(self, event):
        global objekat
        objekat.generisi_nasumicni_graf_slova()
        self.controller.show_frame("Stranica_1")

class Stranica_1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background="white")
        self.controller = controller
        label = tk.Label(self, text="Graf je unesen!", font=controller.title_font,bg="white" )
        label.pack(side="top", fill="x", pady=10)

        label_2=tk.Label(self, text="U narednom dijelu omogucena su 2 tipa vizualizacije", font=controller.font,bg="white" )
        label_3=tk.Label(self, text=" i to korak po korak, te animacioni prikaz.", font=controller.font,bg="white" )
        #label_2.pack(side="top", fill="x", pady=5)
        #label_3.pack(side="top", fill="x", pady=5)
        label_2.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        label_3.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        button = tk.Button(self, text="Nazad",
                           command=lambda: (dek(), controller.show_frame("Pocetna_stranica")),bg="white" )
        

        button_1 = tk.Button(self, text="Animacija", command=self.aktivacija, bg="white")
        #button_1.bind('<Button 1>', self.aktivacija)                   
        
        global objekat
        button_2 = tk.Button(self, text="Korak po korak",
                           command=lambda:  (objekat.step_by_step_iter(),controller.show_frame("Korak")),bg="white" )

        button.place(relx=0.335, rely=0.7, anchor=tk.CENTER)                   
        button_1.place(relx=0.47, rely=0.7, anchor=tk.CENTER)
        button_2.place(relx=0.65, rely=0.7, anchor=tk.CENTER)

        global graf1
        graf1 = tk.PhotoImage(file='graf.png') 
        self.lbl=tk.Label(self, image=graf1)
        self.lbl.place(relx=0.1, rely=0.9, anchor=tk.CENTER)

    def aktivacija(self):
        self.controller.show_frame("Brzina")


class Animacija(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background="white")
        self.controller = controller   
        label = tk.Label(self, text="Animacija u toku", font=controller.title_font, background="white")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Nazad na pocetnu stranicu",
                           command=lambda:(dek(), controller.show_frame("Pocetna_stranica")),background="white")
        
        global img1
        img1 = tk.PhotoImage(file='sat1.png')
        self.lbl=tk.Label(self, image=img1)
        self.lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        button.place(relx=0.5, rely=0.87, anchor=tk.CENTER)

class Unos(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background="white")
        self.controller = controller
        #label = tk.Label(self, text="Unos grafa", font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)
        l=tk.Label(self, text="Rucni unos grafa",font=controller.font, background="white") 
        label_1 = tk.Label(self, text="Cvor 1",background="white") 
        label_2 = tk.Label(self, text="Cvor 2",background="white") 
        label_3 = tk.Label(self, text="Tezina",background="white") 

        button3 = tk.Button(self, text="Dalje",background="white")
        button4 = tk.Button(self, text="Ponovni unos", background="white")
        button5 = tk.Button(self, text="Zavrsen unos", command=lambda: self.zavrsen_unos(),background="white" )

        button3.bind('<Button 1>', self.dalje)
        button4.bind('<Button 1>', self.ponovni_unos)

        button3.place(relx=0.31, rely=0.7, anchor=tk.CENTER)
        button4.place(relx=0.46, rely=0.7, anchor=tk.CENTER)
        button5.place(relx=0.65, rely=0.7, anchor=tk.CENTER)

        l.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        label_1.place(relx=0.3, rely=0.2, anchor=tk.CENTER)
        label_2.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
        label_3.place(relx=0.3, rely=0.4, anchor=tk.CENTER) 
        self.entry_1 = tk.Entry(self) 
        self.entry_2 = tk.Entry(self) 
        self.entry_3 = tk.Entry(self)
        self.entry_1.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.entry_2.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        self.entry_3.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        button = tk.Button(self, text="Nazad",
                           command=lambda: controller.show_frame("Pocetna_stranica"),background="white")
        button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        global graf
        graf = tk.PhotoImage(file='graf.png') 
        self.lbl=tk.Label(self, image=graf)
        self.lbl.place(relx=0.1, rely=0.9, anchor=tk.CENTER)

    def zavrsen_unos(self):
        global pairs
        global objekat
        objekat.rucni_unos_grafa(pairs)
        self.controller.show_frame("Stranica_1")

    def dalje(self,event):
        global pairs
        pairs.append([int(self.entry_1.get()),int(self.entry_2.get()),int(self.entry_3.get())])
        self.entry_1.delete(0, tk.END)
        self.entry_2.delete(0, tk.END)
        self.entry_3.delete(0, tk.END)
        print(pairs)
    def ponovni_unos(self,event):
        global pairs
        pairs =list()
        self.entry_1.delete(0, tk.END)
        self.entry_2.delete(0, tk.END)
        self.entry_3.delete(0, tk.END)

class Korak(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="white")
        self.controller = controller
        label = tk.Label(self, text="Vizualizacija korak po korak", font=controller.font, bg="white")
        label.pack(side="top", fill="x", pady=57)
        button = tk.Button(self, text="Nazad na pocetnu stranicu",
                           command=lambda:(dek(), controller.show_frame("Pocetna_stranica")), bg="white")
        
        button_1 = tk.Button(self, text="Sljedeci korak",
                           command=lambda: self.dalje(), bg="white")
        button_1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        global graf3
        graf3 = tk.PhotoImage(file='graf.png') 
        self.lbl=tk.Label(self, image=graf3)
        self.lbl.place(relx=0.1, rely=0.9, anchor=tk.CENTER)

    def dalje(self):
        global objekat
        if(not(objekat.zadnja_iter)):
            objekat.step_by_step_iter()
            
        else:
            dek()
            self.controller.show_frame("Pocetna_stranica")

class Brzina(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background="white")
        self.controller = controller
        label_1 =tk.Label(self, text="Postavka brzine animacije",font=controller.font, background="white")
        label = tk.Label(self, text="Brzina animacije (s)" ,background="white")
        #label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Nazad na pocetnu stranicu", command=lambda: (dek(),controller.show_frame("Pocetna_stranica")),background="white")
        
        button1 = tk.Button(self, text="OK", background="white")
        button1.bind('<Button 1>', self.akt)

        self.entry_1 = tk.Entry(self)
        self.entry_1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        label_1.place(relx=0.5, rely=0.27, anchor=tk.CENTER)
        label.place(relx=0.25, rely=0.4, anchor=tk.CENTER)
        button1.place(relx=0.7, rely=0.4, anchor=tk.CENTER)
        button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        global graf2
        graf2 = tk.PhotoImage(file='graf.png') 
        self.lbl=tk.Label(self, image=graf2)
        self.lbl.place(relx=0.1, rely=0.9, anchor=tk.CENTER)

    def akt(self,event):
        #global objekat
        self.controller.show_frame("Animacija")
        objekat.setuj_brzinu_animacije(int(self.entry_1.get()))
        print("Pauza je ", int(self.entry_1.get()), "s")
        objekat.zapocni_pretragu()
        global nazad
        while (objekat.animacija_u_toku and nazad):
            pass
        nazad=True
        dek()
        self.controller.show_frame("Pocetna_stranica")

if __name__ == "__main__":

    #objekat.generisi_nasumicni_graf_slova()
    app = SampleApp()
    app.mainloop()