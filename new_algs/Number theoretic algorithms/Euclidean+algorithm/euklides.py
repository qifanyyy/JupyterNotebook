"""
Algorytm Euklidesa
  ___     _   _ _    _                        
 | __|  _| |_| (_)__| |___ ___      _ __ _  _ 
 | _| || | / / | / _` / -_|_-<  _  | '_ \ || |
 |___\_,_|_\_\_|_\__,_\___/__/ (_) | .__/\_, |
                                   |_|   |__/ 
Z dedykacja dla Pani Profesor Stajno :)
"""
a = int(raw_input("Podaj liczbe a: "))
b = int(raw_input("Podaj liczbe b: "))
c = 0
licznik = 1
if b == 0:
	print("b == 0. Koniec liczenia. NWD wynosi: " + str(a))
	exit()
while b != 0:
	print("\n\n\nRunda " + str(licznik))
	c = a % b
	a = b
	b = c
	print("a = " + str(a))
	print("c = " + str(c))
	print("b = " + str(b))
	licznik += 1
