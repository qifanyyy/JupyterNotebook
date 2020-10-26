#!/usr/bin/python

import sys

from path import Path
from PlotGraph import PlotGraph
from ReadGraph import ReadGraph

if __name__ == '__main__':
	if not len(sys.argv) > 1:
		raise ValueError("Please enter the file to be read as an argument")
	
	inputFile = Path(sys.argv[1])

	r = ReadGraph(inputFile)
	graphMat = r.read()
	print "Analysing graph matrix..\n"
	print graphMat
	print "\nPlotting the graph.."
	p = PlotGraph(graphMat)
	p.plot()
