#!/usr/bin/python
# Perform regression test, comparing outputs of different johnson implementation
# Code adapted from https://github.com/cmu15418/asst3-s20/blob/master/code/regress.py

import argparse
import subprocess
import sys
import math
import os
import os.path
import getopt
from datetime import datetime

from graph import generate_graph, graphName

# General information

# Gold-standard reference program
standardProg = "./johnson_boost"

# Simulator being tested
testProg = "./johnson_seq"
ompTestProg = "./johnson_omp"
cudaTestProg = "./johnson_cuda"

# Directories
# graph files
dataDir = "./graphs"
# cache for holding reference solver results
cacheDir = "./regression-cache"

# Limit on how many mismatches get reported
mismatchLimit = 5

# Series of tests to perform.
# Each defined by:
#  nnode, nnedge, seed
regressionList = [
    (64,   200,    1),
    (512,  4000,   2),
    #(1024, 10000,  3),
]

def regressionName(params, standard = True, short = False, graphFileName = None):
    if graphFileName is not None:
        name = os.path.split(graphFileName)[-1]
    else:
        nnode, nedge, seed = params
        name = "n{}-e{}-s{}.txt".format(nnode, nedge, seed)
    if short:
        return name
    return ("ref" if standard else "tst") +  "-" + name

def regressionCommand(graphFileName, standard = True, threadCount = 1, gpu = False):
    #nnode, nedge, seed = params

    #graphFileName = graphName(nnode, nedge, seed)

    prog = ''
    prelist = []

    if standard:
        prog = standardProg
    elif gpu:
        prog = cudaTestProg
    elif threadCount > 1:
        prog = ompTestProg
    else:
        prog = testProg

    cmd = prelist + [prog, "-g", graphFileName]

    if standard:
        pass # any additional arg goes here
    elif gpu:
        pass # any additional arg goes here
    elif threadCount > 1:
        cmd += ["-t", str(threadCount)]

    cmd += ["-P"]

    return cmd

def runImpl(params, standard = True, threadCount = 1, gpu = False, graphFileName=None):
    if graphFileName is None:
        nnode, nedge, seed = params
        graphFileName = graphName(nnode, nedge, seed)

        if not os.path.exists(graphFileName):
            # generate graph
            sys.stderr.write("Generating graph: %s \n" % str(graphFileName))
            generate_graph(nnode, nedge, seed)

        pname = cacheDir + "/" + regressionName(params, standard)
    else:
        pname = cacheDir + "/" + regressionName(params, standard, graphFileName=graphFileName)

    cmd = regressionCommand(graphFileName, standard, threadCount, gpu)
    cmdLine = " ".join(cmd)

    try:
        outFile = open(pname, 'w')
    except Exception as e:
        sys.stderr.write("Couldn't open file '%s' to write.  %s\n" % (pname, e))
        return False
    try:
        sys.stderr.write("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "] " + "Executing " + cmdLine + " > " + regressionName(params, standard, graphFileName=graphFileName) + "\n")
        graphProcess = subprocess.Popen(cmd, stdout = outFile)
        graphProcess.wait()
        outFile.close()
    except Exception as e:
        sys.stderr.write("Couldn't execute " + cmdLine + " > " + regressionName(params, standard, graphFileName=graphFileName) + " " + str(e) + "\n")
        outFile.close()
        return False
    return True

