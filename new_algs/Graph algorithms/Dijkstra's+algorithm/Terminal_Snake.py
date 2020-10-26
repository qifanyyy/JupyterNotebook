import os
from random import *
from pygame import Vector2
from pygame import time

def draw():
	os.system('cls') 
	for j in range(height+1):
		for i in range(width+1):
			currvec=Vector2(i,j)
			if currvec == snake.head: 
				print('D',end='')
				continue
			elif currvec in snake.body :
				print('X',end='')
				continue
			elif currvec == food:
				print('F',end='')
				continue
			else:					
				print('#',end='') if j== 0 or j==height or i==0 or i == width else print(' ',end='')
		print('')

def neighbour(node):
	node=Vector2(node)
	return [(node.x+1,node.y),(node.x-1,node.y),(node.x,node.y+1),(node.x,node.y-1)]

def find_path(food):
	nodes,prev,dist,k={},{},{},[]
	for x in range(1,width):
		for y in range(1,height):
			node=(x,y)
			if x not in [0,width] and  y not in [0,height] and Vector2(node) not in snake.body and node!=snake.head:
				nodes[node]='blank'
				dist[node]=1000000
	nodes[snake.head.x,snake.head.y]='blank'
	dist[snake.head.x,snake.head.y]=0
	backup=nodes.copy()
	while(nodes):
		u=0
		mn=1000000
		for node in nodes:
			if dist[node]<mn:
				mn = dist[node] 
				u=node
		try:
			nodes.pop(u)		
		except Exception:
			continue
		for v in neighbour(u):
			if v in nodes:
				if dist[v]>dist[u]+1:
					dist[v]=dist[u]+1
					prev[v]=u
	S=[]
	u=(int(food.x),int(food.y))
	if u in backup or u==tuple(snake.head):
		while u in prev:
			S.append(u)
			u=prev[u]
	pos=Vector2(snake.head.x,snake.head.y)
	for i in range(1,len(S)+1):
		move=Vector2(S[-i])-pos
		k.append(move)
		pos=S[-i]
	return k

class snake():

	def __init__(self):
		self.head=Vector2(int(width/2),int(height/2))
		self.body=[Vector2(int(width/2),int(height/2)-1),Vector2(int(width/2),int(height/2)-2)]
		self.alive=1
		self.prev_dir=Vector2(key)

	def move(self):
		global key
		if key==self.prev_dir*(-1):
			key=self.prev_dir
		else:
			self.prev_dir=key
			for i in range(len(self.body)-1,0,-1):
				self.body[i]=self.body[i-1]
		self.body[0]= Vector2(self.head.x,self.head.y)
		self.head+=key 	
		if self.head in self.body or self.head.x in(0,width) or self.head.y in (0,height):
			snake.alive=0
			return False
		return True
		
	def eat(self):
		new_food=Vector2(randint(1,width-1),randint(1,height-1))
		while new_food in snake.body or new_food==snake.head:
			new_food=Vector2(randint(1,width-1),randint(1,height-1))
		self.grow()
		return new_food

	def grow(self):
		last_part=Vector2(self.body[-1].x,self.body[-1].y)
		self.body.append(last_part)

clock=time.Clock()
delta,max_tps,width,height=0.0,40,40,20
idict={'w':(0,-1),'s':(0,1),'a':(1,0),'d':(-1,0)}
key=(1,0)
keys=[key]
snake=snake()
food=Vector2(randint(1,width-1),randint(1,height-1))

while snake.alive:
	delta += clock.tick()/1000.0
	while delta > 1/max_tps:
		delta -= 1/max_tps
		food = snake.eat() if food==snake.head else food
		key=find_path(food)[0]
		draw()
		if not snake.move():
			draw()
			break	
		
while True:
	pass