import sys
import pygame
from Package.Game.Palourde.palourde import Palourde
from Package.Game.Palourde.camera2 import CameraGroup
import time
from Package.menu2 import Menu
from Package.Game.json.test_json import Map


class Game():
    def __init__(self):
        # ===== CONSTANTES =====
        self.FPS = 60

        # ===== VARIABLES =====
        self.running = True
        self.background = (0,200,0)

        pygame.init()
        self.largeur_ecran = 1280
        self.hauteur_ecran = 720
        self.SCREEN = pygame.display.set_mode((self.largeur_ecran,self.hauteur_ecran))
        self.displaySurface = pygame.display.get_surface()   
        
        self.CLOCK = pygame.time.Clock()

        self.CAMERA = CameraGroup(self.displaySurface)    

        self.PALOURDE = Palourde(self.SCREEN,50,50)
        
        self.menu = Menu(self.largeur_ecran, self.hauteur_ecran, self.SCREEN, self.PALOURDE)

    def loadTestMap(self, map):
        testMap = Map()
        testMap.traitement(map)
        listObject = testMap.listObject

        self.CAMERA.loadGame(listSprites=listObject)

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
        self.CAMERA.updateDisplay(self.PALOURDE)
        #self.PALOURDE.framePalourde(self.CAMERA.getSpriteActual())
        pygame.display.update()

    
    def run(self):
        game.loadTestMap(self.menu.map)
        self.background = self.menu.background
        self.CAMERA.toggleCameraMove()
        while self.running:
            self.CLOCK.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.quit()
                    
            if self.menu.etape_menu != self.menu.NONE:
                self.menu.update()
                self.updateGame()
            else:
                self.loadTestMap(blocs)
                self.updateGame()

            pygame.display.update()       
            # print(self.PALOURDE.vitesseChute ) 
            print(self.PALOURDE.speed)
        

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()
        

if __name__ == "__main__":
    game = Game()
    game.run()
