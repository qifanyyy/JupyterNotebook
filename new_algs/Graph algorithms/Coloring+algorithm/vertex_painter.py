#Vertex Painting Interface Alpha
print("[info]Launching Vertex Painter...")
import pygame, sys
from pygame.locals import *
#Color Point Format
global pt, colorpt,filename,colorrect,rtp
filename = "teapot.asc"
pt = []
rpt = []
colorpt = []
colorrect = []

ScreenWidth = 720
ScreenHeight = 480

pygame.init()
form = pygame.display.set_mode((ScreenWidth, ScreenHeight))

TICK, t = pygame.USEREVENT+1, 200
pygame.time.set_timer(TICK, t)

pygame.display.set_caption('Vertex Painter')

global currentlayer,mouselocation
mouselocation = (0,0)
currentlayer = 0.0
offsetx = ScreenWidth/2
offsety = ScreenHeight/2
scale = 4

def ReadPointCloud(filename):
    infile = open(filename)
    content = infile.read()
    rawcoordinates = content.split("\n")
    return rawcoordinates

def GetLayerCoordinates(points):
    layerpoints = []
    for item in points:
        if str(currentlayer) in item and ";" not in item:
            layerpoints.append(item)
    return layerpoints

def GetTopLayer(points):
    topcoordinate = points[len(points) -2]
    axis = topcoordinate.split()
    return axis[2]

def CreateColorData(rtps):
    global pt, colorpt, rpt
    for coordinates in rtps:
        if ";" not in coordinates:
            if ScalePointCoordinate(coordinates) != None:
                pt.append(ScalePointCoordinate(coordinates))
                rpt.append(coordinates)
                colorpt.append((0,0,0));

def ScalePointCoordinate(point,debug=False):
    axis = point.split()
    if debug != False:
        print(point)
    try:
        ax = int(float(axis[0])* scale + offsetx) 
        ay = int(float(axis[1])* scale + offsety)
        az = float(axis[2])
        return (ax,ay,az)
    except Exception as e:
        #Some Null object get passed to this function as point (?
        pass
        return None

def GetLayerColor(layernumber):
    i = 0
    layernumber += 0.3
    layernumber = float("%.2f"%layernumber)
    print("Current Layer: " + str(layernumber) + " mm")
    for i in range(0,len(pt)):
        if float(pt[i][2]) == float(layernumber):
            #print(float(pt[i][2]),float(layernumber))
            #print(colorpt[i])
            return colorpt[i]
        
def ChangeLayerColor(layernumber,color):
    i = 0
    layernumber += 0.3
    layernumber = float("%.2f"%layernumber)
    print("[info] Layer " + str(layernumber) + " mm changed to " + str(color))
    for i in range(0,len(pt)):
        if float(pt[i][2]) == float("%.2f"%layernumber):
            colorpt[i] = color
            #print(pt[i][2])
    
def WriteText(text,pos):
    basicFont = pygame.font.SysFont(None, 18)
    text = basicFont.render(text, True, (255,255,255))
    form.blit(text,pos)


def DrawColorSelectBox(colorarr,selected):
    gridsize = 32
    background = pygame.Surface((len(colorarr) * gridsize, gridsize))
    pos = 0
    for color in colorarr:
        if pos == selected:
            pygame.draw.rect(background,color,(pos * gridsize,0,gridsize,gridsize))
            pygame.draw.rect(background,(244, 160, 65),(pos * gridsize,0,gridsize,gridsize),2)
        else:
            pygame.draw.rect(background,color,(pos * gridsize,0,gridsize,gridsize))
        pos += 1
    return background
    
def DrawCoordinates(pos):
    drawpos = (pos[0],pos[1] - 18)
    basicFont = pygame.font.SysFont(None, 18)
    text = basicFont.render(str(pos), True, (255,255,255))
    form.blit(text,drawpos)


