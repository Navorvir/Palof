import sys
import pygame
from Package.Game.Palourde.palourde import Palourde
from Package.Game.Palourde.camera import CameraGroup
import time

class Game():
    def __init__(self):
        # ===== CONSTANTES =====
        self.FPS = 60

        # ===== VARIABLES =====
        self.running = True
        self.background = (0,200,0)

        pygame.init()
        self.SCREEN = pygame.display.set_mode((1280,720))
        self.displaySurface = pygame.display.get_surface()   
        
        self.CLOCK = pygame.time.Clock()

        self.CAMERA = CameraGroup(self.displaySurface)    

        self.PALOURDE = Palourde(self.SCREEN,50,50)


    def loadTestMap(self):
        blocs = [
            {"x" : 0 , "y": 400, "width" : 200, "height" : 50},
            {"x" : 500, "y": 400, "width" : 200, "height" : 50},
            {"x" : 700, "y": 200, "width" : 200, "height" : 150},
            {"x" : 200, "y": 800, "width" : 400, "height" : 50},
            {"x" : 0, "y": 650, "width" : 200, "height" : 150},
            {"x" : 600, "y": 650, "width" : 200, "height" : 150},
            {"x" : 0, "y": 100, "width" : 100, "height" : 50},
            {"x" : 400, "y": 100, "width" : 100, "height" : 200},
        ]


        liste_bloc = []

        for bloc in blocs:
            liste_bloc.append(pygame.Rect(bloc["x"], bloc["y"], bloc["width"], bloc["height"]))

        self.CAMERA.loadGame(listSprites=liste_bloc)

    def updateGame(self):
        self.SCREEN.fill(self.background)

        # INPUTS
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q] or keys[pygame.K_LEFT]:			
            self.CAMERA.go_Left()
            self.PALOURDE.marche(-1)

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:			
            self.PALOURDE.marche(1)
            self.CAMERA.go_Right()

        if self.PALOURDE.isFalling == True:
            self.PALOURDE.tomber()
            self.CAMERA.go_Bottom(self.PALOURDE.vitesseChute / 100 )

        elif keys[pygame.K_SPACE]:
            self.PALOURDE.saut()
            self.CAMERA.go_Top( -self.PALOURDE.vitesseChute / 90)
            


        if keys[pygame.K_e]:
            self.PALOURDE.rotation(-1)
        elif keys[pygame.K_a]:
            self.PALOURDE.rotation(1)

        if keys[pygame.K_b]:
            self.CAMERA.toggleCameraMove()
            time.sleep(0.2)


        # Update Affichage
        self.CAMERA.updateDisplay()
        self.PALOURDE.framePalourde(self.CAMERA.getSpriteActual())
        pygame.display.update()

    
    def run(self):

        while self.running:
            self.CLOCK.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.quit()

            self.updateGame()

            pygame.display.update()       
            # print(self.PALOURDE.vitesseChute ) 
            print(self.PALOURDE.speed ) 
        

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()
          

if __name__ == "__main__":
    game = Game()
    game.loadTestMap()
    game.run()