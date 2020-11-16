from tkinter import *
print("WELCOME TO MY PROGRAM...\n")
print("EAA CALCULATOR BY AMOGH NAYAK Ver:1.0...\n")
print("LETS START!!!...")

root = Tk()
root.wm_title("EEA-CALULATOR")
root.resizable(width=FALSE, height=FALSE)
root.geometry("300x400")
num1 = IntVar()
num2 = IntVar() 
text_status = StringVar()#status text 

# function draws EEA table
class eea_table:
    def __init__(self,a,b,d,k,y,s):
        if s == 1:
            color = "red"
        else:
            color = "black"
        z = [40,110,180,250]
        num = [a,b,d,k]
        for i in range(4):
            self.status = Label(root,text=num[i],fg=color).place(x=z[i],y=y,anchor=CENTER)
            
# function computes the EEA table        
def egcd(n1, n2):
    eeatable_new = Frame(root,height = 400, width = 300).place(y=130)
    a1,b1,d1,k1,y = 1,0,n1,0,150
    a2,b2,d2,k2 = 0,1,n2,n1//n2
    eea_table(a1,b1,d1,k1,120,0)
    eea_table(a2,b2,d2,k2,150,0)
    while k2 != 0:
        
        an = a1-k2*a2
        bn = b1-k2*b2
        dn = d1-k2*d2
        y += 30
        if dn == 0:
            kn = 0
        else :
            kn = d2//dn
        eea_table(an,bn,dn,kn,y,0)
        a1,b1,d1,k1 = a2,b2,d2,k2
        a2,b2,d2,k2 = an,bn,dn,kn
    y -= 30
    eea_table(a1,b1,d1,k1,y,1)
    i = "THEREFORE (%d)(%d) + (%d)(%d) = gcd(%d,%d) = %d" %(n1,a1,n2,b1,n1,n2,d1)
    therefore_line= Label(root,text=i,bg="yellow").place(x=145,y=y+60,anchor=CENTER)
    print("DONE!")

#function updates the status of the window      
def label_status():
    if (num1.get() == 0 or num2.get()== 0):
        text_status.set("Error: Number should not be ZERO...")
        print ("Error: Number should not be ZERO...")
    elif (num1.get() <= num2.get()):
        text_status.set("Error: Num1 should be GREATER than Num2...")
        print ("Error: Num1 should be GREATER than Num2...")
    elif(num1.get() < 0 or num2.get()< 0):
        text_status.set("Error: Number has to be GREATER than 0...")
        print ("Error: Number has to be GREATER than 0...")
    else :
        text_status.set("Status: Successfull...")
        egcd(num1.get(),num2.get())
                
#interface of the window
num1_label = Label(root, text="Number 1",bd=10).grid(row=0)
num1_text = Entry(root, textvariable=num1,width = 10).grid(row=0,column=1)
num2_label = Label(root, text="Number 2",bd=10).grid(row=0,column = 2)
num2_text = Entry(root, textvariable=num2,width = 10).grid(row=0,column=3)
cal_button = Button(root,text="CALCULATE",width = 15,command=label_status).place(x=90,y=35)

status = Label(textvariable=text_status).place(x=150,y=75,anchor=CENTER)
text_status.set("Status: Done...")

a_label = Label(root,text="A").place(x = 40, y = 95, anchor=CENTER)
b_label = Label(root,text="B").place(x = 110, y = 95, anchor=CENTER)
d_label = Label(root,text="D").place(x = 180, y = 95, anchor=CENTER)
k_label = Label(root,text="K").place(x = 250, y = 95, anchor=CENTER)

        
root.mainloop()
