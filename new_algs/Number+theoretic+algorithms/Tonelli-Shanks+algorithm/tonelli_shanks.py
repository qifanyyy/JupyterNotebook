from Tkinter import *
def TS(p,n):
    import math
    if(int(math.pow(n,(p-1)/2))%p !=1):
        return("No solutions")
    # find max power of 2 dividing p-1
    s=0
    while((p-1)%math.pow(2,s)==0):
        s+=1
    s-=1
    q=int((p-1)/math.pow(2,s))# p-1=q*2^s
    # Select a z such that z is a quadratic non-residue modulo p
    z=1
    res=int(math.pow(z,(p-1)/2))%p
    while(res !=p-1):
        z+=1
        res=math.pow(z,(p-1)/2)%p
    c=int(math.pow(z,q))%p
    r=int(math.pow(n,(q+1)/2))%p
    t=int(math.pow(n,q))%p
    m=s
    while(t%p !=1):
        i=0
        div=False
        while(div==False):
            i+=1
            t=int(math.pow(t,2))%p
            if(t%p==1):
                div=True
        b=int(math.pow(c,int(math.pow(2,m-i-1))))%p
        r=(r*b)%p
        t=t*(b**2)%p
        c=(b**2)%p
        m=i
        
    return r
    
def calculate():
    res=TS(int(e1.get()), int(e2.get()))
    print(res)
    t="result: "+str(res)
    text.delete(1.0, END)
    text.insert(INSERT,t)

    
master = Tk()
master.title("Tonelli-shanks")
labelfont = ('times', 20, 'bold')
label1=Label(master, text="prime p (modulo):")
label1.grid(row=0)
label1.config(bg='black', fg='yellow')
label1.config(font=labelfont)
label2=Label(master, text="n:")
label2.grid(row=1)
label2.config(bg='black',fg='yellow')
label2.config(font=labelfont)

e1 = Entry(master)
e2 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
text = Text(master,bd=5,height=1,width=20)
text.grid(row=2)



Button(master, text='Calculate', command=calculate).grid(row=3, column=1, sticky=W, pady=4)

mainloop( )
