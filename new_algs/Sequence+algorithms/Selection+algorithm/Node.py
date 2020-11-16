import socket
import threading
import random
import os
import time
import select

import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

NO_COLOR = "\33[m"
RED, GREEN, ORANGE, BLUE, PURPLE, LBLUE, GREY = \
    map("\33[%dm".__mod__, range(31, 38))

logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

# the decorator to apply on the logger methods info, warn, ...
def add_color(logger_method, color):
	def wrapper(message, *args, **kwargs):
		return logger_method(
		# the coloring is applied here.
		color+message+NO_COLOR,
		*args, **kwargs
	)
	return wrapper

for level, color in zip((
	"info", "warn", "error", "debug"), (
	GREEN, ORANGE, RED, BLUE
)):
	setattr(logger, level, add_color(getattr(logger, level), color))

id = int(input("Enter PID: ")) #os.getpid()
logger = logging.getLogger(__name__)
logger.info("NODE ID: %d",id)



c=0
s=0
serverPort = 1025
rightFd = ''
leftFd = ''
flag = 0
phase = 1
msgFromRight = 'NULL'
msgFromLeft = 'NULL'
end = True
backLogQ = 5
bufferSize = 1024
lock = threading.Condition()

"""
This thread is created for receiving connection request
from Left
"""
def server():
    global leftFd
    s = socket.socket()
    logger.info("Socket successfully created for server")
    global serverPort
    portNotAlloacted = True
    while(portNotAlloacted):
        try:
            s.bind(('127.0.0.1', serverPort))
            portNotAlloacted = False
        except OSError:
            serverPort = random.randint(1026, 50000)

    logger.info("socket binded to %s" % (serverPort))

    s.listen(backLogQ)
    print("server is listening on port number ",serverPort)
    leftFd, addr = s.accept()
    print("Got connection from ", addr)


def client():
    global serverPort
    global end
    s = socket.socket()
    port = 8080
    s.connect(('127.0.0.1', port))
    
    running = True
    while(running):
        fromMaster = ((s.recv(1024)).decode('utf-8')).split()
        try:
            if fromMaster[0] == 'PORTNO':
                reply = 'PORT NO: ' + str(serverPort)
                reply = reply.encode('utf-8')
                s.send(reply)
            if fromMaster[0] == 'CONNECTCWTO':
                clientCW(fromMaster)
            if fromMaster[0] == 'START':
                t3 = threading.Thread(target=transition)
                t3.start()
            if fromMaster[0] == 'EXIT':
                s.close()
                running = False
        except IndexError:
            logger.info("DONE: SUCCESS")
            end = False
            break

def clientCW(fromMaster):
    global rightFd
    rightFd = socket.socket()
    IP = fromMaster[1]
    PORT = int(fromMaster[2])
    rightFd.connect((IP,PORT))
    print("connected to ",IP , PORT)


"""
This thread sends and recieves messages from left and right
nodes and processes these messages and sends/relays them to others
"""
def transition():
    global end
    global flag
    msgc = "clockwise " + str(id) + " 1 "
    msga = "anticlockwise " + str(id) + " 1 "
    sendRightNode(msga)
    sendLeftNode(msgc)
    while(end): 
        time.sleep(0.5)
        receiveFromRight()
        time.sleep(0.5)
        receiveFromLeft()
        time.sleep(0.5)
        processAndSend()
        time.sleep(5)


