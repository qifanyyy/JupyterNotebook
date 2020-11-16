#!/usr/bin/env python3
#
info = """
GA-airplane-designer
    A program to produce rough aircraft designs optimized to a given fitness 
    function from a selection of engines, airfoils, and design unique geometry
    by utilizing a genetic algorithm.
    
Author: Kevin R. Johnson
Email: Kevin@KevinJohnsonAviation.com
Copyright (C) 2015 Kevin R. Johnson 
Released under the GNU General Public License v3.0

    GA-airplane-designer, of which this file is part of, is free software: 
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
## Import my custom libraries...
import Airplane     # Do customize payload and cruise alt to suit.   
## Import useful python libraries...
import math, random, sys, time
try:
   import cPickle as pickle
except:
   import pickle

### Data we will build aircraft from
## Geometry limits:
GeoLims = {'Chord':(2.5, 7),\
           'Span':(10, 34),\
           'FlapX':(0.8, 0.8),\
           'FlapAngle':(20.0, 20.0),\
           'FuseBoxLen':(90.0/12.0, 100.0/12.0),\
           'FusePyramidLen':(4.0, 18.0),\
           'FuseWidth':(2.0, 2.0),\
           'FuseHeight':(3.0,3.0),\
           'HTailChord':(1.0, 4.0),\
           'VTailChord':(1.0, 4.0),\
           'HTailSpan':(4.0, 10.0),\
           'VTailSpan':(2.0, 6.0),\
           'MGTW':(1600.0, 1600.0),\
           'Payload':(250.0, 250.0),\
           'CruiseAlt':(10000, 10000),\
           'ExtrasWeight':(60, 60)}
## Airfoils for XFoil to use on the main wing.
Airfoils= [{'name':'Clark Y', 'file':'clarky.dat'}, \
           {'name':'NLF 0414F', 'file':'NLF-0414F.dat'}, \
           {'name':'NLF 0115', 'file':'nlf0115.dat'}, \
           {'name':'NLF 0215F', 'file':'nlf0215f.dat'}, \
           #{'name':'NLF 1015', 'file':'nlf1015.dat'}, \
           {'name':'NLF 415', 'file':'nlf415.dat'}, \
           {'name':'P-51 Tip', 'file':'p51dtip.dat'}, \
           {'name':'NACA 63215', 'file':'n63215.dat'}, \
           {'name':'NACA 23012', 'file':'naca 23012'}, \
           {'name':'NACA 23008', 'file':'naca 23008'}, \
           {'name':'NACA 4412', 'file':'naca 4412'}, \
           {'name':'NACA 2412', 'file':'naca 2412'}]
## Airfoils for XFoil to use on the tail
TailFoils=[{'name':'NACA 0008', 'file':'naca 0008'}, \
           {'name':'NACA 0012', 'file':'naca 0012'}]
## Material data:
# Units are feet and lb/ft**3
Sheets = [{'name':'6061-T6', 'thick':0.025 / 12, 'density':0.0975 * (12**3)}]
## Engine Data.
# Rotax 912ULS: http://www.rotaxservice.com/rotax_engines/rotax_912ULSs.htm
# Rotax 914ULS: http://www.rotaxservice.com/rotax_engines/rotax_914ULs.htm
# http://easa.europa.eu/system/files/dfu/EASA-TCDS-E.122_BRP--Powertrain_Rotax_914_series_engines-03-26022010_.pdf
# All below have 60lb of accessories added to the listed dry weight.
# C-85: http://en.wikipedia.org/wiki/Continental_O-190  
# Lycoming O-320: http://en.wikipedia.org/wiki/Lycoming_O-320#Specifications_.28O-320-A1A.29
# Lycoming O-360: http://en.wikipedia.org/wiki/Lycoming_O-360#Specifications_.28O-360-A1A.29
Engines = [{'name':'Rotax 912ULS', 'HP': 95, 'weightLb':140.6,  'GPH':7.0, 'critAlt':0}, \
           {'name':'Rotax 914UL',  'HP':100, 'weightLb':166.4,  'GPH':7.5, 'critAlt':16000}, \
#           {'name':'Cont C-85',    'HP': 85, 'weightLb':180+60, 'GPH':5.4, 'critAlt':0}, \
           {'name':'Lyc O-320',    'HP':150, 'weightLb':244+60, 'GPH':9,   'critAlt':0}, \
           {'name':'Lycom O-360',  'HP':180, 'weightLb':258+60, 'GPH':10,  'critAlt':0},\
           {'name':'80HP VW',      'HP':80,  'weightLb':161,    'GPH':5,   'critAlt':0}]

### Lets define some useful functions:
## Returns 1 if variable in desired range or is variable equal to ValElse, else return 0
def AccVarRange(VarToEval, VarLowerLimit, VarUpperLimit):
    if (VarLowerLimit <= VarToEval) and (VarToEval <= VarUpperLimit):
        return 1.0
    else:
        return 0.0

## Return the value of the product of all the elements in a list.
def MultiplyElements(l):
    p = 1
    for i in l:
        p = i * p
    return p

## The design evaluation & fitness function
# CUSTOMIZE THIS to fit the mission you want performed.
def FitnessFunction(airplane):
    S = [1.0]
    ## Compute safety / stability acceptability coefficients:
    # Is stall speed acceptable?
    S.append(AccVarRange(airplane.Vs, 0.0, 61.0))
    # Is there sufficient vertical tail?
    S.append(AccVarRange(airplane.Vv, 0.02, 0.05))
    # Is there sufficient horizontal tail?
    S.append(AccVarRange(airplane.Vh, 0.30, 0.60))
    # Compute the overall safety/stability coefficient
    S = MultiplyElements(S)
    
    # Compute climb performance
    C = [1.0]
    # Pparam
    C.append(AccVarRange(airplane.Pparam, 0, 200))
    # Rate of climb in fpm
    C.append( min(1.0, max(0, (750.0 - airplane.Vz)/(750.0 - 1500.0))) )
    # Estimated Ceiling
    C.append(AccVarRange(airplane.Zmax, 15000, 60000))
    # Compute overall climb acceptability
    C = MultiplyElements(C)
       
    ## Compute the mission fitness which we wish to maximize
    # In this example we'll score higher points for less time on a 1,300nmi flight
    # assume each stop costs 1 hour
    DistToFly = 1300.0
    TimePerStop = 1.0
    NoStopTimeEnroute = DistToFly / airplane.Vc
    Stops = math.ceil(DistToFly / airplane.RangeVFRcruise)
    StopsTime = Stops * TimePerStop
    FlightTime = NoStopTimeEnroute + StopsTime
    UpperTime = 16.0    # Max time enroute beyond which no points awarded
    LowerTime = 6.0   # Time enoute below which no extra points awarded 
    U = min(1.0, max(0, (UpperTime - FlightTime)/(UpperTime - LowerTime)))
    
    # If the airplane is "unsafe" return zero, otherwise return the utility of the design
    return S * C * U

def MakeRandomAirplane(name):
    A = Airplane.Airplane(name,\
        random.choice(Engines),\
        random.choice(Airfoils),\
        random.uniform(*GeoLims['Chord']),\
        random.uniform(*GeoLims['Span']),\
        random.uniform(*GeoLims['FlapX']),\
        random.uniform(*GeoLims['FlapAngle']),\
        random.uniform(*GeoLims['FuseBoxLen']),\
        random.uniform(*GeoLims['FusePyramidLen']),\
        random.uniform(*GeoLims['FuseWidth']),\
        random.uniform(*GeoLims['FuseHeight']),\
        random.choice(TailFoils),\
        random.uniform(*GeoLims['HTailChord']),\
        random.uniform(*GeoLims['VTailChord']),\
        random.uniform(*GeoLims['HTailSpan']),\
        random.uniform(*GeoLims['VTailSpan']),\
        random.uniform(*GeoLims['MGTW']),\
        random.choice(Sheets),\
        random.uniform(*GeoLims['Payload']),\
        random.uniform(*GeoLims['CruiseAlt']),\
        random.uniform(*GeoLims['ExtrasWeight']))
        
    return (FitnessFunction(A), A)

def SpawnAirplanes(name, A1, A2, pMut=1.0/25.0):
    Genome = (name,)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].Engine,)
    else: Genome += (random.choice(Engines),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].Airfoil,)
    else: Genome += (random.choice(Airfoils),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].Chord,)
    else: Genome += (random.uniform(*GeoLims['Chord']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].Span,)
    else: Genome += (random.uniform(*GeoLims['Span']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].FlapX,)
    else: Genome += (random.uniform(*GeoLims['FlapX']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].FlapAngle,)
    else: Genome += (random.uniform(*GeoLims['FlapAngle']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].FuseBoxLen,)
    else: Genome += (random.uniform(*GeoLims['FuseBoxLen']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].FusePyramidLen,)
    else: Genome += (random.uniform(*GeoLims['FusePyramidLen']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].FuseWidth,)
    else: Genome += (random.uniform(*GeoLims['FuseWidth']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].FuseHeight,)
    else: Genome += (random.uniform(*GeoLims['FuseHeight']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].TailFoil,)
    else: Genome += (random.choice(TailFoils),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].HTailChord,)
    else: Genome += (random.uniform(*GeoLims['HTailChord']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].VTailChord,)
    else: Genome += (random.uniform(*GeoLims['VTailChord']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].HTailSpan,)
    else: Genome += (random.uniform(*GeoLims['HTailSpan']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].VTailSpan,)
    else: Genome += (random.uniform(*GeoLims['VTailSpan']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].MGTW,)
    else: Genome += (random.uniform(*GeoLims['MGTW']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].Sheet,)
    else: Genome += (random.choice(Sheets),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].Payload,)
    else: Genome += (random.uniform(*GeoLims['Payload']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].CruiseAlt,)
    else: Genome += (random.uniform(*GeoLims['CruiseAlt']),)
    if random.random() > pMut: Genome += (random.choice([A1, A2])[1].ExtrasWeight,)
    else: Genome += (random.uniform(*GeoLims['ExtrasWeight']),)
    
    A = Airplane.Airplane(*Genome)    
    return (FitnessFunction(A), A)

def ProgBar(curVal, maxVal, timeStart, barLen=30):
    curProg = 1.0*curVal / maxVal
    timeNow = time.time()
    dt = timeNow - timeStart
    try:
        print("\r[{0}{1}] @ {2} of {3}: <sec/Iter>= {4:1.3f}, Est. time-to-go: {5:1.2f} sec.   ".format('#'*int(barLen*curProg), ' '*(barLen-int(barLen*curProg)), curVal, maxVal, dt/curVal, (dt/curVal)*(maxVal - curVal)), end="")
    except:
        print("\r[{0}] @ {1} of {2}".format(' '*barLen, 0, maxVal), end="")
    if curVal == maxVal:
        print("")
        
if __name__ == "__main__":
    print( info)
    #random.seed(1336765201) # just made up a number so I can reproduce runs.
    DesignIDnum = 0
    ## Settings for the genetic algorithm
    # Try to pick up where we last left off if we can...
    try:
        print( "Attempting Resume/Import.")
        finalDesignsPickleFile = open('FinalDesigns.pkl', 'rb')
        PopSize = pickle.load(finalDesignsPickleFile)
        BreederSize = pickle.load(finalDesignsPickleFile)
        Generations = int(sys.argv[1])
        Population = pickle.load(finalDesignsPickleFile)
        BestSoFar = pickle.load(finalDesignsPickleFile)
        DesignIDnum = pickle.load(finalDesignsPickleFile)
        state = pickle.load(finalDesignsPickleFile)
        random.setstate(state)
        finalDesignsPickleFile.close()
        print( "Resume/Import Successful")
    # Otherwise we start off a new study...
    except:
        print( "Resume/Import unsuccessful, starting new study.")
        PopSize = int(sys.argv[2])
        BreederSize = int(sys.argv[3])
        Generations = int(sys.argv[1])
        Population = []
        DesignIDnum = 1
        print( "Initialize the population...")
        timeStart = time.time()
        for i in range(PopSize):
            ProgBar(i, PopSize, timeStart)
            Population.append(MakeRandomAirplane(DesignIDnum))
            DesignIDnum += 1
        ProgBar(PopSize, PopSize, timeStart)
        BestSoFar = Population[0]
    # Evolve the population
    timeStart = time.time()
    for gen in range(Generations):
        print( "Gen #: {}, Now on design #: {}".format(gen, DesignIDnum))
        # Find the fittest, if there's a score tie the oldest gets priority.
        Population.sort(key=lambda tup: tup[0], reverse=True)
        # Keep only the best for breeding
        Population = Population[0:BreederSize]
        # If there's a new best ever let us know, and save them for later
        if Population[0][0] > BestSoFar[0]:
            BestSoFar = Population[0]
            print( "@ gen={0} of {3}: Best design so far is #{1} @ {2:1.5f}".format(gen, BestSoFar[1].name, BestSoFar[0], Generations))
            topScoreStr = "\tTop {d} Scores: ".format(min(5,PopSize))
            for i in range(min(5,PopSize)):
                topScoreStr += "{0:1.3f}".format(Population[i][0]) + " "
            print( topScoreStr)

        # Breed new designs
        print( "Breeding new designs")
        timeStart = time.time()
        for i in range(PopSize - BreederSize):
            ProgBar(i, (PopSize - BreederSize), timeStart)
            DesignIDnum += 1    # Increment the design number so we can keep track.
            # Allows 2 or more parents as we can select from those just bred...
            Population.append(SpawnAirplanes(DesignIDnum, random.choice(Population), random.choice(Population)))
        ProgBar((PopSize - BreederSize), (PopSize - BreederSize), timeStart)

    print( "")
    print( "#################################################")
    print( "#                   REPORT")
    print( "# NAME: Design #{}".format(BestSoFar[1].name))
    print( "# SCORE: {}".format(BestSoFar[0]))
    print( "#")
    print( "#                PERFORMANCE")
    print( "# Vs = {0:1.1f} knots".format(BestSoFar[1].Vs))
    print( "# CLmax = {0:}".format(BestSoFar[1].CLmax))
    print( "# Vc = {0:1.1f} knots".format(BestSoFar[1].Vc))
    print( "# Range VFR = {0:1.1f} nmi".format(BestSoFar[1].RangeVFRcruise))
    print( "# Endurance VFR = {0:1.1f} hrs".format(BestSoFar[1].EnduranceVFR))
    print( "#")
    print( "#              SPECIFICATIONS")
    attrs = vars(BestSoFar[1])
    print( ', '.join("%s: %s" % item for item in attrs.items()))
    print( "#")
    print( "#################################################")
    print( "")
    
    finalDesigns = open('FinalDesigns.log', 'w')
    finalDesigns.write("All designs at end of program:\n")
    for i in Population:
        attrs = vars(i[1])
        finalDesigns.write("{"+"'Score' : {},".format(i[0])+','.join("%s:%s" % item for item in attrs.items()))
        finalDesigns.write("}\n")
    
    finalDesignsPickleFile = open('FinalDesigns.pkl', 'wb')
    pickle.dump(PopSize, finalDesignsPickleFile)
    pickle.dump(BreederSize, finalDesignsPickleFile)
    pickle.dump(Population, finalDesignsPickleFile)
    pickle.dump(BestSoFar, finalDesignsPickleFile)
    pickle.dump(DesignIDnum, finalDesignsPickleFile)
    pickle.dump(random.getstate(), finalDesignsPickleFile)
    finalDesignsPickleFile.close()
