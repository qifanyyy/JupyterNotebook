from zrsaMP import keygen

sk, pk, n = keygen()
print ("Secret key:", sk)
print ("Public Key:", pk)
print ("Modulus:", n)
