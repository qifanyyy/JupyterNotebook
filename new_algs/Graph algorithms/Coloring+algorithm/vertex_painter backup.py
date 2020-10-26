#Vertex Painting Interface Alpha
print("[info]Launching Vertex Painter...")
import pygame, sys
from pygame.locals import *
#Color Point Format
global pt, colorpt
pt = []
colorpt = []

ScreenWidth = 720
ScreenHeight = 480

pygame.init()
form = pygame.display.set_mode((ScreenWidth, ScreenHeight))

TICK, t = pygame.USEREVENT+1, 200
pygame.time.set_timer(TICK, t)

pygame.display.set_caption('Vertex Painter')

global currentlayer,mouselocation
mouselocation = (0,0)
currentlayer = 0.3
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
    global pt, colorpt
    for coordinates in rtps:
        if ";" not in coordinates:
            point.append(coordinates);
            colordata.append([0,0,0]);

def main():
    global currentlayer,mouselocation
    rtps = ReadPointCloud("pointclouds.asc")
    layerpt = GetLayerCoordinates(rtps)
    topz = GetTopLayer(rtps)
    while True:
        form.fill((0,0,0))

        #Create cross-section point cloud
        for points in layerpt:
            axis = points.split()
            ax = int(float(axis[0])* scale + offsetx) 
            ay = int(float(axis[1])* scale + offsety)
            pygame.draw.circle(form,(255,255,255),(ax,ay),1)
            
        #Draw Mouse Position to form
        pygame.draw.circle(form,(130, 177, 255),mouselocation,10)
        for event in pygame.event.get():
            if event.type == QUIT: #Closing Handler
                print("[Info]System Exiting...")
                pygame.quit()
                sys.exit()
            if event.type == TICK:
                #currentlayer += 0.3
                #currentlayer = float("%.2f"%currentlayer)
                if currentlayer > float(topz):
                    currentlayer = 0.3
                elif currentlayer < 0.3:
                    currentlayer = float(topz)
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
                if event.key == pygame.K_DOWN:
                    currentlayer -= 0.3
                    currentlayer = float("%.2f"%currentlayer)
                    layerpt = GetLayerCoordinates(rtps)
            if event.type == pygame.MOUSEMOTION:
                mouselocation = event.pos
        pygame.display.update()


main()
