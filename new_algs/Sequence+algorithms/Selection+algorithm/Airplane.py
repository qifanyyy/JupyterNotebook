#!/usr/bin/env python3
#
info = """
Airplane.py
    A class that builds a mathematical model of a airplane based
    on the specifications/geometry it is called with then computes
    a set of performance parameters of interest that result from an 
    airplane with those specifications/geometry.

Author: Kevin R. Johnson
Email: Kevin@KevinJohnsonAviation.com
Copyright (C) 2015 Kevin R. Johnson 
Released under the GNU General Public License v3.0

    Airplane.py is free software: 
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

### Sources:
## Prof Bento S. de Mattos
# http://www.aer.ita.br/~bmattos/download/weight_class2drag.pdf
#
## Chris Heintz
# http://zenithair.com/kit-data/ch-design-made-simple-p1.pdf
#
## Engine Data.
# Rotax 912ULS: http://www.rotaxservice.com/rotax_engines/rotax_912ULSs.htm
# Rotax 914ULS: http://www.rotaxservice.com/rotax_engines/rotax_914ULs.htm
# http://easa.europa.eu/system/files/dfu/EASA-TCDS-E.122_BRP--Powertrain_Rotax_914_series_engines-03-26022010_.pdf
# All below have 60lb of accessories added to the listed dry weight.
# C-85: http://en.wikipedia.org/wiki/Continental_O-190  
# Lycoming O-320: http://en.wikipedia.org/wiki/Lycoming_O-320#Specifications_.28O-320-A1A.29
# Lycoming O-360: http://en.wikipedia.org/wiki/Lycoming_O-360#Specifications_.28O-360-A1A.29

### Import useful libraries
## Import my custom libraries...
import XfoilTalk            # My interface to xfoil.
import StandardAtmosphere   # Handy tools for standard atmosphere data.
## Import useful python libraries...
import math
 
class Airplane:

    KnotsToFPS = 6076.0/3600
    FPStoKnots = 3600/6076.0
        
    def CalcFuseSurfArea(self):
        BoxSidesArea = self.FuseBoxLen * (2*self.FuseWidth + 2*self.FuseHeight)
        PyramidSidesArea = self.FuseHeight * math.sqrt( (self.FuseWidth/2.0)**2.0  + self.FusePyramidLen**2.0 ) + self.FuseWidth  * math.sqrt( (self.FuseHeight/2.0)**2.0 + self.FusePyramidLen**2.0 )
        return BoxSidesArea + PyramidSidesArea
    
    # Calculate cruise speed at alt w/ wide-open-throttle
    def CalcVcWOTatAlt(self):
        if self.Engine['critAlt'] > self.CruiseAlt:
            # Don't lose HP below the critical altitude
            self.PwotAlt = self.Engine['HP']
        else:
            # Assume power goes as the air density at cruise alt / density at sea level
            self.PwotAlt = self.Engine['HP'] * StandardAtmosphere.Delta(self.CruiseAlt - self.Engine['critAlt']) 
        # Consider a speed range...  Somewhere in here the drag equals the thrust
        VcUpper = 150.0 * math.pow( self.PwotAlt / (self.S + 100.0), 1.0/3.0) * self.KnotsToFPS # Chris Heintz approx.
        VcLower = min(VcUpper * 0.75, 1.5* self.Vs)
        # Lets binary search this range or that speed...
        VcEst = (VcUpper + VcLower)/2.0
        while True:
            # Compute all the Reynolds Numbers
            ReNumWing = VcEst * self.Chord / self.kvisc
            ReNumHtail = VcEst * self.HTailChord / self.kvisc
            ReNumVtail = VcEst * self.VTailChord / self.kvisc
            ReNumFuse = VcEst * self.FuseLength / self.kvisc
            # Compute the CL we are cruising at on the wing, assume all others are at alfa=0
            CLc = math.sqrt((2.0 * self.MGTW) / (self.S * self.rho * VcEst * VcEst))
            # Compute all the drag terms, if there's a glitch go with a nominal guess and hopefully clean up on the next iteration.
            try:
                CDwing = XfoilTalk.GetData(self.Airfoil['file'], ReNumWing, 'cl', CLc)['CD']
                Dwing  = 0.5 * self.rho * VcEst * VcEst * self.S  * CDwing
            except:
                Dwing  = 0.5 * self.rho * VcEst * VcEst * self.S  * 0.0001
            try:
                CDhtail = XfoilTalk.GetData(self.TailFoil['file'], ReNumHtail, 'a', 0.0)['CD']
                Dhtail = 0.5 * self.rho * VcEst * VcEst * self.HS  * CDhtail
            except:
                Dhtail = 0.5 * self.rho * VcEst * VcEst * self.HS  * 0.0001
            try:
                CDvtail = XfoilTalk.GetData(self.TailFoil['file'], ReNumVtail, 'a', 0.0)['CD']
                Dvtail = 0.5 * self.rho * VcEst * VcEst * self.VS  * CDvtail
            except: 
                Dvtail = 0.5 * self.rho * VcEst * VcEst * self.VS  * 0.0001
            # Prof Bento S. de Mattos Estimation of zero-lift drag of fuselage
            CfFuse = (0.455/math.pow(math.log10(ReNumFuse), 2.58))
            FFfuse = 1.0 + (60.0/math.pow(self.FuseLength / max(self.FuseWidth,self.FuseHeight), 3.0)) + (self.FuseLength / max(self.FuseWidth,self.FuseHeight))/400.0
            FuseWetRatio = self.FuseSurfArea / self.S
            CDfuse = CfFuse * 1.0 * FFfuse * FuseWetRatio
            Dfuse  = 0.5 * self.rho * VcEst * VcEst * self.S  * CDfuse
            # The total drag is
            D = Dwing + Dhtail + Dvtail + Dfuse
            if abs(VcEst*D - self.PwotAlt*550)/(self.PwotAlt*550) < 0.05:
                self.Vc = VcEst
                self.CLc = CLc
                self.Drag = D
                return
            if (VcUpper - VcLower < 1.0):
                self.Vc = VcLower
                self.CLc = CLc
                self.Drag = D
                return
            if VcEst * D > self.PwotAlt * 550:
                VcUpper = VcEst
                VcEst = (VcUpper + VcLower)/2.0
            else:
                VcLower = VcEst
                VcEst = (VcUpper + VcLower)/2.0
                
    def CalcMoment(self):
        # Datum at front face of fuselage box
        #   Assume wing and all fuel negligibly close to the CofG
        #   Assume engine CofG 2' from front of fuselage.
        #   Assume payload at 0.75 of the box's length.
        Moment = self.Engine['weightLb'] * 2 + \
                 self.Payload * self.FuseBoxLen * 0.75 + \
                 ((self.FuseBoxLen * self.FuseWidth) + (self.FuseBoxLen * self.FuseHeight)) * 2 * \
                    self.skinAreaDens * self.FuseBoxLen/2 + \
                 (self.FuseHeight * math.sqrt( (self.FuseWidth/2.0)**2.0  + self.FusePyramidLen**2.0 ) + \
                 self.FuseWidth  * math.sqrt( (self.FuseHeight/2.0)**2.0 + self.FusePyramidLen**2.0 ) * \
                    self.skinAreaDens * (self.FuseBoxLen + self.FusePyramidLen/4.0) + \
                 (self.HS + self.VS) * 2 * self.skinAreaDens * (self.FuseBoxLen + self.FusePyramidLen))
        return Moment

    def __init__(self, name, Engine, Airfoil, Chord, Span, FlapX, FlapAngle, FuseBoxLen, FusePyramidLen, FuseWidth, FuseHeight, Tailfoil, HTailChord, VTailChord, HTailSpan, VTailSpan, MGTW, Sheet, Payload, CruiseAlt, ExtrasWeight):
        # Values that are for this specific airplane go here. 
        self.name = name        # A Unique way to identify this individual Airplane
        self.Engine = Engine    # An entry from Engines
        self.Airfoil = Airfoil  # An entry from Airfoils
        self.Chord = Chord      # In feet
        self.Span = Span        # In feet
        self.FlapX = FlapX      # Fraction of Chord [0,1] 
        self.FlapAngle = FlapAngle  # In degrees
        self.FuseBoxLen = FuseBoxLen    # In feet
        self.FusePyramidLen = FusePyramidLen    # In feet
        self.FuseWidth = FuseWidth  # In feet
        self.FuseHeight = FuseHeight    # In feet
        self.TailFoil = Tailfoil    # An entry from Tailfoils
        self.HTailChord = HTailChord    # In feet
        self.VTailChord = VTailChord    # In feet
        self.HTailSpan = HTailSpan  # In feet
        self.VTailSpan = VTailSpan  # In feet
        self.MGTW = MGTW    # Max Gross Takeoff Weight in pounds
        self.Sheet = Sheet  # An entry from Sheets
        self.Payload = Payload  # In pounds
        self.CruiseAlt = CruiseAlt   # Cruise altitude to optimize at in feet MSL
        self.ExtrasWeight = ExtrasWeight  # Weight budget for avionics/extras in pounds
        # OK, that's everything we build an airplane around, now lets calculate the rest.
        self.SheetLayers = 3
        # Handy constants.
        self.rho = StandardAtmosphere.Dens(self.CruiseAlt)
        self.kvisc = StandardAtmosphere.Kvisc(self.CruiseAlt)
        self.skinAreaDens = self.SheetLayers * self.Sheet['thick'] * self.Sheet['density']
        # Lets calculate toward stall speed...
        self.S = self.Chord * self.Span
        ReynNumStallGuess = 61 * self.KnotsToFPS * self.Chord / StandardAtmosphere.Kvisc(0)
        try:
            self.CLmax = XfoilTalk.CLmaxSearch(self.Airfoil['file'], ReynNumStallGuess, self.FlapX, 0, self.FlapAngle)["CL"]
            self.Vs = math.sqrt(2*self.MGTW/(self.S * self.CLmax * self.rho)) * self.FPStoKnots
        except:
            try:
                self.CLmax = XfoilTalk.CLmaxSearch(self.Airfoil['file'], ReynNumStallGuess, 1.0, 0, 0)["CL"]
                self.Vs = math.sqrt(2*self.MGTW/(self.S * self.CLmax * self.rho)) * self.FPStoKnots
            except:
                self.CLmax = 1.3
                self.Vs = math.sqrt(2*self.MGTW/(self.S * self.CLmax * self.rho)) * self.FPStoKnots
        self.AR = self.Span * self.Span / self.S
        # Lets calculate toward mass properties...
        self.FuseSurfArea = self.CalcFuseSurfArea()
        self.FuseLength = self.FuseBoxLen + self.FusePyramidLen
        self.HS = self.HTailChord * self.HTailSpan
        self.VS = self.VTailChord * self.VTailSpan
        self.EmptyWeight = (self.FuseSurfArea + 2*(self.S + self.VS + self.HS)) * self.skinAreaDens + self.Engine['weightLb'] + self.ExtrasWeight
        self.FuelWeight = max(0, self.MGTW - self.Payload - self.EmptyWeight)
        self.Moment = self.CalcMoment()
        self.CofG = self.Moment/self.MGTW
        # Lets calculate endurance...
        self.GPHatAlt = self.Engine['GPH'] * StandardAtmosphere.Delta(max(0.0,self.CruiseAlt - self.Engine['critAlt'])) 
        self.Endurance0Fuel = (self.FuelWeight/6.0) / self.GPHatAlt
        self.EnduranceVFR = max(0, self.Endurance0Fuel - 0.5)
        # Lets calculate toward stability terms...
        self.TailArm = self.FuseBoxLen + self.FusePyramidLen - self.CofG
        # Tail volume coefficients
        self.Vh = (self.HS * self.TailArm) / (self.S * self.Chord)
        self.Vv = (self.VS * self.TailArm) / (self.S * self.Span)
        # Calculate cruise speed WOT at Altitude!
        self.CalcVcWOTatAlt()
        # Calc Cruise Range VFR
        self.RangeVFRcruise = self.Vc * self.EnduranceVFR
        # The below approximations are from Chris Heintz @ zenithair.com
        self.Pparam = (self.MGTW/self.Engine['HP']) * (self.MGTW/self.S) # < 200 acceptable, <150 very good.
        self.Vz = ((7000 * self.Engine['HP'])/self.MGTW)*math.pow(self.AR, 1/4.0)  # feet per min best rate of climb
        self.Zmax = 16 * self.Vz    # Approximate service ceiling in feet.
        
if __name__ == "__main__":

    ### Data
    Engines = [{'name':'Rotax 912ULS', 'HP': 95, 'weightLb':140.6,  'GPH':7.0, 'critAlt':0}, \
               {'name':'Rotax 914UL',  'HP':100, 'weightLb':166.4,  'GPH':7.5, 'critAlt':16000}, \
               {'name':'Cont C-85',    'HP': 85, 'weightLb':180+60, 'GPH':5.4, 'critAlt':0}, \
               {'name':'Lyc O-320',    'HP':150, 'weightLb':244+60, 'GPH':9,   'critAlt':0}, \
               {'name':'Lycom O-360',  'HP':180, 'weightLb':258+60, 'GPH':10,  'critAlt':0}, \
               {'name':'80HP VW',      'HP':80,  'weightLb':161,    'GPH':5,   'critAlt':0}]
    # Airfoils for XFoil to use on the main wing.
    Airfoils= [{'name':'Clark Y', 'file':'clarky.dat'}, \
               {'name':'NLF 0414F', 'file':'NLF-0414F.dat'}, \
               {'name':'NLF 0115', 'file':'nlf0115.dat'}, \
               {'name':'NLF 0215F', 'file':'nlf0215f.dat'}, \
               {'name':'NLF 1015', 'file':'nlf1015.dat'}, \
               {'name':'NLF 415', 'file':'nlf415.dat'}, \
               {'name':'NLF 416', 'file':'nlf416.dat'}, \
               {'name':'P-51 Tip', 'file':'p51dtip.dat'}, \
               {'name':'NACA 63215', 'file':'n63215.dat'}, \
               {'name':'NACA 23008', 'file':'naca 23008'}, \
               {'name':'NACA 23012', 'file':'naca 23012'}, \
               {'name':'NACA 23015', 'file':'naca 23015'}, \
               {'name':'NACA 23021', 'file':'naca 23021'}, \
               {'name':'NACA 4408', 'file':'naca 4408'}, \
               {'name':'NACA 4412', 'file':'naca 4412'}, \
               {'name':'NACA 4415', 'file':'naca 4415'}, \
               {'name':'NACA 4421', 'file':'naca 4421'}, \
               {'name':'NACA 2412', 'file':'naca 2412'}]
    # Airfoils for XFoil to use on the tail
    TailFoils=[{'name':'NACA 0006', 'file':'naca 0006'}, \
               {'name':'NACA 0008', 'file':'naca 0008'}, \
               {'name':'NACA 0012', 'file':'naca 0012'}]
    # Material data:
    # Units are feet and lb/ft**3
    Sheets = [{'name':'6061-T6', 'thick':0.025 / 12, 'density':0.0975 * (12**3)}]

    print( info)
    #name, Engine, Airfoil, Chord, Span, FlapX, FlapAngle, FuseBoxLen, FusePyramidLen, FuseWidth, FuseHeight, Tailfoil, HTailChord, VTailChord, HTailSpan, VTailSpan, MGTW, Sheet):
    #
    #aplane = Airplane("RV-12", Engines[0], {'name':'NACA 23014', 'file':'NACA 23014'}, 4.75, 26+(9/12.0), 1, 0, 100/12.0, (19+11/12.0) - (100/12.0), 44/12.0, 44/12.0, TailFoils[-1], 3, 3, 6, 3, 1320, Sheets[0], 430, 7500, 60)

    aPlane = Airplane("Da Plane!", Engines[1], Airfoils[9], 5, 14, 0.80, 30, 100/12.0, 18 - (100/12.0), 24/12.0, 36/12.0, TailFoils[0], 3, 3, 6, 4, 1320, Sheets[0], 250, 10000, 60)
    print("")
    print( "#################################################")
    print( "#                   REPORT                      #")
    print( "# Vs = {0:1.1f} knots".format(aPlane.Vs))
    print( "# CLmax = {0:}".format(aPlane.CLmax))
    print( "# Vc = {0:1.1f} knots".format(aPlane.Vc))
    print( "# Range VFR = {0:1.1f} nmi".format(aPlane.RangeVFRcruise))
    print( "# Endurance VFR = {0:1.1f} hrs".format(aPlane.EnduranceVFR))
    print( "#                                               #")
    print( "#################################################")
    print("")
    attrs = vars(aPlane)
    print( ', '.join("%s: %s" % item for item in attrs.items()))
    

