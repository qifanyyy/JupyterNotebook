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

id = os.getpid()
logger = logging.getLogger(__name__)
logger.info("Master Node")


FLAGFORALGO = False

listIP = []
listPORT = []
listFD = []

def server():
    s = socket.socket()
    print("Socket successfully created")
    port = 8080
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', port))
    print("socket binded to %s" % (port))
    s.listen(5)
    print ("socket is listening")
    c, addr = s.accept()
    print('Got connection from', addr)
    listIP.append(addr[0])
    listFD.append(c)
    c.send(b'PORTNO')
    reply = c.recvfrom(1024)
    reply = reply[0].decode('utf-8').split()
    listPORT.append(int(reply[2]))
    print(listIP)
    print(listPORT)

flag=True
while(flag):
    print("::::::::::::::::::::::::MASTER::::::::::::::::::::::::::")
    print("Choose the following")
    print("1:Get a Node")
    print("2:Make a Ring")
    print("3:Run Algorithm")
    print("10: Exit")
    choice = input()
    if choice=='1':
        server()
    if choice=='2':
        if(len(listFD)>0 and (not FLAGFORALGO)):
            for i in range(len(listFD)):
                fd = listFD[i]
                if(i==(len(listFD)-1)):
                    msg = ('CONNECTCWTO 127.0.0.1 ' +str(listPORT[0])).encode('utf-8')
                else:
                    msg = ('CONNECTCWTO 127.0.0.1 '+str(listPORT[i+1])).encode('utf-8')
                fd.send(msg)
            print("RING FORMED")
            FLAGFORALGO=True
        else:
            print("Cannot make ring not enough node or ring already formed")

    if choice=='3':
        if FLAGFORALGO :
            msg = ('START').encode('utf-8')
            for i in range(len(listFD)):
                fd = listFD[i]
                fd.send(msg)
        else:
            print("Cannot Run Alorithm")
    if choice=='10':
        flag=False


if __name__ == "__main__": 
    main()