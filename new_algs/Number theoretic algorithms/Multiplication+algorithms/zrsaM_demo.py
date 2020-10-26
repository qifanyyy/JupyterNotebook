from Crypto.Util import number
from zrsaM import encrypt, decrypt, sign, verify, keygen

# requires pycrypto

# This script demonstrates a signed communication between Alice and Bob

print "Generating Alice and Bob's keys..."
# Alice's keys
alice_sk, alice_pk, alice_mod = keygen()

# Bob's keys
bob_sk, bob_pk, bob_mod = keygen()

# Messages to be sent
print "Alice wants to send the message"
alice_msg = "Hello Bob!"
print alice_msg
print "Bob wants to send the message"
bob_msg = "Hello Alice!"
print bob_msg

# Encryption of the messages
alice_m = number.bytes_to_long(alice_msg)
bob_m = number.bytes_to_long(bob_msg)

print "Alice encrypts a message to Bob with his public key and modulus"
to_bob = encrypt(alice_m, bob_pk, bob_mod)
print to_bob
print "Bob encrypts a message to Alice with her public key and modulus"
to_alice = encrypt(bob_m, alice_pk, alice_mod)
print to_alice

# Signing of the messages
print "Alice signs her message to Bob using her secret key and modulus"
to_bob_sign = sign(to_bob, alice_sk, alice_mod)
print to_bob_sign
print "Bob signs his message to Alice using his secret key and modulus"
to_alice_sign = sign(to_alice, bob_sk, bob_mod)
print to_alice_sign

# They exchange messages and decrypt

print "Alice receives a message from Bob and decrypts it with her private key"
from_bob_m = decrypt(to_alice, alice_sk, alice_mod)
print from_bob_m
print "Bob receives a message from Alice and decrypts it with his private key"
from_alice_m = decrypt(to_bob, bob_sk, bob_mod)
print from_alice_m

# Alice and Bob compute the signature verification and if it's True then they know the message originated from the correct sender

# Bob verifies and reads the message
print "Bob verifies the contents of the message using his public key and the signature"
if verify(from_alice_m, to_bob, bob_pk, bob_mod, to_bob_sign):
    print "Bob reads the message:"
    print number.long_to_bytes(from_alice_m)

# Alice verifies and reads the message
print "Alice verifies the contents of the message using her public key and the signature"
if verify(from_bob_m, to_alice, alice_pk, alice_mod, to_alice_sign):
    print "Alice reads the message"
    print number.long_to_bytes(from_bob_m)
