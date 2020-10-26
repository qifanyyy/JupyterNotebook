import re
import math


class loc:

    def __init__(self, name, lat, lon):
        self.Longitude = lon
        self.Latitude = lat
        self.Name = name

    def distance(self, b):
        LatRad =  math.radians( self.Latitude )
        LongRad = math.radians( self.Longitude )
        longDiff = math.radians(  b.Longitude - self.Longitude )
        latdiff =  math.radians(  b.Latitude -  self.Latitude )
        a = math.pow( math.sin( latdiff /2.0 ), 2 ) + math.cos( LatRad ) * math.cos( math.radians( b.Latitude ) ) * math.pow( math.sin(longDiff/2.0) ,2)
        #print a
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return 3961.0 * c

    def __str__(self):

        return "Name: " + str(self.Name) +" Lat: "+ str(self.Latitude) +" Long: " + str(self.Longitude)

matches = []

desired = loc("dest", 35.880036, -106.303114)
end = loc("src", 35.882965, -106.318882)
#print desired.distance(end)
#print end.distance(desired)


f = open('USA-country-simple.tmg', 'r')
regex = re.compile(".+\s+35\.{1}\d+\s+-106\.{1}\d+")
for line in f:
    if regex.match(line):
        #print "line found"
        #print line
        sline = []
        sline = line.split(" ");
        matches.append( loc( sline[0] ,float(sline[1]),float(sline[2]) ) )
        #matches.apends(line)

closest = matches[0]
print "looking"
shortesDist = desired.distance(closest)

for cl in matches:
    #print "shortest distance found"
    #print shortesDist
    #print "cl's distance from desired"
    #print desired.distance(cl)
    if desired.distance(cl) < shortesDist:
        #print "\nbefore switch"
        #print shortesDist
        #print closest
        closest = cl
        shortesDist = desired.distance(cl)
        #print "after switch"
        #print shortesDist
       # print closest
        #print "\n"

        
print "found: "
print closest
print "diatance"
print shortesDist

