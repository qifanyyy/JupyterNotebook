#
# Script to perform automated testing for assignment 1 of AA, 2017 semester 1
#
# The provided Python script will be the same one used to test your implementation.
# We will be testing your code on the core teaching servers (titan, jupiter etc), so please try your code there.
# The script first compiles your Java code, runs one of the two implementations then runs a series of test.
# Each test consists of sequence of operations to execute, whose results will be saved to file, then compared against
# the expected output.  If output from the tested implementation is the same as expected (script is tolerant for
# some formatting differences but if you don't change the IO functionality of the supplied files, you'll be fine), then we pass that test.
# Otherwise, difference will be printed via 'diff' (if in verbose mode, see below).
#
# Usage, assuming you are in the directory where the test script " assign1TestScript.py" is located.
#
# > python assign1TestScript.py [-v] <codeDirectory> <name of implementation to test> <data filename> <list of input files to test on>
#
#options:
#
#    -v : verbose mode
#
#Input:
#
#   code directory : directory where the Java files reside.  E.g., if directory specified is Assign1-s1234,
#        then Assign1-s1234/NearestNeighFileBased.java should exist.  This is also where the script
#        expects your program to be compiled and created in, e.g., Assign2-s1234/NearestNeighFileBased.class.
#   name of implementation to test: This is the name of the implementation to test.  The names
#        should be the same as specified in the script or in NearestNeighFileBased.java
#   data filename: This is the input data file consists of a list of point information.
#   input files: these are the input command files, where each file is a list of commands to execute.
#        IMPORTANT, the expected output file must be in the same directory
#        as the input files, and the should have the same basename - e.g., if we have input operation
#        file of "test1.in", then we should have expected files "test1.out".
#
#
# As an example, I can run the code like this when testing code directory "Assign1-s1234",
# the data file is named "sampleData.txt",
# all my input command and expected files are located in a directory called "tests"
# and named "test1.in" and testing for naive implementation:
#
#> python assign1TestScript.py -v   Assign1-s1234    naive    sampleData.txt    tests/test1.in
#
# Note that for each tests, the output will be stored within the code directory.  For example, above
# that would mean test1-naive.out will be created in Assign1-s1234.
#
#
#
# Jeffrey Chan, 2017
#

import string
import csv
import getopt
import os
import os.path
import re
import sys
import subprocess as sp


def main():

    # process command line arguments
    try:
        # option list
        sOptions = "v"
        # get options
        optList, remainArgs = getopt.gnu_getopt(sys.argv[1:], sOptions)
    except getopt.GetoptError, err:
        print >> sys.stderr, str(err)
        usage(sys.argv[0])

    bVerbose = False


    for opt, arg in optList:
        if opt == "-v":
            bVerbose = True
        else:
            usage(sys.argv[0])


    if len(remainArgs) < 4:
        usage(sys.argv[0])


    sOrigPath = os.getcwd()

    # code directory
    sCodeDir = os.path.abspath(remainArgs[0])
    # which implementation to test (see NearestNeighFileBased.java for the implementation strings)
    sImpl = remainArgs[1]
    # data file name
    sDataFile = os.path.join(sOrigPath, remainArgs[2])
    # set of input files that contains the operation commands
    lsInFile = remainArgs[3:]


    # check implementation
    setValidImpl = set(["naive", "kdtree"])
    if sImpl not in setValidImpl:
        print >> sys.stderr, sImpl + " is not a valid implementation name."
        sys.exit(1)


    # compile the skeleton java files
    sCompileCommand = "javac NearestNeighFileBased.java"
    sExec = "NearestNeighFileBased"

    # whether executable was compiled and constructed
    bCompiled = False

    os.chdir(sCodeDir)


    # compile
    proc = sp.Popen(sCompileCommand, shell=True, stderr=sp.PIPE)
    (sStdout, sStderr) = proc.communicate()
    print sStderr

    # check if executable was constructed
    if not os.path.isfile(sExec + ".class"):
        print >> sys.stderr, sExec + ".java didn't compile successfully."
    else:
        bCompiled = True


    # variable to store the number of tests passed
    passedNum = 0
    lsTestPassed = []
    print ""

    if bCompiled:
        # loop through each input test file
        for (j, sInLoopFile) in enumerate(lsInFile):
            sInFile = os.path.join(sOrigPath, sInLoopFile)
            sTestName = os.path.splitext(os.path.basename(sInFile))[0]
            sOutputFile = os.path.join(sCodeDir, sTestName + "-" + sImpl + ".out")
            sExpectedFile = os.path.splitext(sInFile)[0] + ".exp"

            # check if expected files exist
            if not os.path.isfile(sExpectedFile):
                print >> sys.stderr, sExpectedFile + " is missing."
                continue


            sCommand = os.path.join("java " + sExec + " " + sImpl + " \"" + sDataFile + "\" \"" + sInFile + "\" \"" + sOutputFile + "\"")
            print sCommand

            if bVerbose:
                print "Testing: " + sCommand
            proc = sp.Popen(sCommand, shell=True, stderr=sp.PIPE)

            (sStdout, sStderr) = proc.communicate()

            if bVerbose and len(sStderr) > 0:
                print >> sys.stderr, "\nWarnings and error messages from running java program:\n" + sStderr

            # compare expected with output
            bPassed = evaluate(sExpectedFile, sOutputFile)
            if bPassed:
                passedNum += 1
                lsTestPassed.append(sTestName)
            else:
                # print difference if failed
                if bVerbose:
                    print >> sys.stderr, "Difference between output and expected:"
                    proc = sp.Popen("diff -y " + sOutputFile + " " + sExpectedFile, shell=True)
                    proc.communicate()
                    print >> sys.stderr, ""


    # change back to original path
    os.chdir(sOrigPath)

    print "\nSUMMARY: " + sExec + " has passed " + str(passedNum) + " out of " + str(len(lsInFile)) + " tests."
    print "PASSED: " + ", ".join(lsTestPassed) + "\n"

########################################################################################################################

def evaluate(sExpectedFile, sOutputFile):
    """
    Evaluate if the output is the same as expected input for the vertices operation.
    """

    lExpMatches = []
    lActMatches = []

    with open(sExpectedFile, "r") as fExpected:
        # should only be one line
        for sLine in fExpected:
            # space delimiter
            sLine1 = sLine.strip()
            lFields = re.split("[\t ]*[,|\|]?[\t ]*", sLine1)
            lExpMatches.extend(lFields)


    with open(sOutputFile, "r") as fOut:
        # should only be one line
        for sLine in fOut:
            # space delimiter
            sLine1 = sLine.strip()

            # if line is empty, we continue (this also takes care of extra newline at end of file)
            if len(sLine1) == 0:
                continue
            # should be space-delimited, but in case submissions use other delimiters
            lFields = re.split("[\t ]*[,|\|]?[\t ]*", sLine1)
            lActMatches.extend(lFields)

    setExpMatches = set(lExpMatches)
    setActMatches = set(lActMatches)



    # if there are differences between the sets
    if len(setExpMatches.symmetric_difference(setActMatches)) > 0:
        return False


    # passed
    return True


def usage(sProg):
    print >> sys.stderr, sProg + " [-v] <code directory> <name of implementation to test> <input data file> <list of test comamnd files>"
    sys.exit(1)


if __name__ == "__main__":
    main()
