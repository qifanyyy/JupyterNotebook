from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import logging
import RSA
import socketserver
import sys

if "--debug" in sys.argv:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=loglevel)

public, private = RSA.generate_keypair(3, 5)

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        logging.info("New connection from {}".format(self.client_address[0]))

        # Send the public key
        pubkey_message = "pubkey: e={}, n={}".format(public[0], public[1])
        logging.debug("Sent: {}".format(pubkey_message))
        self.request.sendall(bytes(pubkey_message, 'utf-8'))

        # Read the AES IV & session key
        encrypted_session_key = self.request.recv(1024)
        session_key = RSA.decrypt(encrypted_session_key, private)
        logging.debug("Session key: " + session_key.hex())
        iv = self.request.recv(16)
        logging.debug("AES IV: " + iv.hex())
        cipher = AES.new(session_key, AES.MODE_CBC, iv)

        # Read the credentials. Pretend logins are always successful.
        encrypted_email = self.request.recv(1024)
        email = str(unpad(cipher.decrypt(encrypted_email), AES.block_size), 'UTF-8')
        encrypted_password = self.request.recv(1024)
        password = str(unpad(cipher.decrypt(encrypted_password), AES.block_size), 'UTF-8')
        logging.info("New login: email={}, password={}".format(email, password))

        # Workaround to force the crypto lib to play nice
        cipher._next = [cipher.encrypt, cipher.decrypt]
        # Send the list of emails
        emails = \
            "    <From maurizio.zamboni@polito.it> PolitOpenDays\n" +\
            "    <From rettore@polito.it> Nuove indicazioni per le attività didattiche\n" +\
            "    <From anna.carbone@polito.it> Your IICQ exam results"
        output = cipher.encrypt(pad(bytes(emails, 'UTF-8'), AES.block_size))
        logging.debug("Sent: " + output.hex())
        self.request.sendall(output)
        self.request.close()

HOST, PORT = "localhost", 9999

# Create the server, binding to localhost on port 9999
with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    logging.info("Listening on {}:{}".format(HOST, PORT))
    server.serve_forever()