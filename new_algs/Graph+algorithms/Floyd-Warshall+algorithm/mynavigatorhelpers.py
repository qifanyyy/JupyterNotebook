'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *




### This function optimizes the given path and returns a new path
### source: the current position of the agent
### dest: the desired destination of the agent
### path: the path previously computed by the Floyd-Warshall algorithm
### world: pointer to the world
def shortcutPath(source, dest, path, world, agent):
    ### YOUR CODE GOES BELOW HERE ###
    
    repeat = True
    while repeat:
        repeat = False
        for i in range(len(path) - 2):
            if clearShot(path[i], dest, world.getLines(), world.getPoints(), agent):
                return path[:i+1]
            
            if clearShot(path[i], path[i + 2], world.getLines(), world.getPoints(), agent):
                path.remove(path[i+1])
                repeat = True
                break

    ### YOUR CODE GOES BELOW HERE ###
    return path



### This function changes the move target of the agent if there is an opportunity to walk a shorter path.
### This function should call nav.agent.moveToTarget() if an opportunity exists and may also need to modify nav.path.
### nav: the navigator object
### This function returns True if the moveTarget and/or path is modified and False otherwise
def mySmooth(nav):
    ### YOUR CODE GOES BELOW HERE ###
    
    current = nav.agent.getLocation()
    goal = nav.agent.moveTarget
    
    if clearShot(current, goal, nav.world.getLines(), nav.world.getPoints(), nav.agent):
        nav.agent.moveToTarget(goal)
        return True

    ### YOUR CODE GOES ABOVE HERE ###
    return False

### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the current location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
def clearShot(p1, p2, worldLines, worldPoints, agent):
    ### YOUR CODE GOES BELOW HERE ###
    
    if rayTraceWorldNoEndPoints(p1, p2, worldLines) == None:
        for point in worldPoints:
            if minimumDistance((p1, p2), point) < agent.getMaxRadius():
                return False
        return True
    
    ### YOUR CODE GOES ABOVE HERE ###
    return False

