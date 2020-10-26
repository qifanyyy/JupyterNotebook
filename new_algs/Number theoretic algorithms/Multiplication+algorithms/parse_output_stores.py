#!/bin/python

import sys

infile = open(sys.argv[1]+"_stores.err", "r")
outfile = open(sys.argv[1]+"_stores.csv", "w")

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/float(n) # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    """Calculates the population standard deviation
    by default; specify ddof=1 to compute the sample
    standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5





l1_locality_list = []
l2_locality_list = []
l3_locality_list = []

outfile.write("L1 Stores, L1 Store Misses, L2 Store Hits, L3 Store Hits, L1 Store Locality, L2 Store Locality, LLC Store Locality\n")

while(1):
	line = infile.readline()
	if line.isspace():
		continue
        else:
		break

while(1):
	line = infile.readline()
        if not line:
		break
	if line.lstrip().split(' ', 1)[0] == 'Performance':
		continue
        if line.isspace():
		continue

        l1_stores = line.lstrip().split(' ',1)[0]
	l1_stores = l1_stores.replace(',', '')
        line = infile.readline()
        l1_store_misses = line.lstrip().split(' ',1)[0]
	l1_store_misses = l1_store_misses.replace(',', '')
        line = infile.readline()
        l2_store_hits = line.lstrip().split(' ',1)[0]
	l2_store_hits = l2_store_hits.replace(',', '')
        line = infile.readline()
        l3_store_hits = line.lstrip().split(' ',1)[0]
	l3_store_hits = l3_store_hits.replace(',', '')     
	line = infile.readline()
        line = infile.readline()
	

	l1_store_hits = int(l1_stores) - int(l1_store_misses)
	l1_store_locality = float(l1_store_hits)/float(l1_stores) 

	l2_store_locality = float(l2_store_hits)/float(l1_store_misses)

	l3_stores = int(l1_store_misses) - int(l2_store_hits)
 	l3_store_locality = float(l3_store_hits)/float(l3_stores)

	l1_locality_list.append(l1_store_locality)
	l2_locality_list.append(l2_store_locality)
	l3_locality_list.append(l3_store_locality)

	outfile.write(str(l1_stores) + ", " + str(l1_store_misses) + ", " + str(l2_store_hits) + ", " + str(l3_store_hits) + ", " + str(l1_store_locality) + ", " + str(l2_store_locality) + ", " + str(l3_store_locality) + "\n")



outfile.write("\n\n")


l1_locality_mean = mean(l1_locality_list)
l1_locality_stddev = stddev(l1_locality_list)
l1_locality_rel_sd = l1_locality_stddev * 100.00 / l1_locality_mean
outfile.write("L1 STORE LOCALITY, " + str(l1_locality_mean) + ", " + str(l1_locality_stddev) + ", " + str(l1_locality_rel_sd) + "%" + "\n")

l2_locality_mean = mean(l2_locality_list)
l2_locality_stddev = stddev(l2_locality_list)
l2_locality_rel_sd = l2_locality_stddev * 100.00 / l2_locality_mean
outfile.write("L2 STORE LOCALITY, " + str(l2_locality_mean) + ", " + str(l2_locality_stddev) + ", " + str(l2_locality_rel_sd) + "%" + "\n")

l3_locality_mean = mean(l3_locality_list)
l3_locality_stddev = stddev(l3_locality_list)
l3_locality_rel_sd = l3_locality_stddev * 100.00 / l3_locality_mean
outfile.write("L3 STORE LOCALITY, " + str(l3_locality_mean) + ", " + str(l3_locality_stddev) + ", " + str(l3_locality_rel_sd) + "%" + "\n")











