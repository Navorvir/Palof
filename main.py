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

palourde = palourde.palourde(screen,0,0)

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
    liste_bloc = [bloc1,bloc2]

    for i in range(2):
        pygame.draw.rect(screen,((i+1)*70,(i+1)*50,120),liste_bloc[i])

    palourde.frame_palourde(liste_bloc)

    pygame.display.update()