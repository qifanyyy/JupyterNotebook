import pygame,sys,random,time
from pygame.locals import *
pygame.init()
WINDOWWIDTH=500
WINDOWHEIGHT=300
ARRWIDTH=400
BOXWIDTH=4
SPACE=1
FPS=5
#colors
WHITE       = (255,255,255)
BLACK       = (  0,  0,  0)
RED         =  (255,  0,  0)
BLUE        = (  0,  0,255)
DARKGRAY    = ( 40, 40, 40)
GREEN       = (  0,255,  0)
POWDER_BLUE = (176,224,230)


SURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
BASICFONT = pygame.font.Font('freesansbold.ttf', 13)
pygame.display.set_caption('Sorting')
SURF.fill(POWDER_BLUE)
#functions
def terminate():
    pygame.quit()
    sys.exit()
def generate_array():
    length=int(ARRWIDTH/(BOXWIDTH+SPACE))
    arr=[i*2 for i in range(length-1)]
    random.shuffle(arr)
    return arr
def draw_box(i,height,COLOR):
    x=(i*(BOXWIDTH+SPACE))+int((WINDOWWIDTH-ARRWIDTH)/2)
    pygame.draw.rect(SURF,COLOR,(x,WINDOWHEIGHT-50,BOXWIDTH,-height))
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('space-array,s-SelectionSort,b-BubbleSort',
                                    True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (5,5)
    SURF.blit(pressKeySurf, pressKeyRect)


#Algoritms
def bubbleSort(arr): 
    n = len(arr) 
    for i in range(n):    
        for j in range(0, n-i-1): 
            SURF.fill(POWDER_BLUE)
            for k in range(len(arr)):
                if k==j or k==j+1:
                    COLOR=RED
                else:
                    COLOR=BLUE
                draw_box(k,arr[k],COLOR)
            pygame.display.update()
  
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                SURF.fill(POWDER_BLUE)
                for k in range(len(arr)):
                    if k==j or k==j+1:
                        COLOR=GREEN
                    else:
                        COLOR=BLUE
                    draw_box(k,arr[k],COLOR)
                pygame.display.update()
#Selection Sort
def SelectionSort(arr):
    
    for i in range(len(arr)): 
 
        min_idx = i 
        for j in range(i+1, len(arr)):
            SURF.fill(POWDER_BLUE)
            for k in range(len(arr)):
                if k==min_idx or k==j:
                    COLOR=RED
                else:
                    COLOR=BLUE
                draw_box(k,arr[k],COLOR)
            pygame.display.update()
            if arr[min_idx] > arr[j]: 
                min_idx = j 

                 
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        SURF.fill(POWDER_BLUE)
        for k in range(len(arr)):
            if k==i or k==min_idx:
                COLOR=GREEN
            else:
                COLOR=BLUE
            draw_box(k,arr[k],COLOR)
        pygame.display.update()



while True:
    fps=pygame.time.Clock()
    drawPressKeyMsg()
    for event in pygame.event.get():
        if event.type==QUIT:
            terminate()
        elif event.type==KEYDOWN:
            if event.key==K_SPACE:
                SURF.fill(POWDER_BLUE)
                arr=generate_array()
                for i in range(len(arr)):
                    draw_box(i,arr[i],BLUE)
            if event.key==K_UP: 
                SURF.fill(POWDER_BLUE)
                a=sorted(arr)
                for i in range(len(a)):
                    COLOR=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    draw_box(i,a[i],COLOR)
            if event.key==K_b:
                if arr!=sorted(arr):
                    bubbleSort(arr)
            if event.key==K_s:
                if arr!=sorted(arr):
                    SelectionSort(arr)
                
    pygame.display.update()
    fps.tick(2)