def checkFiles(refPath, testPath):
    badLines = 0
    lineNumber = 0
    try:
        rf = open(refPath, 'r')
    except:
        sys.sterr.write("Couldn't open reference file '%s'\n" % refPath);
        return False
    try:
        tf = open(testPath, 'r')
    except:
        sys.stderr.write("Couldn't open test file '%s'\n" % testPath);
        return False
    while True:
        rline = rf.readline()
        tline = tf.readline()
        lineNumber +=1
        if rline == "":
            if tline == "":
                break
            else:
                badLines += 1
                sys.stderr.write("Mismatch at line %d.  File %s ended prematurely\n" % (lineNumber, refPath))
                break
        elif tline == "":
            badLines += 1
            sys.stderr.write("Mismatch at line %d.  File %s ended prematurely\n" % (lineNumber, testPath))
            break
        if rline[-1] == '\n':
            rline = rline[:-1]
        if tline[-1] == '\n':
            tline = tline[:-1]
        if rline != tline:
            badLines += 1
            if badLines <= mismatchLimit:
                sys.stderr.write("Mismatch at line %d.\n" % (lineNumber))
                # sys.stderr.write("Mismatch at line %d.  File %s:'%s'.  File %s:'%s'\n" % (lineNumber, refPath, rline, testPath, tline))
    rf.close()
    tf.close()
    if badLines > 0:
        sys.stderr.write("%d total mismatches.  Files %s, %s\n" % (badLines, refPath, testPath))
    return badLines == 0

def regress(params, threadCount, gpu, graphFileName=None):
    sys.stderr.write("+++++++++++++++++ Regression %s +++++++++++++++\n" % regressionName(params, standard=True, short=True, graphFileName=graphFileName))
    refPath = cacheDir + "/" + regressionName(params, standard = True, graphFileName = graphFileName)
    if not os.path.exists(refPath):
        if not runImpl(params, standard = True, gpu = False, graphFileName = graphFileName):
            sys.stderr.write("Failed to run with reference solver\n")
            return False

    if not runImpl(params, standard = False, threadCount = threadCount, gpu = gpu, graphFileName = graphFileName):
        sys.stderr.write("Failed to run with test solver\n")
        return False

    testPath = cacheDir + "/" + regressionName(params, standard = False, graphFileName = graphFileName)

    return checkFiles(refPath, testPath)

def run(flushCache, threadCount, gpu=False, graphFileName=None):

    if flushCache and os.path.exists(cacheDir):
        try:
            graphProcess = subprocess.Popen(["rm", "-rf", cacheDir])
            graphProcess.wait()
        except Exception as e:
            sys.stderr.write("Could not flush old result cache: %s" % str(e))
    if not os.path.exists(cacheDir):
        try:
            os.mkdir(cacheDir)
        except Exception as e:
            sys.stderr.write("Couldn't create directory '%s'" % cacheDir)
            sys.exit(1)
    goodCount = 0
    allCount = 0
    if graphFileName is not None:
        if regress(None, threadCount, gpu, graphFileName):
            sys.stderr.write("Regression %s Passed\n" % regressionName(None, standard = False, graphFileName = graphFileName))
            goodCount += 1
        else:
            sys.stderr.write("Regression %s Failed\n" % regressionName(None, standard = False, graphFileName = graphFileName))
        totalCount = 1
        allCount = 1
    else:
        rlist = regressionList
        for p in rlist:
            allCount += 1
            if regress(p, threadCount, gpu):
                sys.stderr.write("Regression %s Passed\n" % regressionName(p, standard = False))
                goodCount += 1
            else:
                sys.stderr.write("Regression %s Failed\n" % regressionName(p, standard = False))
        totalCount = len(rlist)
    message = "SUCCESS" if goodCount == totalCount else "FAILED"
    sys.stderr.write("Regression set size %d.  %d/%d tests successful. %s\n" % (totalCount, goodCount, allCount, message))

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", "--flushCache", action="store_true",
                    help="Clear expected result cache")
    parser.add_argument("-t", "--threadCount", type=int,
                    help="Specify number of OMP threads.\n If > 1, will run johnson-omp.  Else will run johnson-seq")
    parser.add_argument("-G", "--gpu", action="store_true",
                    help="Run johnson-cuda")
    parser.add_argument("-g", "--graphFileName", type=str,
                    help="Specify graph to run")

    args = parser.parse_args()

    threadCount = args.threadCount or 8
    flushCache = args.flushCache or False
    gpu = args.gpu or False
    graphFileName = args.graphFileName

    run(flushCache, threadCount, gpu, graphFileName)
