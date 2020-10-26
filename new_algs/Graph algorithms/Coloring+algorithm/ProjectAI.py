# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 23:00:07 2019

@author: Gulam Kibria
"""
# Driver Code

from tkinter import *
from tkinter import Canvas
from tkinter import Frame
from tkinter import messagebox
from tkinter.font import Font
from collections import defaultdict
from tkinter.simpledialog import askstring
import time

root = Tk()
x1=[0]*100
b1 =[0]*100
r1 =[0]*100
g1 =[0]*100
ff1 =[0]*20   #1,2,3,4,5,6,7,8,9,10,11
deg=[0]*20
ff1[10]=0.1

def exitt():
    root.destroy()
    
def addeg(x,g):
    deg[ord(x[0])-65]+=1
    deg[ord(x[1])-65]+=1
    g.graph[ord(x[0])-65][ord(x[1])-65]=1
    g.graph[ord(x[1])-65][ord(x[0])-65]=1
    
def play():
    for i in range(0,20):
        deg[i]=0
        
    g = Graph(9)
    for x in range(9):
            for y in  range(9):
                g.graph[x].append(0) 
                
    gc=[('A','B'),('A','D'),('A','E'),('B','C'),('B','E'),('B','F'),('C','F'),('D','E'),('D','G'),('D','H'),('E','F'),('E','H'),('E','I'),('F','I'),('G','H'),('H','I')]
    for x in gc:
        addeg(x,g)
        
    if (ff1[2]==0):
        Mnumber = askstring('Colour Number', 'Please Enter Your Colour Number for Graph Coloring')
        ff1[2]=int(Mnumber)
        
    ff1[10]=ff1[11].get()
    m = ff1[2]
    g.graphColouring(m)
    
def reset():
        if (ff1[1]==0):
            for l in range(10):
                    canvas.itemconfig(x1[l],fill="white")
                    canvas.itemconfig(r1[l],fill="white")
                    canvas.itemconfig(g1[l],fill="white")
                    canvas.itemconfig(b1[l],fill="white")
                    canvas.update()
            ff1[10]=ff1[11].get()
        elif (ff1[1]==1 or ff1[3]==1 or ff1[4]==1):
            for l in range(10):
                        canvas.itemconfig(x1[l],fill="white")
                        canvas.itemconfig(r1[l],fill="red")
                        canvas.itemconfig(g1[l],fill="green")
                        canvas.itemconfig(b1[l],fill="blue")
                        canvas.update()
            ff1[10]=ff1[11].get()
            if (ff1[3]==1):
                ff1[6]=ff1[7]=0
                ff1[4]=ff1[5]=0
            elif(ff1[4]==1):
                ff1[8]=ff1[9]=0
                ff1[3]=ff1[5]=0
            elif(ff1[5]==1):
                ff1[3]=ff1[4]=0
                
                        
def Change_Number_Colour():
        Mnumber = askstring('Change Colour Number', 'Previous colour number is -> "'+str(ff1[2])+'" If You Change your Colour Number Then Please Enter Your New Colour Number for Graph Coloring')
        ff1[2]=int(Mnumber)
        reset()

def selected1():
     if j.get()==4:
        for l in range(10):
                canvas.itemconfig(x1[l],fill="white")
                canvas.itemconfig(r1[l],fill="white")
                canvas.itemconfig(g1[l],fill="white")
                canvas.itemconfig(b1[l],fill="white")
                canvas.update()
        ff1[1]=0
        ff1[10]=ff1[11].get()
     elif j.get()==5:
        for l in range(10):
                canvas.itemconfig(x1[l],fill="white")
                canvas.itemconfig(r1[l],fill="white")
                canvas.itemconfig(g1[l],fill="white")
                canvas.itemconfig(b1[l],fill="white")
                canvas.update()
        r1[7] = canvas.create_oval(110, 95, 95, 80, fill="red",width=0)
        r1[8]= canvas.create_oval(210, 95, 195, 80, fill="red" ,width=0)
        r1[9] = canvas.create_oval(310, 95, 295, 80, fill="red",width=0)
        r1[4] = canvas.create_oval(110, 195, 95, 180, fill="red",width=0)
        r1[5] = canvas.create_oval(210, 195, 195, 180, fill="red",width=0)
        r1[6] = canvas.create_oval(310, 195, 295, 180, fill="red",width=0)
        r1[1] = canvas.create_oval(110, 295, 95, 280, fill="red",width=0)
        r1[2] = canvas.create_oval(210, 295, 195, 280, fill="red",width=0)
        r1[3] = canvas.create_oval(310, 295, 295, 280, fill="red",width=0)
        
        g1[7] = canvas.create_oval(103, 110, 88, 95, fill="green",width=0)
        g1[8]= canvas.create_oval(203, 110, 188, 95, fill="green",width=0)
        g1[9] = canvas.create_oval(303, 110, 288, 95, fill="green",width=0)
        g1[4] = canvas.create_oval(103, 210, 88, 195, fill="green",width=0)
        g1[5] = canvas.create_oval(203, 210, 188, 195, fill="green",width=0)
        g1[6] = canvas.create_oval(303, 210, 288, 195, fill="green",width=0)
        g1[1] = canvas.create_oval(103, 310, 88, 295, fill="green",width=0)
        g1[2] = canvas.create_oval(203, 310, 188, 295, fill="green",width=0)
        g1[3] = canvas.create_oval(303, 310, 288, 295, fill="green",width=0)
        
        b1[7] = canvas.create_oval(95, 95, 80, 80, fill="blue",width=0)
        b1[8]= canvas.create_oval(195, 95, 180, 80, fill="blue",width=0)
        b1[9] = canvas.create_oval(295, 95, 280, 80, fill="blue",width=0)
        b1[4] = canvas.create_oval(95, 195, 80, 180, fill="blue",width=0)
        b1[5] = canvas.create_oval(195, 195, 180, 180, fill="blue",width=0)
        b1[6] = canvas.create_oval(295, 195, 280, 180, fill="blue",width=0)
        b1[1] = canvas.create_oval(95, 295, 80, 280, fill="blue",width=0)
        b1[2] = canvas.create_oval(195, 295, 180, 280, fill="blue",width=0)
        b1[3] = canvas.create_oval(295, 295, 280, 280, fill="blue",width=0)
        ff1[1] = 1
        ff1[10]=ff1[11].get()
        if (ff1[3]==1):
                ff1[6]=ff1[7]=0
                ff1[4]=ff1[5]=0
        elif(ff1[4]==1):
                ff1[8]=ff1[9]=0
                ff1[3]=ff1[5]=0
        elif(ff1[5]==1):
                ff1[3]=ff1[4]=0

def selected():
     if i.get()==1:
        ff1[5]=1
        ff1[3]=0
        ff1[4]=0
        ff1[10]=ff1[11].get()
        for l in range(10):
                        canvas.itemconfig(x1[l],fill="white")
                        canvas.itemconfig(r1[l],fill="red")
                        canvas.itemconfig(g1[l],fill="green")
                        canvas.itemconfig(b1[l],fill="blue")
                        canvas.update()
     elif i.get()==2:
        ff1[3]=1
        ff1[4]=0
        ff1[5]=0
        ff1[6]=ff1[7]=0
        ff1[10]=ff1[11].get()
        for l in range(10):
                        canvas.itemconfig(x1[l],fill="white")
                        canvas.itemconfig(r1[l],fill="red")
                        canvas.itemconfig(g1[l],fill="green")
                        canvas.itemconfig(b1[l],fill="blue")
                        canvas.update()
     elif i.get()==3:
         ff1[4]=1
         ff1[3]=0
         ff1[5]=0
         ff1[8]=ff1[9]=0
         ff1[10]=ff1[11].get()
         for l in range(10):
                        canvas.itemconfig(x1[l],fill="white")
                        canvas.itemconfig(r1[l],fill="red")
                        canvas.itemconfig(g1[l],fill="green")
                        canvas.itemconfig(b1[l],fill="blue")
                        canvas.update()
         
root.title("@****************************************Map Coloring****************************************@")
root.geometry("850x650+250+1")
canvas = Canvas(root, width=400, height=400, bg="pink")
frame = Frame(root , height=200, width=200)
frame1 = Frame(root, height=400, width=250)
frame.pack()
frame.place(x=90, y=550)
canvas.pack()
canvas.place(x=40, y=120)
frame1.pack()
frame1.place(x=500, y=121)

photo=PhotoImage(file='bek3.png')
canvas.create_image(0, 0, image=photo, anchor=NW)

x1[1] = canvas.create_oval(120, 320, 70, 270, fill="white", outline="black", width=2)
x1[2] = canvas.create_oval(220, 320, 170, 270, fill="white", outline="black", width=2)
x1[3] = canvas.create_oval(320, 320, 270, 270, fill="white", outline="black", width=2)
x1[4] = canvas.create_oval(120, 220, 70, 170, fill="white", outline="black", width=2)
x1[5] = canvas.create_oval(220, 220, 170, 170, fill="white", outline="black", width=2)
x1[6] = canvas.create_oval(320, 220, 270, 170, fill="white", outline="black", width=2)
x1[7] = canvas.create_oval(120, 120, 70, 70, fill="white", outline="black", width=2)
x1[8] = canvas.create_oval(220, 120, 170, 70, fill="white", outline="black", width=2)
x1[9] = canvas.create_oval(320, 120, 270, 70, fill="white", outline="black", width=2)
# ------------------------------------------------------------------------------
canvas.create_line(120, 95, 170, 95, fill="black", width=2)
canvas.create_line(220, 95, 270, 95, fill="black", width=2)
canvas.create_line(120, 195, 170, 195, fill="black", width=2)
canvas.create_line(220, 195, 270, 195, fill="black", width=2)
canvas.create_line(120, 295, 170, 295, fill="black", width=2)
canvas.create_line(220, 295, 270, 295, fill="black", width=2)
canvas.create_line(95, 120, 95, 170, fill="black", width=2)
canvas.create_line(95, 220, 95, 270, fill="black", width=2)
canvas.create_line(195, 120, 195, 170, fill="black", width=2)
canvas.create_line(195, 220, 195, 270, fill="black", width=2)
canvas.create_line(295, 120, 295, 170, fill="black", width=2)
canvas.create_line(295, 220, 295, 270, fill="black", width=2)
canvas.create_line(180, 115, 115, 180, fill="black", width=2)
canvas.create_line(280, 115, 215, 180, fill="black", width=2)
canvas.create_line(180, 215, 115, 280, fill="black", width=2)
canvas.create_line(280, 215, 215, 280, fill="black", width=2)

f1 = Font(family="Times New Romad", size=18, weight="bold")
f2 = Font(family="Times New Romad", size=12, weight="bold")  
f3 = Font(family="Times New Romad", size=10, weight="bold")

title = Label(frame1, text="Algorithm->>: Backtracking", bg = "firebrick",fg="lightcyan", font=f1).pack(side=TOP)
frame2 = Frame(root, height=200, width=200)
frame2.pack()
frame2.place(x=580, y=375)
title1 = Label(frame2, text="Speed",bg="salmon", fg="navy", font=f1).pack(side=TOP)
s=Scale(frame2,from_=0.1,to=5,bg="lightcyan",orient=HORIZONTAL,length=165,width=7,sliderlength=20,resolution="0.1")
s.pack()
ff1[11]=s

i = IntVar()
j = IntVar()
r11 = Radiobutton(frame1, text="None                        ", value=1, variable=i,font=f2,bg="lightcyan",fg="black",command=selected).pack(side=BOTTOM)
r33 = Radiobutton(frame1, text="MRVwithDegree    ", value=3,font=f2, variable=i,bg="lightcyan",fg="black",command=selected).pack(side=BOTTOM)
r22 = Radiobutton(frame1, text="MRV                         ", value=2, variable=i,font=f2,bg="lightcyan",fg="black",command=selected).pack(side=BOTTOM)
title2 = Label(frame1, text="Ordering:",bg="salmon", fg="navy", font=f1).pack(side=BOTTOM)
r55 = Radiobutton(frame1, text="None                        ", value=4, variable=j,bg="lightcyan",fg="black",font=f2,command=selected1).pack(side=BOTTOM)
r44 = Radiobutton(frame1, text="ForwardChecking", value=5, variable=j,bg="lightcyan",fg="black",font=f2,command=selected1).pack(side=BOTTOM)
j.set(4)
i.set(1)
title1 = Label(frame1, text="Filtering:",bg="salmon", fg="navy", font=f1).pack(side=BOTTOM)
b = Button(frame, text="Reset", bg="green", height=1, width=5,font=f3,command=reset)
b11 = Button(frame, text="Exit", bg="plum1", height=1, width=5,font=f3,command=exitt)
b44 = Button(frame , text="Change Colour Num..", bg="Purple",fg="lightcyan", height=1, width=17,font=f3,command=Change_Number_Colour)
b33 = Button(frame, text="Play", bg="green", height=1, width=5,font=f3,command=play)
b44.pack(side=LEFT)
b.pack(side=LEFT)
b11.pack(side=LEFT)
b33.pack(side=LEFT)

class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        
    def isSafe(self, v, colour, c):
        for i in range(self.V):
            if self.graph[v][i] == 1 and colour[i] == c:
                return False
        return True
#..........................Forward checking..............................#

    def ColourChange(self,v,colour,c):
        for i in range(self.V):
            if self.graph[v][i] == 1 and colour[i]==0:
                if(c==1):
                    canvas.itemconfig(r1[i+1],fill="white")
                elif(c==2):
                    canvas.itemconfig(g1[i+1],fill="white")
                elif(c==3):
                    canvas.itemconfig(b1[i+1],fill="white")
                    
    def colourChack(self,v,colour,lastcolour):
        for i in range(self.V):
            if self.graph[v][i] == 1 and colour[i]!=0:
                LastColour1=canvas.itemcget(x1[i+1],"fill")
                if lastcolour==LastColour1:
                        return False
        return True
    
    def ColourChange1(self,v,colour,lastcolour):
            for i in range(self.V):
                if self.graph[v][i]==1 and colour[i]==0:
                    if(lastcolour=="red"):
                        if(self.colourChack(i,colour,lastcolour)==True):
                            canvas.itemconfig(r1[i+1],fill=lastcolour)
                        else:
                            canvas.itemconfig(r1[i+1],fill="white")
                    elif(lastcolour=="green"):
                         if(self.colourChack(i,colour,lastcolour)==True):
                             canvas.itemconfig(g1[i+1],fill=lastcolour)
                         else:
                             canvas.itemconfig(g1[i+1],fill="white")
                    elif(lastcolour=="blue"):
                        if(self.colourChack(i,colour,lastcolour)==True):
                            canvas.itemconfig(b1[i+1],fill=lastcolour)
                        else:
                            canvas.itemconfig(b1[i+1],fill="white")
                elif self.graph[v][i]==1 and colour[i]!=0:
                    if(colour[i]==1):
                        canvas.itemconfig(r1[v+1],fill="white")
                    elif(colour[i]==2):
                        canvas.itemconfig(g1[v+1],fill="white")
                    elif(colour[i]==3):
                        canvas.itemconfig(b1[v+1],fill="white")
                                          
#..........................Ordering..............................#
                        
    def Mrv(self):
            min_value=3
            exit_value=0
            for i in range(1,10):
                x=3
                LastColour_x1=canvas.itemcget(x1[i],"fill")
                if(LastColour_x1=="white"):
                    LastColour_r1=canvas.itemcget(r1[i],"fill")
                    if(LastColour_r1=="white"):
                        x-=1
                    LastColour_g1=canvas.itemcget(g1[i],"fill")
                    if(LastColour_g1=="white"):
                        x-=1
                    LastColour_b1=canvas.itemcget(b1[i],"fill")
                    if(LastColour_b1=="white"):
                        x-=1
                    if((x < min_value )):
                                 min_value=x
                                 ff1[6]=i
                else:
                    exit_value+=1
            if(exit_value==9):
                    ff1[7]=1
                    return ;
    
    def Mrv_W_Deg(self):
            max_value1=0
            min_value1=3
            exit_value1=0
            for i in range(1,10):
                x=3
                LastColour_x1=canvas.itemcget(x1[i],"fill")
                if(LastColour_x1=="white"):
                    LastColour_r1=canvas.itemcget(r1[i],"fill")
                    if(LastColour_r1=="white"):
                        x-=1
                    LastColour_g1=canvas.itemcget(g1[i],"fill")
                    if(LastColour_g1=="white"):
                        x-=1
                    LastColour_b1=canvas.itemcget(b1[i],"fill")
                    if(LastColour_b1=="white"):
                        x-=1
                    if((x <= min_value1)):
                                  min_value1=x
                                  if (max_value1 < min_value1+deg[i-1]):
                                                   max_value1=min_value1+deg[i-1]
                                                   ff1[8]=i           
                else:
                    exit_value1+=1
            if(exit_value1==9):
                        ff1[9]=1
                        return ;

    def graphColourUtil(self, m, colour, v):
        if v == self.V:
            return True
        for c in range(1, m + 1):
                if self.isSafe(v, colour, c) == True:
                    colour[v] = c
                    if c==1:
                        st="red"
                    elif c==2:
                        st="green"
                    elif c==3:
                        st="blue"
                    elif c==5:
                        st="black"
                    elif c==4:
                        st="cyan"
                    time.sleep(ff1[10])
                    canvas.update()
                    canvas.itemconfig(x1[v+1],fill=st)
                    canvas.itemconfig(r1[v+1],fill=st)
                    canvas.itemconfig(g1[v+1],fill=st)
                    canvas.itemconfig(b1[v+1],fill=st)
                    if(ff1[1]==1):
                        self.ColourChange(v,colour,c)
                        if(ff1[3]==1):
                            if ff1[7]==0:
                                self.Mrv()
                                v=ff1[6]-2
                        if(ff1[4]==1):
                            if ff1[9]==0:
                                self.Mrv_W_Deg()
                                v=ff1[8]-2
                        if(ff1[5]==1):
                            ff1[3]=ff1[4]=0
                         
                    canvas.update()
                    if self.graphColourUtil(m,colour, v + 1) == True:
                        return True
                    time.sleep(ff1[10])
                    canvas.update()
                    LastColour=canvas.itemcget(x1[v+1],"fill")
                    canvas.itemconfig(x1[v+1],fill="white")
                    canvas.itemconfig(r1[v+1],fill="white")
                    canvas.itemconfig(g1[v+1],fill="white")
                    canvas.itemconfig(b1[v+1],fill="white")
                    if ff1[1]==1:
                        canvas.itemconfig(r1[v+1],fill="red")
                        canvas.itemconfig(g1[v+1],fill="green")
                        canvas.itemconfig(b1[v+1],fill="blue")
                        self.ColourChange1(v,colour, LastColour)
                    canvas.update()
                    colour[v] = 0

    def graphColouring(self, m):
        colour = [0] * self.V
        v=0
        if(ff1[4]==1):
            if ff1[9]==0:
                self.Mrv_W_Deg()
                v=ff1[8]-1
        if self.graphColourUtil(m, colour, v) == None:
            messagebox.showwarning('Notification','Not Possible Colouring Please Increase Your Colour Number')
            return False
        time.sleep(.5)
        messagebox.showinfo('Notification','"\/***********Graph Colouring Complited***********\/"')
root.mainloop()