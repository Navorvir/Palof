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

        if pygame.key.get_pressed()[pygame.K_q] or pygame.key.get_pressed()[pygame.K_LEFT]:
            self.PALOURDE.roulement(1)

        elif pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.PALOURDE.roulement(-1)

        if self.PALOURDE.isFalling == True:
            self.PALOURDE.tomber()


        elif self.PALOURDE.timeChute <= 6 / 30 and  (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_UP]):
            self.PALOURDE.saut()

        self.CAMERA.moveCamera(self.PALOURDE.xCamera,self.PALOURDE.yCamera)
            


        if keys[pygame.K_e]:
            self.PALOURDE.rotation(-1)
        elif keys[pygame.K_a]:
            self.PALOURDE.rotation(1)

        if keys[pygame.K_b]:
            self.CAMERA.toggleCameraMove()
            time.sleep(0.2)


        # Update Affichage
        self.CAMERA.updateDisplay()
        print(self.CAMERA.getSpriteActual()[0])
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

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()
          

if __name__ == "__main__":
    game = Game()
    game.loadTestMap()
    game.run()