"""
This function is used process the incoming messages
and decide the action and send the message
and relays the message when required
"""
def processAndSend():
    logger.debug("ENTRY to processAndSend()")
    global msgFromLeft
    global msgFromRight
    global id
    global phase
    global end
    msgFromLeft = msgFromLeft.split()
    msgFromRight = msgFromRight.split()
    # nothing received on any side
    if msgFromLeft[0] =='NULL' and msgFromRight[0] =='NULL':
        msgFromLeft  = 'NULL'
        msgFromRight ='NULL'
        return
    else:
        print("Message received from LeftNode ",msgFromLeft);
        print("Message received from RightNode ",msgFromRight);
        # tuple received on each side
        if len(msgFromLeft)==3 and len(msgFromRight)==3:
            if msgFromLeft[2]=="1" and msgFromRight[2]=='1':
                if id != int(msgFromLeft[1]) and id != int(msgFromRight[1]):
                    retval = max(id,int(msgFromLeft[1]),int(msgFromRight[1]))
                    if retval == int(msgFromLeft[1]):
                        sendLeftNode(msgFromLeft[1])
                    if retval == int(msgFromRight[1]):
                        sendRightNode((msgFromRight[1]))
                if int(msgFromLeft[1])==id and int(msgFromRight[1])==id:
                        logger.info("<<<<<I-am-leader>>>>>")
                        end = False
            if msgFromLeft[2]=='1' and msgFromRight[2]!='1':
                pass
            if msgFromLeft[2] != '1' and msgFromRight[2] == '1':
                pass
            if msgFromLeft[2] != "1" and msgFromRight[2] != '1':
                if (id == int((msgFromRight[1]))) and (id == int((msgFromLeft[1]))):
                    logger.info("<<<<<I-am-leader>>>>>")
                    end = False
                if (id != int((msgFromRight[1]))) and (id != int((msgFromLeft[1]))):
                    msgFromRight[2] = str(int(msgFromRight[2])-1)
                    msgFromLeft[2] = str(int(msgFromLeft[2])-1)
                    sendRightNode(' '.join(msgFromLeft))
                    sendLeftNode(' '.join(msgFromRight))
        # advance to the next phase
        if len(msgFromLeft)==1 and len(msgFromRight)==1 and msgFromLeft[0]!='NULL' and msgFromRight[0]!='NULL':
            if int(msgFromLeft[0])==id and int(msgFromRight[0])==id:
                msgc = "clockwise " + str(id) + " "+str(pow(2,phase))+' '
                msga = "anticlockwise " + str(id) + " "+str(pow(2,phase))+' '
                sendRightNode(msga)
                sendLeftNode(msgc)
                phase = phase+1
            if int(msgFromRight[0]) > id and int(msgFromLeft[0]) > id:
                sendLeftNode(msgFromRight[0])
                sendRightNode(msgFromLeft[0])
        if msgFromLeft[0]=='NULL' and len(msgFromRight)==3:
            if msgFromRight[2]=='1':
                retval = max(id,int(msgFromRight[1]))
                if retval == int(msgFromRight[1]):
                    sendRightNode(msgFromRight[1])
            else:
                msgFromRight[2] = str(int(msgFromRight[2])-1)
                sendLeftNode(' '.join(msgFromRight))

        if msgFromRight[0] == 'NULL' and len(msgFromLeft)==3:
            if msgFromLeft[2] == '1':
                retval = max(id, int(msgFromLeft[1]))
                if retval == int(msgFromLeft[1]):
                    sendLeftNode(msgFromLeft[1])
            else:
                msgFromLeft[2] = str(int(msgFromLeft[2]) - 1)
                sendRightNode(' '.join(msgFromLeft))

        if msgFromLeft[0]=='NULL' and len(msgFromRight)==1:
            if int(msgFromRight[0])!=id:
                sendLeftNode(msgFromRight[0])

        if msgFromRight[0] == 'NULL' and len(msgFromLeft)==1:
            if int(msgFromLeft[0])!=id:
                sendRightNode(msgFromLeft[0])

    msgFromLeft = 'NULL'
    msgFromRight = 'NULL'
    logger.debug("EXIT from processAndSend()")


def sendRightNode(msg):
    global rightFd
    rightFd.send(msg.encode('utf-8'))


def receiveFromRight():
    global rightFd
    global msgFromRight
    result = select.select([rightFd], [], [], 0)
    if result[0]:
        msg = rightFd.recv(1024)
        msg = msg.decode('utf-8')
        logger.info("Received msg: %s", msg)
        msgFromRight = msg

def sendLeftNode(msg):
    global leftFd
    leftFd.send(msg.encode('utf-8'))

def receiveFromLeft():
    global leftFd
    global msgFromLeft
    result = select.select([leftFd], [], [], 0)
    if result[0]:
        msg = leftFd.recv(1024)
        msg = msg.decode('utf-8')
        logger.info("Received msg: %s", msg)
        msgFromLeft = msg

def main():

    t1 = threading.Thread(target=server)
    t1.start()

    time.sleep(1)
    
    t2 = threading.Thread(target=client)
    t2.start()


if __name__ == "__main__": 
    main()







