import turtle
import ctypes
import sys
import collections
import pathfinderalgorithms as pf
import tkinter as tk
import math
import Grids

space=[]
res_x,res_y=ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1)
wn=turtle.Screen()
wn.bgcolor("black")
wn.title("Pacman Game With Artificial Intelligence")
wn.setup(width=.99,height=.90,startx=0,starty=0)

#register shapes Konum Değiştir Erken Yapıyor
wn.register_shape("img/map.gif")
wn.register_shape("img/strawberry.gif")
wn.register_shape("img/Pacman_Right.gif")



# class for the Maze turtle (map.gif square)
class Maze(turtle.Turtle):               
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("img/map.gif")
        self.penup()
        self.speed(0)

# class for the End Or Food (fruit)
class Forage(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("img/strawberry.gif")
        self.penup()
        self.speed(0) 

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

class Space(turtle.Turtle): #Look Repeat
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0) 

class Sprite(turtle.Turtle):  #turtle hareket eden nesne olarak baz alındı
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("img/Pacman_Right.gif")
        self.speed(0)


def is_collision(self, other):
        a=self.xcor()-other.xcor()
        b=self.ycor()-other.ycor()
        distance = math.sqrt((a*2) + (b*2))
        if distance < 5:
            return True
        else:
            return False

map_graph = collections.defaultdict(list)

def DiscoverMaze(x_pos,y_pos): #Maze'in Graphını Çıkar
    if (x_pos+24,y_pos) in space:
        map_graph[space.index((x_pos,y_pos))].append(space.index((x_pos+24,y_pos)))
    if (x_pos-24,y_pos) in space:
        map_graph[space.index((x_pos,y_pos))].append(space.index((x_pos-24,y_pos)))
    if (x_pos,y_pos+24) in space:
        map_graph[space.index((x_pos,y_pos))].append(space.index((x_pos,y_pos+24)))
    if (x_pos,y_pos-24) in space:
        map_graph[space.index((x_pos,y_pos))].append(space.index((x_pos,y_pos-24)))
    last_index=space.index((x_pos,y_pos))+1
    if  last_index != len(space):
        x_y_pos=space[last_index]
        DiscoverMaze(x_y_pos[0],x_y_pos[1])

def Move(endStamp):
    for index in pf.path_list:
        x_y_position=space[index]
        sprite.goto(x_y_position[0],x_y_position[1])
    sprite.goto(space[endStamp])


def setupMaze(grid):
    for y in range(len(grid)):                                 #Labirent İçin Kodlanan Grid'in Tüm Birimleri Çizilecek
        for x in range(len(grid[y])):                
            character = grid[y][x]                   
            screen_x = ((-res_x/2)+(res_x-960)/2) + (x * 24)   #Her Bir Square 24x24 Bit       960=41*20
            screen_y = (res_y/3) - (y * 24)                    #Ekrandaki Maze Tam Center'lı Gibi Düşünülmeli Analitik Düzlem Üzerinde 
            if character == "+":                    
                maze.goto(screen_x, screen_y)        
                maze.stamp()                         
                walls.append((screen_x, screen_y))  
                
            elif character == "f": 
                forage.goto(screen_x, screen_y)         #Forage kordinatlara götürür
                forage.stamp()                          #nesneyi ekrana stamp eder
                forages.append((screen_x,screen_y))     
                space.append((screen_x,screen_y))

            elif character == "s":                      #grid için s karakter içeriyorsu
                sprite.speed(1)
                sprite.goto(screen_x, screen_y)      
                sprite.pen(fillcolor="black", pencolor="yellow", pensize=2)
                space.append((screen_x,screen_y))
            
            else:
                space.append((screen_x,screen_y))


   
############# Main Program Class  ######################

maze = Maze()                
sprite = Sprite()            
forage=Forage()
walls =[]                   
forages = []


#Algorithms Return Type:Tuple (Explored,Path_List)
#Algorithms Astarsearch: Path_List,cost_so_far

######################## DFS Algorithm ########################
#setupMaze(Grids.dfsGrid)              # Maze Çiziliyor...
#DiscoverMaze(sprite.xcor(),sprite.ycor())
#pf.path_list=[]
#dfs_came_from=pf.dfs(map_graph,0,space.index(forages[0]))
#pf.traverseback(dfs_came_from,space.index(forages[0]),0)
#Move(space.index(forages[0]))
#print("DFS Completed")
#tk.mainloop()
######################## DFS Algorithm ########################

######################## BFS Algorithm ########################
#setupMaze(Grids.bfsGrid)              # Maze Çiziliyor...
#DiscoverMaze(sprite.xcor(),sprite.ycor())
#pf.path_list=[]
#bfs_came_from=pf.bfs(map_graph,0,space.index(forages[0]))
#pf.traverseback(bfs_came_from,space.index(forages[0]),0)
#Move(space.index(forages[0]))
#print("BFS Completed")
#tk.mainloop()
######################## BFS Algorithm ########################

######################## UCS Algorithm ########################
#setupMaze(Grids.ucsGrid)              # Maze Çiziliyor...
#DiscoverMaze(sprite.xcor(),sprite.ycor())
#pf.path_list=[]
#ucs_came_from=pf.ucs(map_graph,0,space.index(forages[0]))
#pf.traverseback(ucs_came_from,space.index(forages[0]),0)
#Move(space.index(forages[0]))
#print("UCS Completed")
#tk.mainloop()
######################## UCS Algorithm ########################

######################## aStar Algortihm ########################
#setupMaze(Grids.aStar)              # Maze Çiziliyor...
#DiscoverMaze(sprite.xcor(),sprite.ycor())
#pf.path_list=[]
#aStar_came_from=pf.aStar(map_graph,0,space.index(forages[0]),(sprite.xcor(),sprite.ycor()),(forages[0]))
#pf.traverseback(aStar_came_from,space.index(forages[0]),0)
#last_forages_index=space.index(forages[0])
#Move(last_forages_index)
#print("aStar Completed")
#tk.mainloop()
######################## aStar Algortihm ########################

######################## aStar 4(Forage) Algortihm ########################
setupMaze(Grids.aStar4Foragesgrid)              # Maze Çiziliyor...
DiscoverMaze(sprite.xcor(),sprite.ycor())
pf.path_list=[]
aStar_came_from=pf.aStar(map_graph,0,space.index(forages[1]),(sprite.xcor(),sprite.ycor()),(forages[1]))
pf.traverseback(aStar_came_from,space.index(forages[1]),0)
last_forages_index=space.index(forages[1])
Move(last_forages_index)

pf.path_list=[]
aStar_came_from=pf.aStar(map_graph,last_forages_index,space.index(forages[2]),(sprite.xcor(),sprite.ycor()),(forages[2]))
pf.traverseback(aStar_came_from,space.index(forages[2]),last_forages_index)
last_forages_index=space.index(forages[2])
Move(last_forages_index)

pf.path_list=[]
aStar_came_from=pf.aStar(map_graph,last_forages_index,space.index(forages[0]),(sprite.xcor(),sprite.ycor()),(forages[0]))
pf.traverseback(aStar_came_from,space.index(forages[0]),last_forages_index)
last_forages_index=space.index(forages[0])
Move(last_forages_index)
print("aStar(4 Forages) Completed")
tk.mainloop()
######################## aStar 4(Forage) Algortihm ########################


