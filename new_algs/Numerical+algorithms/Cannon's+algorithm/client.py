#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys

import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
import Cannon
import time
from matrix_utils import matrix_multiply

def load_matrix_from_file(filename):
    with file(filename) as f:
        rows = f.readlines()

    order = len(rows[0].split())
    retval = Cannon.Matrix(order, [])

    for row in rows:
        rowdata = row.split()
        assert len(rowdata) == order
        for n in rowdata:
            retval.data.append(float(n))

    assert len(retval.data) == order ** 2
    return retval


class Client(Ice.Application):
    def run(self, argv):
    	t_dist = 0;
    	t_secu = 0;
        loader = self.string_to_proxy(argv[1], Cannon.OperationsPrx)

        example = argv[2]

        A = load_matrix_from_file('m/{}A'.format(example))
        B = load_matrix_from_file('m/{}B'.format(example))
		t_dist = time.time()
        C = loader.matrixMultiply(A, B)
		t_dist = time.time() - t_dist
		
		t_secu = time.time()
		c = matrix_multiply(A,B)
		t_secu = time.time() - t_secu 
		
        expected = load_matrix_from_file('m/{}C'.format(example))

        retval = (C == expected)
        print("OK" if retval else "FAIL")
        print("El tiempo que ha tardado en distribuido ha sido {}".format(t_dist))
        print("El tiempo que ha tardado en secuencial ha sido {}".format(t_secu))
        
        if(C == None): print("Timeout expired")
        
        return not retval

    def string_to_proxy(self, str_proxy, iface):
        proxy = self.communicator().stringToProxy(str_proxy)
        retval = iface.checkedCast(proxy)
        if not retval:
            raise RuntimeError('Invalid proxy %s' % str_proxy)

        return retval

    def print_matrix(self, M):
        ncols = M.ncols
        nrows = len(M.data) / ncols

        for r in range(nrows):
            print M.data[r * ncols:(r + 1) * ncols]


if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))
