#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright 2018(c). All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
# Author: Ing. Oraldo Jacinto Simon

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        absolute_import as _py3_abs_import)


class Edge(object):
    def __init__(self, source, sink, weight):
        self.source = source
        self.sink = sink
        self.capacity = weight

    def __repr__(self):
        return '%s => %s : %s ' %(self.source, self.sink, self.capacity)

class Flow(object):
    def __init__(self):
        self.adjacency = {}
        self.flow = {}

    def get_edges(self, source):
        '''Return adjacents

        '''
        return self.adjacency[source]

    def add_edge(self, source, sink, capacity):
        '''Add an edge to the flow

        '''
        if source == sink:
            raise ValueError('source == sink')
        edge = Edge(source, sink, capacity)
        redge = Edge(sink, source, capacity)
        edge.redge = redge
        redge.redge = edge
        if source not in self.adjacency:
            self.adjacency[source] = []
        if sink not in self.adjacency:
            self.adjacency[sink] = []

        self.adjacency[source].append(edge)
        self.adjacency[sink].append(redge)

        self.flow[edge] = 0
        self.flow[redge] = 0

###############################################################################
#Maximum Flow Ford-Fulkerson Algorithm
###############################################################################
    def find_augmentation_path(self, source, sink, path):
        '''A implementation of BFS version to find an augmentation path

        '''
        tail = [(source, path)]
        while tail:
            (source, path) = tail.pop(0)
            for e in self.get_edges(source):
                residual = e.capacity - self.flow[e]
                if residual > 0 and e not in path and e.redge not in path:
                    if e.sink == sink:
                        return path + [e]
                    else:
                        tail.append((e.sink, path + [e]))


    def maximum_flow(self, source, sink):
        '''A function for computing the maximum flow among a pair of nodes in a
        capacitated graph

        '''
        path = self.find_augmentation_path(source, sink, [])
        trace = []
        while path != None:
            residuals = [edge.capacity - self.flow[edge] for edge in path]
            flow = min(residuals)
            trace.append({'Path': path, 'Flow': flow})
            for e in path:
                self.flow[e] += flow
                self.flow[e.redge] -= flow
            path = self.find_augmentation_path(source, sink, [])
        res = sum(self.flow[e] for e in self.get_edges(source))
        return {'Trace': trace, 'Maximum_flow': res}
