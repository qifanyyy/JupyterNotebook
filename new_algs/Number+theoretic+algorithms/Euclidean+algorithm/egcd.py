import sys

def egcd(a, b):
	auxiliar = (a, b)
	a = max(auxiliar)
	b = min(auxiliar)
	x = (1, 0)
	y = (0, 1)
	while a % b != 0:
		q = a / b
		c = a % b
		nx = x[0] - (x[1] * q)
		ny = y[0] - (y[1] * q)
		x = (x[1], nx)
		y = (y[1], ny)
		a = b
		b = c
	resultado = (b, x[1], y[1])
	return resultado

if len(sys.argv) != 3:
	print ('El numero de argumentos es invalido')
else:
	if sys.argv[1].isdigit() and sys.argv[2].isdigit():
		if sys.argv[1] > 1 and sys.argv[2] > 1:
			a = int(sys.argv[1])
			b = int(sys.argv[2])
			resultado = egcd(a, b)
			print (resultado)
	else:
		print ('Todos los argumentos deben ser numeros')
