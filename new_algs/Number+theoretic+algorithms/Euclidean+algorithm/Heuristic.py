import math

def EuclideanDis(sprite_x,sprite_y,target_x,target_y): #Euclidean Uzaklığı
     return math.sqrt(pow((target_x-sprite_x),2)+pow((target_y-sprite_y),2))

def ManhattanDis(x_sprite,y_sprite,x_target,y_target): #Manhattan Uzaklığı
     distance_x=x_target-x_sprite
     distance_y=y_target-y_sprite
     return abs(distance_x/24)+abs(distance_y/24)

          