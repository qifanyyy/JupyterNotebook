

def main():
	
	r1 = 19
	r2 = 16

	invMult = inversoMultiplicativo(r1,r2) 

	if invMult:
		strInvMult = "El inverso multiplicativo de " + "\n" + str(r1) + "\n y \n" + str(r2) + "\n es: " + "\n" + str(invMult)
		"""strInvMult = strInvMult + "\nya que " + str()"""
	else:
		strInvMult = "El inverso multiplicativo de " + "\n" + str(r1) + "\n y \n" + str(r2) + "\n no existe "
	
	print(strInvMult)

def inversoMultiplicativo(r1, r2):
	if r2>r1 or r2<0:
		print("Condición 0 <= r2 <= r1 no cumplida")
		return False

	auxR1 = r1
	auxR2 = r2
	auxR4 = 1
	j = 2
	arrayT = []
	arrayT.append(0)
	arrayT.append(1)
	
	while auxR4 != 0:

		auxR3 = auxR1 // auxR2
		auxR4 = auxR1 % auxR2

		arrayT.append((arrayT[j-2] - auxR3 * arrayT[j-1]) % r1) 

		"""print(str(auxR1) + "  = " + str(auxR3) + " x " + str(auxR2) + " + " + str(auxR4) + "\n" + "T" + str(j) + " = " + str(arrayT[j]))"""

		auxR1 = auxR2
		auxR2 = auxR4
		j += 1;

		if auxR4 == 1:
			"""print(str(r1) + " y " + str(r2) + " son primos relativos")"""
			return arrayT[j-1]

	return False


