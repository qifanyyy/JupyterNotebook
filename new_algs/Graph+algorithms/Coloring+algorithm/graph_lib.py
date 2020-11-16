# This file includes the Python side of communicating functions between C++ and Python. 
# CTypes is used for the communication.

import ctypes
import os
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

class Graph_Lib(object):
    def __init__(self):
        self.lib = ctypes.cdll.LoadLibrary('./source/lib_graph.so')
        # graph constructors and destructors
        self.lib.insert_batch.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.lib.insert_batch.restype = ctypes.POINTER(ctypes.c_int)
        self.lib.reset_batch.argtypes = []
        self.lib.read_batch.argtypes = [ctypes.c_char_p]
        self.lib.read_batch.restype = ctypes.POINTER(ctypes.c_int)
        # embedding init
        self.lib.init_node_embeddings.argtypes = []
        self.lib.init_graph_embeddings.argtypes = []
        # embedding update
        self.lib.update_graph_embeddings.argtypes = []
        # getters
        self.lib.get_node_embed.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        self.lib.get_node_embed.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_float))
        self.lib.get_graph_embed.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self.lib.get_graph_embed.restype = ctypes.POINTER(ctypes.c_float)
        self.lib.get_batch_filenames.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.lib.get_batch_filenames.restype = ctypes.POINTER(ctypes.c_char_p)
        # coloring of batch
        self.lib.color_batch.argtypes = [ctypes.POINTER(
            ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        self.lib.color_batch.restype = ctypes.POINTER(ctypes.c_int)
        
        # self.lib.update_node_embeddings.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]

    def insert_batch(self, batch, min_n, max_n):
        # batch many graphs are constructed with nodes in given interval [min_n, max_n]
        nodes = self.lib.insert_batch(batch, min_n, max_n)
        return nodes[:batch]

    def reset_batch(self):
        # values in C++ about the batch are reset
        self.lib.reset_batch()

    def read_batch(self, path):
        # all the matrix files in the given path are read and set as a whole batch of graphs
        a = ctypes.c_int(0)
        location = ctypes.c_char_p(path.encode('utf-8'))
        nodes = self.lib.read_batch(location, ctypes.byref(a))
        return nodes[:a.value]

    def init_node_embeddings(self):
        # node embeddings are initialized
        self.lib.init_node_embeddings()

    def init_graph_embeddings(self):
        # graph embedings are initialized
        self.lib.init_graph_embeddings()

    def update_graph_embeddings(self):
        # graph embeddings are updated
        self.lib.update_graph_embeddings()

    def get_node_embed(self, index):
        # node embedding is retrieved for single graph in batch specified with index
        a = ctypes.c_int(0) # row size of node embedding matrix
        b = ctypes.c_int(0) # column size of node embedding matrix
        res = self.lib.get_node_embed(index, ctypes.byref(a), ctypes.byref(b))
        arr = []
        for r in range(a.value): # all the embedding values are copied to a 2D list named arr
            temp = []
            for c in range(b.value):
                val = res[r][c]
                temp.append(val)
            arr.append(temp)
        return np.array(arr)

    def get_graph_embed(self, index):
        # graph embedding is retrieved for single graph in batch specified with index
        a = ctypes.c_int(0) # size of the embedding list
        res = self.lib.get_graph_embed(index, ctypes.byref(a))
        return np.array(res[:a.value]) # since return from c++ is a pointer, a limitation to the parameter is required
    
    def get_batch_filenames(self):
        # if a batch is created from actual matrix files, then the filenames of all the graphs in batch is got
        a = ctypes.c_int(0)
        res = self.lib.get_batch_filenames(ctypes.byref(a)) # filenames of each graph is returneds
        return np.array(res[:a.value])

    def color_batch(self, nodes):
        # calls C++ coloring functon for the selected nodes in the nodes array for each graph in batch
        a = ctypes.c_int(0)
        start = (ctypes.c_int * len(nodes))(*nodes)
        res = self.lib.color_batch(start, ctypes.byref(a)) # colors selected for each graph is returned
        return np.array(res[0:a.value])

