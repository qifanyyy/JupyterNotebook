#!/usr/bin/env python3
#
info = """
XfoilTalk

    A library to simplify and programmatically interface with xfoil.

Author: Kevin R. Johnson
Email: Kevin@KevinJohnsonAviation.com
Copyright (C) 2015 Kevin R. Johnson 
Released under the GNU General Public License v3.0

    XfoilTalk, of which this file is part of, is free software: 
    you can redistribute it and/or modify it under the terms of the 
    GNU General Public License as published by the Free Software Foundation, 
    either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    A copy of the GNU General Public License is available at:
    https://www.gnu.org/licenses/gpl-3.0.txt
"""

### Import useful libraries
import sys, re, subprocess, string, atexit
try:
   import cPickle as pickle
except:
   import pickle

### Lets set some xfoil stuff
# Where is xfoil?
xfoil = subprocess.check_output('which xfoil', shell=True).strip()
# Set xfoil "global" parameters:
Iter = 50
Panels = 250
NCrit = 9.00
ASEQ = {'Min':1,'Max':'18', 'Step':'0.1'}
PlotSettings = {'Alfa':{'Min':'0.00', 'Max':'18.0', 'Step':'2.00'},
                'CL'  :{'Min':'0.000', 'Max':' 2.5', 'Step':'0.50'},
                'CD'  :{'Min':'0.000', 'Max':'0.04', 'Step':'0.01'},
                'CM'  :{'Min':'-0.25', 'Max':'0.00', 'Step':'0.05'}}
# Now lets pack some of this for convenience...
def setVarsStr(ReynoldsNumber):
    return string.join(["ppar","n",str(Panels),"\n","panel","oper","iter "+ str(Iter),"vpar","n",str(NCrit),""],'\n')

# Get prior results / build prior result dictionary:
# Significantly speeds up the runtime for GA-airplane-designer
try:
    priorCLmaxResultsFile = open( "saveCLmax.pkl", "rb" )
    priorCLmaxResults = pickle.load( priorCLmaxResultsFile )
    priorCLmaxResultsFile.close()
except:
    priorCLmaxResults = {}
    
try:
    priorGetDataResultsFile = open( "saveGetData.pkl", "rb" )
    priorGetDataResults = pickle.load( priorGetDataResultsFile )
    priorGetDataResultsFile.close()
except:
    priorGetDataResults = {}

### Let's define some useful functions!

# Save the prior results for later when the program exits.
def atExitFunct():
    priorCLmaxResultsFile = open( "saveCLmax.pkl", "wb" )
    pickle.dump(priorCLmaxResults, priorCLmaxResultsFile)
    priorGetDataResultsFile = open( "saveGetData.pkl", "wb" )
    pickle.dump(priorGetDataResults, priorGetDataResultsFile)
    priorCLmaxResultsFile.close()
    priorGetDataResultsFile.close()
# Don't indent this!  This is the library that registeres the above to run at close.
atexit.register(atExitFunct)

##  A handy thing to get a value from the xfoil output.
def GrepVals(ValKeyStr, StrToGrep):
    if re.findall('Type "!" to continue iterating', StrToGrep) != []:
        return 'DNE'
    try: 
        return float(re.findall(str(ValKeyStr)+" = *([ ,-][0-9]+.[0-9]+)", StrToGrep)[-1])
    except:
        print( re.findall(str(ValKeyStr)+" = *([ ,-][0-9]+.[0-9]+)", StrToGrep))

## Get the correct load for the airfoil either internally generated NACA or "load file"
def GetAirfoilLoadCmd(airfoil):
    # Figure out how to command the airfoil we want to load...
    if re.match("[N,n][A,a][C,c][A,a] ", airfoil) == None:
        return "load " + str(airfoil)
    else:
        return str(airfoil)

## Puts a flap on
def Flap(HingeX = 1, HingeY = 0, FlapAngle = 0):
        return string.join(["gdes", "flap {0} {1} {2}".format(HingeX, HingeY, FlapAngle), "plot", "exec",""],'\n')

