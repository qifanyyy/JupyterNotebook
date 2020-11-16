#/////////////////////////////////////////////////////////
#Colored Coordinate to ESSC System Control Sequency Array
#This system must be used as a module
#/////////////////////////////////////////////////////////
from math import sqrt
CPL = 2 #Number of color dot per unit of length
colorpt = []#Tmp Storage for Colored Data
cmyk_scale = 100
def RGB2CMYK(a):
    #As 3D printing require deeper color, CMYK are relative to
    #C = Blue
    #M = Red
    #Y = Yellow
    #K = Black
    r = int(a[0])
    g = int(a[1])
    b = int(a[2])
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / 255.
    m = 1 - g / 255.
    y = 1 - b / 255.

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale


def GetDistance(E1,E2):
    
    if E1 != None and E2 != None:
        E1 = float(E1)
        E2 = float(E2)
        return abs(E1 - E2)
    else:
        return 0
def GetRGB(color):
    color = color.replace("(","").replace(")","")
    tmp = color.split(",")
    return tmp

def ConvertToDistance(raw):
    print("[info] Processing Extruder Position Differece...")
    distances = []
    content = raw.split("\n")
    for i in range(0,len(content) -2):
        #For each coordinate
        E1 = float(content[i].split()[3].replace("E",""))
        E2 = float(content[i + 1].split()[3].replace("E",""))
        distances.append(abs(E2 - E1))
    print("[info] All distance calculated.")
    distances.append(10.0) #Extra 1cm for backup
    return distances

def GetE(raw,coordinate):
    for line in raw:
        if coordinate in line:
            return line.split(" ")[3].replace("E","")
    print("ERROR IN FINDING THIS COORDINATE")
    print(coordinate)

def Converter(filename):
    infile = open(filename)
    extfile = open("extruderdata.ims")
    content = infile.read()
    extdata = extfile.read()
    extruderpos = extdata.split("\n")
    coordinates = content.split("\n")
    distances = ConvertToDistance(extdata)
    print(len(distances))
    print(len(coordinates))
    carray = []
    larray = []
    currentheight = 0
    for coordinateid in range(0,len(coordinates)-3):
        if ";" not in coordinates[coordinateid]:
            tmp = coordinates[coordinateid].split(":")
            point = tmp[0]
            color = tmp[1]
            CMYKcolor = RGB2CMYK(GetRGB(color))
            npoint = coordinates[coordinateid + 1].split(":")[0]
            length = distances[coordinateid]
            #print("%.2f"%length,end="")
            thiscolor = ""
            if CMYKcolor[0] == 100:
                thiscolor += "B"
            if CMYKcolor[1] == 100:
                thiscolor += "R"
            if CMYKcolor[2] == 100:
                thiscolor += "Y"
            if CMYKcolor[3] == 100:
                thiscolor += "K"
            #print(thiscolor)
            if ("%.1f" % float(point.split()[2])) != currentheight:
                currentheight  = ("%.1f" % float(point.split()[2]))
                print("[info]Processing Layer: " + str(currentheight))
            length = length / len(thiscolor)
            al = int(length * CPL)
            if al >1:
                carray.append(thiscolor)
                larray.append(str(al))
    return carray,larray
            
def debug():
    print("[info]Color Array Generator In Progress.")
    carray,larray = Converter("colordata.ims")
    extfile = open("Colorarray.txt","w")
    for i in range(0,len(carray)-1):
        extfile.write(carray[i] + ":" + larray[i] + "\n")
    extfile.close()
    print("[info]Color Array Datafile Generated.")
debug()
    
