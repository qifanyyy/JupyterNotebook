from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from qiskit_fast_shor import Shor
from qiskit import Aer, IBMQ
from scapy.all import sniff, TCP
import logging
import re
import RSA
import socket
import sys

# Defaulting level to logging.WARN helps us disable logging in Qiskit code
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.WARN)
logger = logging.getLogger('simple_example')
if "--debug" in sys.argv:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

class SniffingFSM:
    state = "INIT"

    def ingest(self, data, sourceIsServer):
        if self.state == "INIT":
            assert sourceIsServer
            pubkey_pattern = re.compile("pubkey: e=([0-9]+), n=([0-9]+)")
            pubkey_matches = pubkey_pattern.match(str(data, 'utf-8'))
            self.pubkey = (int(pubkey_matches.group(1)), int(pubkey_matches.group(2)))
            logger.info("Public key found: {}".format(self.pubkey))
            self.state = "AWAIT_SESSION_KEY"
        elif self.state == "AWAIT_SESSION_KEY":
            assert not sourceIsServer
            self.encrypted_session_key = data
            logger.debug("Encrypted session key: " + self.encrypted_session_key.hex())
            self.state = "AWAIT_IV"
        elif self.state == "AWAIT_IV":
            assert not sourceIsServer
            self.iv = data
            logger.debug("AES IV: " + self.iv.hex())
            self.state = "AWAIT_EMAIL"
        elif self.state == "AWAIT_EMAIL":
            assert not sourceIsServer
            self.encrypted_email = data
            logger.debug("Encrypted email: " + self.encrypted_email.hex())
            self.state = "AWAIT_PASSWORD"
        elif self.state == "AWAIT_PASSWORD":
            assert not sourceIsServer
            self.encrypted_password = data
            logger.debug("Encrypted password: " + self.encrypted_password.hex())
            self.state = "AWAIT_EMAILS"
        elif self.state == "AWAIT_EMAILS":
            assert sourceIsServer
            self.encrypted_emails = data
            logger.debug("Encrypted emails: " + self.encrypted_emails.hex())
            self.factor()
            self.state = "INIT"
        else:
            logger.error("Unknown state {}".format(self.state))
            sys.exit(1)

    def factor(self):
        logger.info("Data collected. Constructing Shor circuit...")
        a = 2
        N = self.pubkey[1]

        if "--aer" in sys.argv:
            logger.info("Using Aer backend")
            backend = Aer.get_backend('qasm_simulator')
        else:
            logger.info("Using IBMQ backend")
            provider = IBMQ.load_account()
            backend = provider.get_backend('ibmq_qasm_simulator')

        job_id = None
        if "--cache" in sys.argv:
            logger.info("Using IBMQ job cache")
            if N == 33:
                job_id = "5ecaeb4bd2d11d001a1aaf72"
            elif N == 15:
                job_id = "5ecae5ed4f56e200131772af"
            else:
                logger.error("No cached job for N={}".format(N))
                sys.exit(1)
        else:
            logger.debug("Not using job cache")

        shor = Shor(N, a, quantum_instance=backend, job_id=job_id)
        circuit = shor.construct_circuit()
        logger.info("Running Shor circuit...")
        res = shor.run(job_id=job_id)

        p, q = res["factors"][0]
        logger.info("Public key factored: p, q = {}, {}".format(p, q))
        pubkey, privkey = RSA.generate_keypair(p, q)

        session_key = RSA.decrypt(self.encrypted_session_key, privkey)
        logger.debug("AES session key decrypted: key=" + session_key.hex())
        cipher = AES.new(session_key, AES.MODE_CBC, self.iv)

        email = str(unpad(cipher.decrypt(self.encrypted_email), AES.block_size), 'UTF-8')
        password = str(unpad(cipher.decrypt(self.encrypted_password), AES.block_size), 'UTF-8')
        logger.info("Credentials decrypted: email={}, password={}".format(email, password))

        emails = str(unpad(cipher.decrypt(self.encrypted_emails), AES.block_size), 'UTF-8')
        logger.info("Emails decrypted:")
        print("")
        print(emails)

fsm = SniffingFSM()

packets_seen = []

def custom_action(packet):
    payload = packet[0][1][TCP].payload
    if len(payload) == 0:
        return
    seq = packet[0][1][TCP].seq
    if seq in packets_seen:
        return
    packets_seen.append(seq)
    sourceIsServer = packet[0][1].sport == 9999
    fsm.ingest(bytes(payload), sourceIsServer)

logger.info("Sniffing TCP traffic on loopback interface")
sniff(filter="tcp", prn=custom_action, iface="lo", store=0)