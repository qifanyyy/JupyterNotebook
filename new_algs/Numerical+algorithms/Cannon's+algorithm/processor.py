#!/usr/bin/python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys

import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
Ice.loadSlice('-I {} container.ice'.format(Ice.getSliceDir()))
import Services
import Cannon
import time

from matrix_utils import matrix_multiply, matrix_add


class ProcessorI(Cannon.Processor):
    def init(self, row, col, above, left, order, target, current=None):
        self.C = None
        self.p_A = []; self.p_B = []
        for i in range(order):
            self.p_A.append(None)
            self.p_B.append(None)
        self.g_row = row
        self.g_col = col
        self.g_above = above 
        self.g_left = left
        self.g_order = order 
        self.g_step = 0
        self.collector = target
     	
    def Sum(self, A, B, step):
        self.C = matrix_add(self.C, matrix_multiply(A, B))
        self.g_step = self.g_step + 1
        	
        if self.g_step == self.g_order:
        	if step != (self.g_order - 1):
        		self.g_left.begin_injectFirst(A, (step + 1))
        		self.g_above.begin_injectSecond(B, (step + 1))
        	self.collector.injectSubmatrix(self.C, self.g_row, self.g_col)
        else:
        	if step != (self.g_order - 1):
        		self.g_left.begin_injectFirst(A, (step + 1))
        		self.g_above.begin_injectSecond(B, (step + 1))
        		

    def injectFirst(self, A, step, current=None):
        if self.C == None:
        	self.C = Cannon.Matrix(A.ncols, [])
        	for i in range(A.ncols ** 2):
        		self.C.data.append(0)
        
        self.p_A[step] = A
        			
        if self.p_B[step] != None:
        	self.Sum(A, self.p_B[step], step)
        		  		
        	

    def injectSecond(self, B, step, current=None):
        self.p_B[step] = B
        if self.p_A[step] != None:
            self.Sum(self.p_A[step], B, step)		
        	

class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        servant = ProcessorI()
        
        proxy_container = broker.stringToProxy(args[1])
        
        print("Esperando container...")
        
        while 1:
        	try:
        		proxy_container.ice_ping()
        		print("...Done"); break
        	except Ice.NoEndpointException:
        		time.sleep(1)
        	
        container = Services.ContainerPrx.checkedCast(proxy_container)
        
        if not container:
        	raise RuntimeError('Invalid proxy')

        adapter = broker.createObjectAdapter('ProcessorAdapter')
        
        pos = len(container.list())
        
        if pos == 0:
        	key = "pro:0"
        else:
        	key = "pro:" + str(pos)
        
        proxy = adapter.add(servant, broker.stringToIdentity(key))
        
        container.link(key, proxy)

        print('New processor ready: {}'.format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        
        container.unlink(key)


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
