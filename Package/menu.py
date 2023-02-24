import pygame
import sys
import oldPalourde as palourde # liéer avec la nouvelle palourde
import bouton

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
largeur_ecran = pygame.display.get_window_size()[0]
hauteur_ecran = pygame.display.get_window_size()[1]
running = True
game = False

def quit():
    running = False
    pygame.quit()
    sys.exit()
    

def positionner(x,y):
    palourde.x = x
    palourde.y = y

FPS = 60
clock = pygame.time.Clock()

palourde = palourde.Palourde(screen,0,0)

test = 0
r = 0
g = 0
b = 0
etape_menu = 1



image_mode_course_bouton = pygame.image.load("Bouton_mode_course.png")
image_mode_coop_bouton = pygame.image.load("Bouton_mode_coop.png")
image_mode_versus_bouton = pygame.image.load("Bouton_mode_versus.png")

mode_course_bouton = bouton.bouton(largeur_ecran-pygame.Surface.get_width(image_mode_course_bouton), hauteur_ecran/3, screen, image_mode_course_bouton)
mode_coop_bouton = bouton.bouton(0,hauteur_ecran/3, screen, image_mode_coop_bouton)
mode_versus_bouton = bouton.bouton(largeur_ecran/2, 0, screen, image_mode_versus_bouton)

hauteur_sol = 50
sol = pygame.Rect(0,hauteur_ecran-hauteur_sol,1500,hauteur_sol)
positionner(largeur_ecran/3,hauteur_ecran-hauteur_sol)

while running:
    clock.tick(FPS)
    test+=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                etape_menu = 1
                game = False
                positionner(largeur_ecran/3,hauteur_ecran-hauteur_sol)

    screen.fill((r,g,b))
    
    if game == False:
        liste_bloc = [sol]
        
        if etape_menu == 1:
            r=0
            g=0
            b=0
            liste_bloc = [sol]
            if palourde.palourdeRect.clipline(largeur_ecran,0,largeur_ecran,hauteur_ecran):
                positionner(5,palourde.y)
                etape_menu = 2
 
        if etape_menu == 2:
            if palourde.palourdeRect.clipline(0,0,0,hauteur_ecran):
                positionner(largeur_ecran-palourde.LARGEUR,palourde.y)
                etape_menu = 1

            mode_course_bouton.draw()
            mode_coop_bouton.draw()
            mode_versus_bouton.draw()

            if mode_course_bouton.pressed():
                mode = "mode course"
                game = True
                etape_menu = 0
                positionner(0,0)

            if mode_coop_bouton.pressed():
                mode = "mode coop"
                game = True
                etape_menu = 0
                positionner(0,0)

            if mode_versus_bouton.pressed():
                mode = "mode versus"
                game = True
                etape_menu = 0
                positionner(0,0)

    if game:
        if mode == "mode course":
            r = 50
        elif mode == "mode coop":
            g = 50
        elif mode == "mode versus":
            b = 50

        bloc1 = pygame.Rect(0,400,200,50)
        bloc2 = pygame.Rect(500, 400, 200, 50)
        liste_bloc = [bloc1,bloc2]
            
    for i in range(len(liste_bloc)):
        pygame.draw.rect(screen,((i+1)*70,(i+1)*50,120),liste_bloc[i])

    palourde.framePalourde(liste_bloc)

    pygame.display.update()