import sys
import pygame
import palourde


pygame.init()

screen = pygame.display.set_mode((1500, 900))

running = True

def quit():
    running = False
    pygame.quit()
    sys.exit()



FPS = 60
clock = pygame.time.Clock()

palourde = palourde.Palourde(screen,50,50)

test = 0
r = 0
g = 0
b = 0


while running:
    clock.tick(FPS)

    test+=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill((r,g,b))

    bloc1 = pygame.Rect(0,400,200,50)
    bloc2 = pygame.Rect(500, 400, 200, 50)
    bloc3 = pygame.Rect(700, 200, 200, 150)
    bloc4 = pygame.Rect(200, 800, 400, 50)
    bloc5 = pygame.Rect(0, 650, 200, 150)
    bloc6 = pygame.Rect(600, 650, 200, 150)
    bloc7 = pygame.Rect(0, 500, 100, 50)
    bloc8 = pygame.Rect(400, 500, 100, 200)

    liste_bloc = [bloc1,bloc2,bloc3,bloc4,bloc5,bloc6,bloc7,bloc8]

    for i in range(len(liste_bloc)):
        pygame.draw.rect(screen,(100+i*11,255-20*i,255 - i*10),liste_bloc[i])

    palourde.framePalourde(liste_bloc)

    pygame.display.update()