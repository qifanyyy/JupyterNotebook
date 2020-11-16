#Gcode To Point Cloud System
#This function is used to convert gcode to point cloud
import math
def main():
    infile = open("BeerCan.gcode")
    content = infile.read()
    lines = content.split("\n")
    currentZ = 0
    points = []
    for line in lines:
        if ";" not in line:
            #This line is not a comment line
            if "Z" in line:
                currentZ = GetZ(line)
        if "X" in line and "Y" in line:
            #This is a coordinate define line
            x = GetX(line)
            y = GetY(line)
            points.append(str(x) + ' ' + str(y) + ' ' + str(currentZ))
            
    Write2File(points)
    

def convert(filename):
    infile = open(filename)
    content = infile.read()
    lines = content.split("\n")
    currentZ = 0
    points = []
    for line in lines:
        if ";" not in line:
            #This line is not a comment line
            if "Z" in line:
                currentZ = GetZ(line)
        if "X" in line and "Y" in line:
            #This is a coordinate define line
            x = GetX(line)
            y = GetY(line)
            points.append(str(x) + ' ' + str(y) + ' ' + str(currentZ))
            
    Write2File(points)


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
def GetZ(line):
    line = line.split()
    for item in line:
        if "Z" in item:
            return float(item.replace("Z",""))

def Write2File(arr):
    outfile = open("pointclouds.asc","w")
    for item in arr:
        outfile.write(item + "\n")
    print("//Finish writing to file.//")
    outfile.close()

print("//Gcode to point cloud converter//")
print("//WARNING, STILL IN DEVELOPMENT//\n")
main()