## Solve for the aerodynamic variables of the airfoil at a set Reynolds Number
#  and a select other value, i.e., CL = 0.02 for example, or alfa = 2.
def GetData(airfoil, ReynoldsNumber, FromValStr, FromVal, HingeX=1, HingeY=0, FlapAngle=0):
    try:
        returnDict = priorGetDataResults[(airfoil, ReynoldsNumber, FromValStr, FromVal, HingeX, HingeY, FlapAngle)]
    except:
        # Start xfoil,
        xfoilProc = subprocess.Popen([xfoil], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Communicate the command sequence to xfoil,
        outputString = xfoilProc.communicate( string.join([
            GetAirfoilLoadCmd(airfoil),
            Flap(HingeX,HingeY,FlapAngle),
            setVarsStr(ReynoldsNumber),
            str(FromValStr) + " " + str(FromVal),
            'visc ' + str(ReynoldsNumber),
            str(FromValStr) + " " + str(FromVal)
        ], '\n'))[0]
        # Get all the solved parameters
        returnDict = {}
        returnDict["airfoil"] = str(airfoil)
        returnDict["re"] = ReynoldsNumber
        returnDict["HingeX"] = HingeX
        returnDict["HingeY"] = HingeY
        returnDict["FlapAngle"] = FlapAngle
        returnDict["a"] = GrepVals("a", outputString)
        returnDict["CL"] = GrepVals("CL", outputString)
        returnDict["Cm"] = GrepVals("Cm", outputString)
        returnDict["CD"] = GrepVals("CD", outputString)
        returnDict["CDf"] = GrepVals("CDf", outputString)
        returnDict["CDp"] = GrepVals("CDp", outputString)
        priorGetDataResults[(airfoil, ReynoldsNumber, FromValStr, FromVal, HingeX, HingeY, FlapAngle)] = returnDict
    return returnDict
   
## Lets get the polar for a airfoil at a given Reynolds number.
def PlotPolar(airfoil, ReynoldsNumber, ASEQstart=ASEQ['Min'], ASEQstep=ASEQ['Step'], ASEQmax=ASEQ['Max'], HingeX=1, HingeY=0, FlapAngle=0):
    xfoilProc = subprocess.Popen([xfoil], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    xfoilProc.communicate( string.join([
        GetAirfoilLoadCmd(airfoil),
        Flap(HingeX,HingeY,FlapAngle),
        setVarsStr(ReynoldsNumber),
        "alfa " + str(ASEQstart),
        'visc ' + str(ReynoldsNumber),
        "alfa " + str(ASEQstart),
        "type 2",
        "pacc","","",
        "aseq " + str(ASEQstart) + " " + str(ASEQmax) + " " + str(ASEQstep),
        "pacc",
        "ppax",
        PlotSettings['Alfa']['Min'] + " " + PlotSettings['Alfa']['Max'] + " " + PlotSettings['Alfa']['Step'],
        PlotSettings['CL']['Min'] + " " + PlotSettings['CL']['Max'] + " " + PlotSettings['CL']['Step'],
        PlotSettings['CD']['Min'] + " " + PlotSettings['CD']['Max'] + " " + PlotSettings['CD']['Step'],
        PlotSettings['CM']['Min'] + " " + PlotSettings['CM']['Max'] + " " + PlotSettings['CM']['Step'],
        "pplot",
        "hard"      
    ], '\n'))
    subprocess.call(['mv plot.ps '+ re.sub(" ", "_", str(airfoil))+'_Rn{:.0e}'.format(ReynoldsNumber)+'_Polar.ps'], shell=True)

def PlotFoil(airfoil, HingeX=1, HingeY=0, FlapAngle=0):
    xfoilProc = subprocess.Popen([xfoil], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    xfoilProc.communicate( string.join([
        GetAirfoilLoadCmd(airfoil),
        Flap(HingeX,HingeY,FlapAngle),
        'panel',
        'gdes',
        'hard'], '\n'))
    subprocess.call(['mv plot.ps '+ re.sub(" ", "_", str(airfoil)) +'_Section.ps'], shell=True)

def CLmaxSearch(airfoil, ReynoldsNumber, HingeX=1, HingeY=0, FlapAngle=0, 
                LowerBound=1.0, UpperBound=4.0, DiffLim = 0.05):
    try:
        sol = priorCLmaxResults[(airfoil,ReynoldsNumber,HingeX,HingeY,FlapAngle)]
    except KeyError:
        while True:
            #print( "\tBounds now [{0},{1}]".format(LowerBound, UpperBound))
            if (UpperBound - LowerBound)/UpperBound > DiffLim:
                midpoint = (LowerBound + UpperBound)/2.0
                try:
                    sol = GetData(airfoil, ReynoldsNumber, 'cl', midpoint, HingeX, HingeY, FlapAngle)
                    float(sol["CL"])
                    LowerBound = midpoint
                except:
                    UpperBound = midpoint
            else:
                priorCLmaxResults[(airfoil,ReynoldsNumber,HingeX,HingeY,FlapAngle)] = sol
                break
    return sol

# Demonstrate usage...
if __name__ == "__main__":
    print( info)
    #print( GetData('naca 23015', 3e6, 'a', 4))
    #print( GetData('naca 23015', 3e6, 'cl', 1.8))
    #print( GetData('naca 0015', 3e6, 'a', 2, 0.8, 0, 30))
    #PlotPolar('naca 23015', 3e6)
    #PlotFoil('naca 0015')
    #PlotFoil('naca 0015', 0.8, 0, 30)
    #print( "{} has CLmax = {}".format("NACA 23015", CLmaxSearch('naca 23015', 3e6)))
    #print( "{} has CLmax = {}".format("NACA 23015 w/ flap", CLmaxSearch('naca 23015', 3e6, 0.7, 0, 30)))
    
