base = input("Please enter the base: ")
exponent = input("Please enter the exponent: ")
modulus = input("Please enter the modulus: ")

if exponent < 0:
    print "To compute the inverse of an element, please use eea.py."
    quit()

if not isinstance(exponent, int) or not isinstance(base, int) or not isinstance(modulus, int):
    print "Please use only integers as input."
    quit()

if exponent == 0:
    print "0   " + str(base) + "^0 = 1 mod " + str(modulus)
    quit()

if base < 0:
    base += modulus

calc = base

binary_Exponent = str("{0:b}".format(exponent))

print binary_Exponent[0] + "   " + str(base)

for i in range(1, len(binary_Exponent)):
    if binary_Exponent[i] == '1':
        print binary_Exponent[i] + "   " + str(calc) + "^2 * " + str(base) + " =",
        calc = (calc*calc*base) % modulus
        print str(calc) +" mod " + str(modulus)
    else:
        print binary_Exponent[i] + "   " + str(calc) + "^2 =",
        calc = (calc*calc) % modulus
        print str(calc) + " mod " + str(modulus)
