#Gcode Analysing System
#This function is for getting the Extruder position just before the Z step move up
import math
def main():
    infile = open("BeerCan.gcode")
    content = infile.read()
    lines = content.split("\n")
    layers = []
    lastlayer = ""
    layerlines = []
    for line in lines:
        if ";" not in line:
            #This line is not a comment line
            if "Z" in line:
                cmd = line.split()
                if "Z" in cmd[len(cmd) - 1]:
                    evalue = GetE(lastlayer)
                    length = GetLayerTotalLength(layerlines)
                    layers.append(str(cmd[len(cmd) - 1]).replace("Z","") + ":" + str(evalue) + ":" + str(length))
                    layerlines = []
        if "E" in line and ";" not in line:
            lastlayer = line
        if "X" in line and "Y" in line:
            #This is a coordinate define line
            layerlines.append(line)
    i = 0
    for item in layers:
        item = item.split(":")
        print("####### LAYER" + str(i) + " #######")
        print("Height: " + str(item[0]))
        print("Extruder: " + str(item[1]))
        print("Distance Traveled: " + str(item[2]))
        i += 1
    Write2File(layers)
    
    
def GetE(line):
    line = line.split()
    for item in line:
        if "E" in item:
            return item
    return "E0" #Usually the start of the gcode

def GetX(line):
    line = line.split()
    for item in line:
        if "X" in item:
            return float(item.replace("X",""))
def GetY(line):
    line = line.split()
    for item in line:
        if "Y" in item:
            return float(item.replace("Y",""))
                         
def GetLayerTotalLength(layerarrays):
    result = 0
    for line in range(0,len(layerarrays) -1):
        x1 = GetX(layerarrays[line])
        y1 = GetY(layerarrays[line])
        x2 = GetX(layerarrays[line + 1])
        y2 = GetY(layerarrays[line + 1])
        result += GetDistance(x1,y1,x2,y2)
    return str(result)
    
def GetDistance(x1,y1,x2,y2):
    result = (x1 - x2) ** 2 + (y1 - y2) ** 2
    result = math.sqrt(result)
    return result

def Write2File(arr):
    outfile = open("layerinfo.ims","w")
    outfile.write(";File Generated for FC3DP Controller.\n")
    outfile.write(";[Z_position]:[Extruder_Steps]:[Layer Length]\n")
    for item in arr:
        outfile.write(item + "\n")
    print("//Finish writing to file.//")
    outfile.close()

    
main()