def GetLeftTop(p1,p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    fx = 0
    fy = 0
    if x1 < x2:
        fx = x1
    else:
        fx = x2
    if y1 < y2:
        fy = y1
    else:
        fy = y2
    return (fx,fy)

def CreateColorRec(color,coordinates):
    global pt,colorpt,colorrect
    print(coordinates)
    try:
        p1 = coordinates[0]
        p2 = coordinates[1]
        width = abs(p1[0] - p2[0])
        height = abs(p1[1] - p2[1])
        rect = pygame.Surface((width,height))
        rect.fill(color)
        pos = GetLeftTop(p1,p2)
        colorrect.append([pos,rect])
        ChangeAllColorInRange(p1,p2,color)
        return rect
    except Exception as e:
        print("[info]Selection out of range.")
        print("[info]Only one coordinate received: " + str(coordinates))

def ChangeAllColorInRange(p1,p2,color):
    global pt,colorpt
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    if x1 > x2:
        x1,x2 = x2,x1
    if y1 > y2:
        y1,y2 = y2,y1
    for i in range(0,len(pt)-1):
        px = pt[i][0]
        py = pt[i][1]
        if px > x1 and px < x2:
            if py > y1 and py < y2:
                #Point in range of coordinates
                colorpt[i] = color

def DrawColorRec(screen):
    global colorrect
    for item in colorrect:
        pos = item[0]
        surface = item[1]
        screen.blit(surface,pos)

def main():
    global currentlayer,mouselocation,filename,colorrec
    rtps = ReadPointCloud(filename)
    CreateColorData(rtps)
    mousedown = False
    print(rtps[1])
    layerpt = GetLayerCoordinates(rtps)  
    topz = GetTopLayer(rtps)
    currentcolor = GetLayerColor(currentlayer)
    tspce = 15
    colorarr = [(0,0,255),(0,255,0),(255,0,0),(0,255,255),(255,0,255),(255,255,0),(0,0,0)]
    selectedcolor = 0
    selectingrec = []
    while True:
        #Background Color Handling
        form.fill((0,0,0))
        DrawColorRec(form)
        #if currentcolor != (0,0,0):
            #form.fill(currentcolor)
        #Draw Debug Text to screen
        WriteText("Vertex Painter Experimental Build v0.1.1",(0,0))
        WriteText("Object Height: " + str(topz) +" mm, ASCII gcode",(0,tspce))
        WriteText("Current Layer: " + str(currentlayer) + " mm",(0,2 * tspce))
        WriteText("Layer Color: " + str(currentcolor) + "",(0,3 * tspce))

        #Create Color Selection Board
        colorbox = DrawColorSelectBox(colorarr,selectedcolor)
        form.blit(colorbox,(0,4 * tspce))
        
        #Create cross-section point cloud
        for points in layerpt:
            axis = points.split()
            ax = int(float(axis[0])* scale + offsetx) 
            ay = int(float(axis[1])* scale + offsety)
            pygame.draw.circle(form,(255,255,255),(ax,ay),1)
            
        #Draw Mouse Position to form
        pygame.draw.circle(form, colorarr[selectedcolor],mouselocation,10)
        DrawCoordinates(mouselocation)
        
        for event in pygame.event.get():
            if event.type == QUIT: #Closing Handler
                print("[Info]System Exiting...")
                pygame.quit()
                sys.exit()
            if event.type == TICK:
                #currentlayer += 0.3
                #currentlayer = float("%.2f"%currentlayer)
                if currentlayer > float(topz):
                    currentlayer = float(topz)
                elif currentlayer < 0.0:
                    currentlayer = 0.0
                #layerpt = GetLayerCoordinates(rtps)
                #print(len(layerpt),currentlayer)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("[Info]System Exiting...")
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    currentlayer += 0.3
                    currentlayer = float("%.2f"%currentlayer)
                    layerpt = GetLayerCoordinates(rtps)
                    currentcolor = GetLayerColor(currentlayer)
                    #print("Current Layer: ", currentlayer)
                if event.key == pygame.K_DOWN:
                    if currentlayer != 0.0:
                        currentlayer -= 0.3
                        currentlayer = float("%.2f"%currentlayer)
                        layerpt = GetLayerCoordinates(rtps)
                        currentcolor = GetLayerColor(currentlayer)
                        #print("Current Layer: ", currentlayer)
                if event.key == pygame.K_PAGEUP:
                    currentlayer = float(topz)
                    currentlayer = float("%.2f"%currentlayer)
                    layerpt = GetLayerCoordinates(rtps)
                    currentcolor = GetLayerColor(currentlayer)

                if event.key == pygame.K_PAGEDOWN:
                    currentlayer = 0.0
                    currentlayer = float("%.2f"%currentlayer)
                    layerpt = GetLayerCoordinates(rtps)
                    currentcolor = GetLayerColor(currentlayer)
                if event.key == pygame.K_a:
                    #Apply Layer Coloring to this layer
                    print("Color Layer Applied")
                    ChangeLayerColor(currentlayer,colorarr[selectedcolor])
                    currentcolor = GetLayerColor(currentlayer)
                    
                if event.key == pygame.K_s:
                    #Change Selected Layer Coloring
                    #print("Color Selection Changed")
                    selectedcolor += 1
                    if selectedcolor > len(colorarr) - 1:
                        selectedcolor = 0
                    
                if event.key == pygame.K_e:
                    #Export the data information
                    expfile = open("colordata.ims","w")
                    pos = 0
                    expfile.write(";Vertex Painter Alpha\n")
                    for pos in range(0,len(pt)):
                        #dataline = str(pt[pos]) + ":" + str(colorpt[pos])
                        dataline = str(rpt[pos]) + ":" + str(colorpt[pos])
                        expfile.write(dataline + "\n")
                    expfile.close()
                    print("Color Data File Exported.")
            #Handling Mouse Events
            if event.type == pygame.MOUSEMOTION:
                mouselocation = event.pos
            if  event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
                if event.pos not in selectingrec:
                    #Not single click
                    selectingrec.append(event.pos)
                    print(selectingrec)
                    CreateColorRec(colorarr[selectedcolor],selectingrec)
                    selectingrec = []
                else:
                    selectingrec = []
            if  event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
                selectingrec.append(event.pos)
        pygame.display.update()


main()
