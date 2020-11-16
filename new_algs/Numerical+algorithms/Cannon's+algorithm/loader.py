#!/usr/bin/python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys

import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
Ice.loadSlice('-I {} container.ice'.format(Ice.getSliceDir()))
import Services
import Cannon
import math
import threading
import time

from matrix_utils import matrix_horizontal_shift, matrix_vertical_shift, matrix_split, matrix_join


class OperationsI(Cannon.Operations):
    def __init__(self, processors):
        self.order = int(math.sqrt(len(processors)))
        self.procesadores = processors
        	
        self.adapter = None; self.collector = None; self.collectorprx = None

    def matrixMultiply(self, A, B, current=None):
        self.adapter = current.adapter
        self.create_collector()
        self.init_processors()
        self.load_processors(A, B)

        retval = self.wait_for_result()

        self.destroy_collector()

        return retval

    def create_collector(self):
    	self.collector = CollectorI(self.order)
    	self.collectorprx = Cannon.CollectorPrx.checkedCast(self.adapter.addWithUUID(self.collector))

    def destroy_collector(self):
        self.adapter.remove(self.collectorprx.ice_getIdentity())
        del self.collector

    def init_processors(self):
    	above = 0; left = 0
    	row = 0; col = 0
    	
    	for i in range(len(self.procesadores)):
    		pro = row * self.order + col; above = (row - 1) * self.order + col; left = row * self.order + (col - 1)
    		
    		if (row - 1) < 0:
    			above = (self.order - 1) * self.order + col
    		if (col - 1) < 0:
    			left = row * self.order + (self.order - 1)
    			
    		self.procesadores[pro].init(row, col, self.procesadores[above], self.procesadores[left], self.order, self.collectorprx)
    		
    		if col == (self.order - 1):
    			col = 0
    			row = row + 1
    		else:
    			col = col + 1

    def load_processors(self, A, B):
        p_A = matrix_split(matrix_horizontal_shift(A, (A.ncols / self.order)), (A.ncols / self.order))
        p_B = matrix_split(matrix_vertical_shift(B, (A.ncols / self.order)), (A.ncols / self.order))
        
        for i in range(len(p_A)):
        	self.procesadores[i].begin_injectFirst(p_A[i], 0); self.procesadores[i].begin_injectSecond(p_B[i], 0)

    def wait_for_result(self):
        return self.collector.get_result()


class CollectorI(Cannon.Collector):
    def __init__(self, order):
        self.blocks = []; self.nblocks = 0;
        self.g_order = order
        self.C = Cannon.Matrix(order, [])
        self.event = threading.Event()
        
        for i in range(order ** 2):
        	self.blocks.append(None)

    def injectSubmatrix(self, block, row, col, current=None):
    	self.blocks[row * self.g_order + col] = block; self.nblocks += 1
    	
    	if(self.nblocks == (self.g_order ** 2)): self.event.set()

    def get_result(self):
        if(self.event.wait(self.g_order ** 2)):
            return matrix_join(self.blocks)
        else:
            return None


class Server(Ice.Application):
    def run(self, args):
        procesadores = []
        broker = self.communicator()
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
        while len(container.list()) != 25:
            time.sleep(1)	
        prox_procesadores = list(container.list().values())
        for i in range(len(prox_procesadores)):
        	procesadores.append(Cannon.ProcessorPrx.checkedCast(prox_procesadores[i]))
        servant = OperationsI(procesadores)
        adapter = broker.createObjectAdapter('LoaderAdapter')
        proxy = adapter.add(servant, broker.stringToIdentity("loader"))
        print('loader ready: {}'.format(proxy))
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
