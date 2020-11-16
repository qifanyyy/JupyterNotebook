# -*- mode:python; coding:utf-8; tab-width:4 -*-

import math
import Cannon
import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))


def matrix_multiply(A, B):
    order = A.ncols
    C = Cannon.Matrix(order, [])
	for r in range(order):
		for c in range(order):
			cell = 0
			for i in range(order):
				cell += A.data[(r * order) + i] * B.data[(i * order) + c]
			C.data.append(cell)

    return C


def matrix_add(A, B):
    order = A.ncols
    C = Cannon.Matrix(order, [])

	for i in range(order ** 2):
		C.data.append(A.data[i] + B.data[i])

    return C


def matrix_horizontal_shift(M, block_order):
    order = M.ncols
    retval = Cannon.Matrix(order, [])

    for i in range(order ** 2):
    	retval.data.append(0)

    for row in range(block_order):
    	for col in range(order):
    		retval.data[row*order + col] = M.data[row*order + col]

    for row in range(block_order, order):
    	salto = int(row/block_order)
    	for col in range(order):
    		mov = ((col + order - salto * block_order) % order)
    		retval.data[row * order + mov] = M.data[row * order + col]

    return retval


def matrix_vertical_shift(M, block_order):
	order = M.ncols
	retval = Cannon.Matrix(order, [])

    for i in range(order ** 2):
    	retval.data.append(0)
    	
    for col in range(block_order):
    	for row in range(order):
    		retval.data[row*order + col] = M.data[row*order + col]
    		
    for col in range(block_order, order):
    	salto = int(col/block_order)
    	for row in range(order):
    		mov = ((row + order - salto * block_order) % order)
    		retval.data[mov * order + col] = M.data[row * order + col]
    		
    return retval


def matrix_split(M, block_order):
	order = M.ncols

    blocks = []

    nbl = order / block_order
    m = []
    
    for ind_by in range(nbl):
    	for ind_bx in range(nbl):
    		pos = (ind_bx * block_order) + (ind_by * (block_order * order))
    		for ind_c in range(block_order):
    			for inc in range(block_order):
    				m.append(M.data[pos + (ind_c * order) + inc])
    		blocks.append(Cannon.Matrix(block_order, m))
    		m = []
    
    return blocks
    
def list_split (M, block_order):
	order = len(M)
	
	blocks = []
	
	nbl = order / block_order
	m = []
	
	for ind_bx in range(nbl):
		for inc in range(block_order):
			m.append(M[(ind_bx * block_order) + inc])
		blocks.append(m)
		m = []
	
	return blocks

def matrix_join(blocks):

    nbl = int(math.sqrt(len(blocks)))
    block_order = blocks[0].ncols
    order = nbl * block_order
    
    M = Cannon.Matrix(order, [])
    
    for nveces in range(nbl):
    	for ind_y in range(block_order):
    		pos = ind_y * block_order 
    		block = nveces * nbl
    		for ind_x in range(nbl):
    			for inc in range(block_order):
    				M.data.append(blocks[block].data[pos + inc])
    			block = block + 1
    
    return M
    
    
