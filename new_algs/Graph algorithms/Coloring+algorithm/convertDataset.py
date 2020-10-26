import os
import sys
# Converts dataset taken from http://networkrepository.com/ to the format used by our colorer
# Usage: python3 convertDataset.py <inputFile> [outputFile]
# [outputFile] optional

def detectnnodesnedges(line):
	splt = line.strip('/n').split(sep=' ')
	tmplist = list()
	for el in splt:
		try:
			tmplist.append(int(el))
		except ValueError:
			pass
	return(min(tmplist), max(tmplist))

def detectifweighted(infilename):
	with open(infilename, "r") as inF:
		l = inF.readline()		# Jump header
		l = inF.readline()		# jump nnodes nedges
		l = inF.readline()
		splt = l.strip('\n').split(sep=' ')
		return len(splt)

def convertGraphFile(infilename, outfilename):
	nfields = detectifweighted(infilename)
	with open(outfilename, "w") as outF:
		with open(infilename, "r") as inF:
			l = inF.readline()		# Jump header
			l = inF.readline()

			nnodes, nedges = detectnnodesnedges(l)
			outF.write(str(nnodes) + ' ' + str(nedges) + '\n')

			# 2 fields in original file
			if nfields == 2:
				for line in inF:
					outF.write(line.strip('\n') + ' 0.1\n')
			# weighted graph (3 fields in original file)
			elif nfields == 3:
				for line in inF:
					outF.write(line)
			# more than 3 fields in the original file
			elif nfields > 3:
				for line in inF:
					splt = line.strip('\n').split(sep=' ')
					outF.write(" ".join(splt[0:3]))


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: python3 convertDataset.py <inputFile> [outputFile]")
		exit(-1)
	infilename = sys.argv[1]
	if len(sys.argv) > 2:
		outfilename = sys.argv[2]
	else:
		ll = infilename.split(sep=os.sep)
		tt = ll[-1].split(sep='.')
		tout = tt[0] + '_converted'
		tt[0] = tout
		newtt = ".".join(tt)
		ll[-1] = newtt
		outfilename = os.sep.join(ll)
	convertGraphFile(infilename, outfilename)
