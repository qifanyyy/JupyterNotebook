import socket
import threading
import os
import time
WAIT_FOR_MY_SERVER_TO_START = 10
L = 0
R = 1
myServerPort = 11111
outfdsLR = [None,None]
def connectLeftRight():
    time.sleep(WAIT_FOR_MY_SERVER_TO_START)
    # fdL = connectToLeft()
    # fdR = connectToRight()
    # store these two in array fds: outfdsLR[L] and outfdsLR[R]

def processRequest(requestBuffer):
    # check the requestBuffer
    # get the message type
        # 1. from ring node -- make me peer type
        # loop in a while loop -- serving your one peer
    return
def main():
    serverSock = socket.socket()
    print("Socket successfully created")
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSock.bind(('127.0.0.1', myServerPort))
    print("socket binded to %s" % (myServerPort))
    serverSock.listen(10)
    print ("socket is listening")
    while True:
        conn, addr = s.accept()
        requestBuffer = conn.recv(1024) # 
        processRequest(requestBuffer)   # launch this function in a new thread
                                        # and move on
        
        conn.close()

if __name__ == '__main__':
    main()