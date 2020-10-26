# wall = -1
# start = 0
# end = 1000
# start is according to the pos nomenclature
# x also is accordind to the pos nomenclature which means first element is the x coordinate 
# and the second is the y coordinate, for arrays it should be like A[sy][sx]
import pygame, time, sys, copy

from pygame.locals import*

pygame.init()

W = 600
H = 600
DISPLAY = pygame.display.set_mode((W, H))
WHITE = (255, 255, 255)
CRIMSON = (220, 20, 60)
LAWN_GREEN = (124, 252, 0)
AQUA = (0, 255, 255)
node_colour = [LAWN_GREEN, CRIMSON, AQUA]
n = 1
flag = 0
start = [0,0]
end = [0,0]
A = [[100 for i in range(30)] for j in range(30)]
next_L = []


def draw_node(pos, n, A):
	if n == 1:
		A[start[1]][start[0]] = 0
	if n == 2:
		A[end[1]][end[0]] = 1000
	pygame.draw.rect(DISPLAY, node_colour[n-1], ((pos[0]//20)*20, (pos[1]//20)*20, 20, 20))
	pygame.display.update()

def draw_wall(pos):
	A[pos[1]//20][pos[0]//20] = -1
	pygame.draw.rect(DISPLAY, node_colour[2], ((pos[0]//20)*20, (pos[1]//20)*20, 20, 20))


def draw_grid(W, H):
	for w in range(0, 600, 20):					#vertical lines
		pygame.draw.line(DISPLAY, WHITE, (w, 0), (w, W), 1)
	for h in range(0, 600, 20):					#horizontal lines
		pygame.draw.line(DISPLAY, WHITE, (0, h), (H, h), 1)

def map(start):
	run  = True
	L = [[0,0]]
	counter = 1
	L[0] = start
	while(run):
		for x in L :
			sy = x[1]
			sx = x[0]
			if((A[sy][sx+1]!=1000 or A[sy+1][sx]!=1000 or A[sy][sx-1]!=1000 or A[sy-1][sx]!=1000) and ( (sx>=0 and sx<=29) and (sy>=0 and sy<=29) ) ):
				if(A[sy][sx+1]!=-1 and A[sy][sx+1] == 100):
					A[sy][sx+1] = counter
					next_L.append([sx+1,sy])
				if(A[sy+1][sx]!=-1 and A[sy+1][sx] == 100):
					A[sy+1][sx] = counter
					next_L.append([sx,sy+1])
				if(A[sy][sx-1]!=-1 and A[sy][sx-1] == 100):
					A[sy][sx-1] = counter
					next_L.append([sx-1,sy])
				if(A[sy-1][sx]!=-1 and A[sy-1][sx] == 100):
					A[sy-1][sx] = counter
					next_L.append([sx,sy-1])
			if( A[sy][sx+1]==1000 or A[sy+1][sx]==1000 or A[sy][sx-1]==1000 or A[sy-1][sx]==1000 ):
				run = False
		L = next_L.copy()
		next_L.clear()
		counter += 1
	find_path()

def find_path():
	path = []
	minimum = 1000
	sx = end[0]
	sy = end[1]
	if ( (sx+1>=0 and sx+1<=29) and (sy>=0 and sy<=29) ):	#this statement is put here to avoid error when corner points are chosen but that should be put whereever i am using ex-1
		if(A[sy][sx+1] < minimum):
			minimum = A[sy][sx+1]
			path.append([sx+1, sy])
	if ( (sx>=0 and sx<=29) and (sy+1>=0 and sy+1<=29) ):
		if(A[sy+1][sx] < minimum):
			minimum = A[sy+1][sx]
			path.clear()
			path.append([sx,sy+1])
	if ( (sx-1>=0 and sx-1<=29) and (sy>=0 and sy<=29) ):
		if(A[sy][sx-1] < minimum):
			minimum = A[sy][sx-1]
			path.clear()
			path.append([sx-1,sy])
	if( (sx>=0 and sx<=29) and (sy-1>=0 and sy-1<=29) ):
		if(A[sy-1][sx] < minimum):
			minimum = A[sy-1][sx]
			path.clear()
			path.append([sx,sy-1])
	step = minimum
	ex = path[0][0]
	ey = path[0][1]
	while(step > 1):
		post = 0
		if( A[ey][ex+1]==step-1 or A[ey+1][ex]==step-1 or A[ey][ex-1]==step-1 or A[ey-1][ex]==step-1 ):
			if(A[ey][ex+1]==step-1 and post == 0):
				path.append([ex+1,ey])
				post = 1
				ex = ex+1
			if(A[ey+1][ex]==step-1 and post == 0):
				path.append([ex,ey+1])
				post = 1
				ey = ey+1
			if(A[ey][ex-1]==step-1 and post == 0):
				path.append([ex-1,ey])
				post = 1
				ex = ex-1
			if(A[ey-1][ex]==step-1 and post == 0):
				path.append([ex,ey-1])
				post = 1
				ey = ey-1
		step = step-1
	for p in path:
		pygame.draw.rect(DISPLAY,WHITE,((p[0])*20,(p[1])*20,20,20))
		pygame.display.update()

running = True
while(running):
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			if (n<=2):
				if n == 1 :
					start[0] = pos[0]//20
					start[1] = pos[1]//20
				if n == 2 :
					end[0] = pos[0]//20
					end[1] = pos[1]//20
				draw_node(pos, n, A)
				if n == 2 :
					flag = 1
			n += 1
		if flag == 1:
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				draw_wall(pos)
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				flag = 0
				map(start)
	draw_grid(W, H)
	pygame.display.update()