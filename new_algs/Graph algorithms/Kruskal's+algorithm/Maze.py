# -*- coding: utf-8 -*-

import numpy as np
import random
from os import system
import sys
import time

# function to print the maze
def printMaze(maze):
  system('clear')
  for i in range(len(maze)):
    for j in range(len(maze[i])):
      if maze[i][j] == 0:
        print('██', end="")
      if maze[i][j] == 6:
        print('@>', end="")
      elif maze[i][j] == 1 or maze[i][j] == 4 or maze[i][j] == 5:
        print('  ', end="")
    print('')

# function to generate the maze
def generate_maze(n, m):
  def find(p, q):
    if p != cells[p] or q != cells[q]:
      cells[p], cells[q] = find(cells[p], cells[q])
    return cells[p], cells[q]    # find spanning tree

  # make even size to avoid issues in the future
  if n % 2 == 1:
    n = n + 1
  if m % 2 == 1:
    m = m + 1

  # maze checkerboard of wall squares and squares that can be either walls or pathways
  maze = np.tile([[1, 2], [2, 0]], (n // 2 + 1, m // 2 + 1))
  maze = maze[:-1, :-1]
  cells = {(i, j): (i, j) for i, j in np.argwhere(maze == 1)}
  walls = np.argwhere(maze == 2)    # union-find
  np.random.shuffle(walls)

  # kruskal's maze algorithm
  for wi, wj in walls:
    if wi % 2:
      p, q = find((wi - 1, wj), (wi + 1, wj))
    else:
      p, q = find((wi, wj - 1), (wi, wj + 1))
    maze[wi, wj] = p != q
    if p != q:
      cells[p] = q

  # initialise the vertical borders
  vertBordersLeft = np.zeros((n + 3,), dtype=int)
  vertBordersRight = vertBordersLeft.copy()
  vertBordersLeft[random.randint(1, n // 2) * 2 - 1] = 6 # Create entrance where agent starts
  vertBordersRight[random.randint(1, n // 2) * 2 - 1] = 5 # Create exit
  
  # initialise the horizontal borders
  horiBorders = np.zeros((m + 1,), dtype=int)

  # pad maze with walls
  maze = np.concatenate(([horiBorders], maze), axis=0)
  maze = np.concatenate((maze, [horiBorders]), axis=0)
  maze = np.insert(maze, 0, vertBordersLeft, axis=1)
  maze = np.insert(maze, len(maze[0]), vertBordersRight, axis=1)

  return maze

def naiveSolveMaze (maze):
  def move(loc, dir, maze):
    newLoc = loc
    
    # edge case for when maze is solved
    if (maze[loc[0]][loc[1] + 1]) == 5:
      maze[loc[0]][loc[1] + 1] = 6
      maze[loc[0]][loc[1]] = 1
      return maze, loc, dir, True
    
    # attempt to turn right, if it's a wall go forwards instead
    if dir == 1:
      if maze[loc[0] + 1][loc[1]] == 1:
        dir += 1
        newLoc = (loc[0] + 1, loc[1])
      else:
        newLoc = (loc[0], loc[1] + 1)
    elif dir == 2:
      if maze[loc[0]][loc[1] - 1] == 1:
        dir += 1
        newLoc = (loc[0], loc[1] - 1)
      else:
        newLoc = (loc[0] + 1, loc[1])
    elif dir == 3:
      if maze[loc[0] - 1][loc[1]] == 1:
        dir += 1
        newLoc = (loc[0] - 1, loc[1])
      else:
        newLoc = (loc[0], loc[1] - 1)
    elif dir == 4:
      if maze[loc[0]][loc[1] + 1] == 1:
        dir = 1
        newLoc = (loc[0], loc[1] + 1)
      else:
        newLoc = (loc[0] - 1, loc[1])
    
    # if not possible to move into new spot (going forwards) then set previous spot and turn right to try and find a new rooute
    if maze[newLoc[0]][newLoc[1]] != 1 and maze[newLoc[0]][newLoc[1]] != 5:
      dir = dir - 1
      # wrap dir around
      if dir < 0:
        dir = 4
      newLoc = loc
    # change location of agent in maze state
    elif maze[newLoc[0]][newLoc[1]] == 1:
      maze[newLoc[0]][newLoc[1]] = 6
      maze[loc[0]][loc[1]] = 1

    return maze, newLoc, dir, False

  printMaze(maze)
  time.sleep(1.0)
  
  # individual maze game loop set up
  i = 1
  mv = move((np.where(maze == 6)[0][0], 0), 1, maze)
  maze = mv[0]
  while (mv[3] != True):
    mv = move(mv[1], mv[2], maze)
    maze = mv[0]

    printMaze(maze)
    time.sleep(0.1)
    i += 1
  
  print("Solved Maze in", i, "steps.")

def main():
    # get command line arguments and generate the maze
    if len(sys.argv) < 3:
      width, height = 32, 56
    else:
      width, height = int(sys.argv[1]), int(sys.argv[2])
    
    # main game loop thing that runs the game infinitely
    while (True):
      maze = generate_maze(width, height)
      naiveSolveMaze(maze)
      # display solved maze for two seconds
      time.sleep(2.0)

if __name__ == "__main__":
    main()
    
