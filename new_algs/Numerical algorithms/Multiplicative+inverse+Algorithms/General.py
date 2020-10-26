"""
	@author: Brando Sánchez BR7
	@Version: 24/03/19
	INSTITUTO POLITÉCNICO NACIONAL
	ESCUELA SUPERIOR DE CÓMPUTO
	CRYPTOGRAPHY
"""

from tkinter import *
import InvMult
import Potentiaton
import Miller_Robin
from functools import partial

def main():
	global w1, r1, r2, e1, e2, e3, e4, e5, e6

		
	x=400
	y=630
	title = "CRYPTOOLS V1.0"
	w1 = Tk()
	dim = str(x) + "x" + str(y)
	w1.title(title)
	w1.maxsize(x,y)

	### INVERSO MULTIPLICATIVO
	f1 = Frame(w1, width=x, height=y, bg='BLACK')
	f1.pack(side=LEFT)

	l1 = Label(w1, text="Ingrese a y b para hallar su inverso multiplicativo:", width=58, bg='BLACK', fg='#01DF3A')
	l1.place(x=0,y=20)

	l2 = Label(w1, text="a = :", width=10, bg='BLACK', fg='#01DF3A')
	l2.place(x=10,y=40)
	

	e1 = Entry(w1, bd=1, width=45, bg='BLACK', fg='#01DF3A', justify=CENTER)
	e1.place(x=70, y=40)

	
	l3 = Label(w1, text="b = :", width=10, bg='BLACK', fg='#01DF3A')
	l3.place(x=10,y=60)

	varInv = StringVar()
	l4 = Label(w1, textvariable=varInv, bg='BLACK', fg='#01DF3A')
	l4.place(x=130,y=130)

	e2 = Entry(w1, bd=1, width=45, bg='BLACK', fg='#01DF3A', justify=CENTER)
	e2.place(x=70, y=60)

	action_InvMult = partial(showInvMult, varInv)
	b1 = Button(w1, text="Generar inverso multiplicativo", bg='BLACK', fg='#01DF3A', command = action_InvMult)
	b1.place(x=120, y=90)

	dif = 20
	### POTENCIACION
	l5 = Label(w1, text="Ingrese base, exponente y modulo :", width=58, bg='BLACK', fg='#01DF3A')
	l5.place(x=0,y=190-dif)

	l6 = Label(w1, text="base = :", width=10, bg='BLACK', fg='#01DF3A')
	l6.place(x=36,y=210-dif)
	
	e3 = Entry(w1, bd=1, width=30, bg='BLACK', fg='#01DF3A', justify=CENTER)
	e3.place(x=110, y=210-dif)

	l7 = Label(w1, text="exponente = :", width=10, bg='BLACK', fg='#01DF3A')
	l7.place(x=20,y=230-dif)

	e4 = Entry(w1, bd=1, width=30, bg='BLACK', fg='#01DF3A', justify=CENTER)
	e4.place(x=110, y=230-dif)

	l8 = Label(w1, text="modulo = :", width=10, bg='BLACK', fg='#01DF3A')
	l8.place(x=26,y=250-dif)

	varPot = StringVar()
	l9 = Label(w1, textvariable=varPot, bg='BLACK', fg='#01DF3A')
	l9.place(x=150,y=320-dif)
	
	e5 = Entry(w1, bd=1, width=30, bg='BLACK', fg='#01DF3A', justify=CENTER)
	e5.place(x=110, y=250-dif)

	action_Pot = partial(showPotentiaton, varPot)
	b2 = Button(w1, text="Realizar Potenciacion", bg='BLACK', fg='#01DF3A', command = action_Pot)
	b2.place(x=140, y=280-dif)

	### Miller-Robin

	l10 = Label(w1, text="Ingrese el numero a evualuar primalidad :", width=58, bg='BLACK', fg='#01DF3A')
	l10.place(x=0,y=350-dif)

	l11 = Label(w1, text="numero = :", width=10, bg='BLACK', fg='#01DF3A')
	l11.place(x=36,y=380-dif)
	
	e6 = Entry(w1, bd=1, width=30, bg='BLACK', fg='#01DF3A', justify=CENTER)
	e6.place(x=110, y=380-dif)

	varPrim = StringVar()
	l12 = Label(w1, textvariable=varPrim, bg='BLACK', fg='#01DF3A')
	l12.place(x=165,y=435-dif)

	action_Prim = partial(showMillerRobin, varPrim)
	b3 = Button(w1, text="Realizar Test Miller-Robin", bg='BLACK', fg='#01DF3A', command = action_Prim)
	b3.place(x=130, y=410-dif)
	
	#Credits
	logo = PhotoImage(file='logo.png')
	imageLabel = Label(w1, image=logo,  width=200, bg='BLACK', fg='#01DF3A')
	imageLabel.place(x=95, y=430)

	w1.mainloop()
	
def showInvMult(varInv):
	
	r1 = e1.get()
	r2 = e2.get()
	invMult = InvMult.inversoMultiplicativo(int(r1), int(r2)) 
	
	if invMult:
		varInv.set("El inverso multiplicativo es " + "\n" + str(invMult))
		"""strInvMult = strInvMult + "\nya que " + str()"""
	else:
		varInv.set("El inverso multiplicativo no existe ")

	

def showPotentiaton(varPot):

	base = e3.get()
	exp = e4.get()
	mod = e5.get()

	result = Potentiaton.squareAndMultiply(int(base),int(exp),int(mod))

	varPot.set('Resultado: ' + str(result))
	

def showMillerRobin(varPrim):
	
	numero = e6.get()

	isPrime = Miller_Robin.millerRobin(int(numero))

	if isPrime:
		varPrim.set('Posible Primo')
	else:
		varPrim.set('Es Compuesto')

main()
