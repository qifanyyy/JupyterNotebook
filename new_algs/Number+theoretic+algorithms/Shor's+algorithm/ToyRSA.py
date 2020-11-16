#
# This is a simple RSA encryption utility
# To use your custom alphabet, please change alphabet var
# 

alphabet84 = " !(),-./0123456789:?АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя"
alphabet50 = " !(),-.0123456789:?АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

#public85 = (11, 85)
#public51 = (7, 51)


pub_key = (11, 85)
message = 'Три девицы под окном пряли поздно вечерком.'

alphabet = ''
if pub_key[1] == 85:
	alphabet = alphabet84
elif pub_key[1] == 51:
	alphabet = alphabet50

encrypted_message = ''
for i in message:
	index = (alphabet.index(i)**pub_key[0]) % pub_key[1]
	encrypted_message += alphabet[index]

print("Encrypted text: {}".format(encrypted_message))
