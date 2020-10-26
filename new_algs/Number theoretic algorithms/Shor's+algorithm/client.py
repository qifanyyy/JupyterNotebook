from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import logging
import re
import RSA
import socket
import sys

HOST, PORT = "localhost", 9999
if "--debug" in sys.argv:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=loglevel)

pubkey_pattern = re.compile("pubkey: e=([0-9]+), n=([0-9]+)")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    logging.info("Connected to {}:{}".format(HOST, PORT))

    # Receive and parse pubkey
    pubkeydata = sock.recv(1024)
    pubkey_matches = pubkey_pattern.match(str(pubkeydata, 'utf-8'))
    pubkey = (int(pubkey_matches.group(1)), int(pubkey_matches.group(2)))
    logging.debug("Public key: {}".format(pubkey))

    # Generate AES IV & session key
    session_key = get_random_bytes(16)
    logging.debug("Session key: " + session_key.hex())
    encrypted_session_key = RSA.encrypt(session_key, pubkey)
    sock.sendall(encrypted_session_key)
    cipher = AES.new(session_key, AES.MODE_CBC)
    # The IV should not be reused in the real world! But this is a demo about
    # factoring RSA keys in TLS, so we can ignore other cryptographic concerns.
    iv = cipher.iv
    logging.debug("AES IV: " + iv.hex())
    sock.sendall(iv)

    # All communication from now on will be encrypted with the AES session key.

    print("Enter your credentials to log in.")
    print("")

    email = input("    Email: ")
    encrypted_email = cipher.encrypt(pad(bytes(email, 'UTF-8'), AES.block_size))
    sock.sendall(encrypted_email)
    password = input("    Password: ")
    encrypted_password = cipher.encrypt(pad(bytes(password, 'UTF-8'), AES.block_size))
    sock.sendall(encrypted_password)
    print("")
    print("Logged in successfully! Here are your emails:")
    print("")

    # Workaround to force the crypto lib to play nice
    cipher._next = [cipher.encrypt, cipher.decrypt]
    # Receive data from the server and shut down
    indata = sock.recv(1024)
    decrypted = str(unpad(cipher.decrypt(indata), AES.block_size), 'UTF-8')
    print(decrypted)