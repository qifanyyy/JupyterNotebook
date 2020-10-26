#EEA (wird benoetigt um s zu berechnen)
def eea(int_1, int_2):

    #Modulureduktion, falls Basis groesser Modulus
    if int_1 < int_2:
        int_2 -= int_1

    #Initialisierung der Liste(n)
    q = ['-', '-']
    r = [int_1, int_2]
    s = [1, 0]
    t = [0, 1]

    i = 2

    #Fuellen der Listen nach dem EEA
    while r[i-1] != 0:
        q.append(r[i-2]/r[i-1])
        r.append(r[i-2]%r[i-1])
        s.append(s[i-2]-q[i]*s[i-1])
        t.append(t[i-2]-q[i]*t[i-1])
        i += 1

    #Modulureduktion, falls berechnete Inverse negativ
    if t[i-2] < 0:
        t[i-2] += int_1

    #Rueckgabe der Inverse
    return t[i-2]

print "\nPlease notice: it is >your< responsibility to provide correct input. The program will >not< check validity of input for you.\n"

#Laesst Nutzer Operation waehlen
douboradd = input("Would you like to double (1) or add (2)? ")

if douboradd == 1:
    x = input("Please enter x: ")
    y = input("Please enter y: ")
    p = input("Please enter the modulus: ")
    a = input("Please enter a: ")
    b = input("Please enter b: ")

    #Berechnung der Koordinaten
    s = ((3*x*x+a) * eea(p, 2*y)) % p
    x3 = (s*s -2*x) % p
    y3 = (s*(x-x3) -y) % p

    print "\n(" + str(x3) + ", " + str(y3) + ")"

else:
    x1 = input("Please enter x1: ")
    y1 = input("Please enter y1: ")
    x2 = input("Please enter x2: ")
    y2 = input("Please enter y2: ")
    p = input("Please enter the modulus: ")
    a = input("Please enter a: ")
    b = input("Please enter b: ")

    #Falls Addition mit eigener Inverse: neutrales Element ausgeben!
    if x1 == x2 and y1 == -y2 + p:
        print "\nAddition with element's own inverse: result is the neutral element!"
        quit()

    #Berechnung der Koordinaten
    s = ((y2-y1) * eea(p, x2-x1)) % p
    x3 = (s*s -x1 -x2) % p
    y3 = (s*(x1-x3) -y1) % p

    print "\n(" + str(x3) + ", " + str(y3) + ")"

#Pruefen, ob Punkt auf Ellipse liegt
if (y3*y3) % p == (x3**3 + a*x3 + b) % p:
    print "Point is an element of the elliptic curve!"
else:
    print "Point is not an element of the elliptic curve!"