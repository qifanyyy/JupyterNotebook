import pygame
import math
#return different thing from find

CLOSEENOUGH = 50


def main():

    pygame.init()
    screen = pygame.display.set_mode((400,400))
    nodes = [Node(100,100,0)]

    connecting = []
    pathFinding = []

    path = []

    pop = 0

    clock = pygame.time.Clock()

    while True:

        clock.tick(30)
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if pygame.mouse.get_pressed()[0]:
                    mx,my = pygame.mouse.get_pos()
                    
                    if nearestDis(nodes,mx,my) >CLOSEENOUGH:
                        pop+=1
                        nodes.append( Node(mx,my,pop) )
                    else:
                        connecting.append(nearestNode(nodes,mx,my))

                elif pygame.mouse.get_pressed()[2]:
                    mx,my = pygame.mouse.get_pos()
                    
                    if nearestDis(nodes,mx,my)<CLOSEENOUGH:
                        pathFinding.append(nearestNode(nodes,mx,my))

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f:
                    mx,my = pygame.mouse.get_pos()
                    near = nearestNode(nodes,mx,my)
                    print()
                    print('This node is',near)
                    print('Connected: ')
                    for node in near.con:
                        print(node)
                    print('Path to: ')
                    for node in near.path:
                        print(node)
                    print()
                    
                    
                        
        if len(connecting)>1:
             n1,n2=connecting
             if n1!=n2:
                 connect(n1,n2, math.hypot(n1.px-n2.px,n1.py-n2.py))
             connecting=[]

        if len(pathFinding)>1:

            for n in nodes:
                n.path = []
                n.length = 1000

            n1,n2 = pathFinding
            pathFinding = []
            path = find(n1,n2)
            
        for n in path:
            pygame.draw.circle(screen,(255,0,0),(n.px,n.py),10)

            
        

        for n in nodes:
            pygame.draw.circle(screen, (255,255,255), (n.px,n.py), 5 )

            for p in n.con:
                pygame.draw.line(screen, (255,255,0), (n.px,n.py),(p.px,p.py) )
    
    
        pygame.display.update()





class Node():

    def __init__(self,x,y,n):

        self.px,self.py = x,y

        self.n = n
        self.con = {}
        self.path = []
        self.length = 1000

    def __str__(self):
        return(str(self.n))


def connect(n1,n2,length):
    n1.con[n2]=length
    n2.con[n1]=length

def updateQueue(queue,node):
    queue.extend( [(node,n) for n in node.con] )
    
def nearestNode(nodes,x,y):
    return min( nodes, key = lambda n:math.hypot(x-n.px,y-n.py) )

def nearestDis(nodes,x,y):
    n = nearestNode(nodes,x,y)
    return math.hypot(x-n.px,y-n.py)

def find(start, end):

    queue = []

    start.path = [start]
    start.length = 0

    updateQueue(queue, start)
    #queue.extend([(start,n) for n in start.con])

    while queue:
        c1,c2 = queue.pop(0)
        if c1.length+c1.con[c2]<c2.length:
            c2.path = c1.path+[c2]
            c2.length = c1.length+c1.con[c2]
            
            updateQueue(queue,c2)

    

    return end.path


#print( find(n0,n1) )

#for node in nodes:
#    print(node.n,node.length)
        
        


if __name__ == '__main__':
    main()











    
