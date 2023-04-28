from os import path
import sys
import pygame
import time

from Package.Game.palourde import Palourde, OtherPalourde
from Package.Game.camera import CameraGroup
from Package.display.menu import Menu
from Package.managementJson import Map

from Package.network.server import Server
from Package.network.client import Client
import threading

        
class Game():
    def __init__(self):

        pygame.init()

        # ==================== CONSTANTES ==================

        # PARAMAETRES DU JEU
        self.FPS : int = 60
        self.SCREEN_WIDTH : int = 1280
        self.SCREEN_HEIGHT : int = 720

        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.DISPLAY_SURFACE = pygame.display.get_surface()   

        self.CAMERA : CameraGroup= CameraGroup(self.DISPLAY_SURFACE)  
  
        self.PALOURDE : Palourde = Palourde(self.SCREEN,50,50)
        self.ALL_PALOURDES : dict = {}

        self.NETWORK_OBJECT = None


        self.MENU : Menu = Menu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCREEN, self.PALOURDE, self.CAMERA)

        # PARAMETRES SUBTILES
        self.BACKGROUND : tuple(int, int, int) = (131,181,214)
        self.BACKGROUND_IMAGE = pygame.image.load(path.join("Assets/Background/background_palof.png"))


        # ==================== VARIABLES ===================
        self.running : bool = True
        self.gameStarted : bool = False
        self.clientEnable : bool = False
        self.modeVersus : bool = False

        self.problem : str = ""
        self.frameFin = 0


        
        # Background
        self.spriteBackground : list = [self.BACKGROUND_IMAGE,self.BACKGROUND_IMAGE]
        self.cooBackground :list = [[0,-500],[1920,-500]]


    # ================== METHODES =======================

    # Methodes controle etat game
    def run(self) -> None:
        # self.BACKGROUND = self.MENU.BACKGROUND
        self.lockCamera()

        # Boucle Principale du jeu
        while self.running:
            self.CLOCK.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    self.MENU.checkInput(event)
              
            
         

            self.updateGame()
           
            pygame.display.update()           
    

                
    def quit(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()
        
    def updateGame(self) -> None:
        self.SCREEN.fill(self.BACKGROUND)
        # self.background()
        if self.PALOURDE.mort:
            threading.Timer(0.2, self.gameOver) # evite qu'il soit bloqué à 1 coté serveur

        if self.MENU.switchSceneEnable == True:
            self.loadMap(self.MENU.map)
            self.MENU.switchSceneEnable = False
        self.MENU.update()
        
        

        # INPUTS
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.PALOURDE.roulement(1)

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.PALOURDE.roulement(-1)
        else:
            self.PALOURDE.roule = False

        #nouveau
        if keys[pygame.K_LSHIFT] and self.PALOURDE.modeVersus == True:
            self.PALOURDE.attaquePalourde()
            self.detectionCoupPalourde()
        

        if self.PALOURDE.timeChute <= 6 / 30 and self.PALOURDE.onGround == True and (keys[pygame.K_SPACE] or keys[pygame.K_UP]):
            self.PALOURDE.saut()

        self.CAMERA.moveCamera(self.PALOURDE.xCamera,self.PALOURDE.yCamera)

           # Update Affichage
        self.CAMERA.updateDisplay(self.PALOURDE)

        #Initialisation de la sauvegarde des palourde pour effectuer les événements des objets spéciaux
        self.palourdeEvenement = [self.PALOURDE]

        if self.NETWORK_OBJECT != None and self.gameStarted and self.NETWORK_OBJECT.gameStarted:
            self.updateOtherPalourde()
        
        #Traitement pour déterminer si la partie est finie
        if self.modeVersus == True:
            nbPalourde = 0
            if self.PALOURDE.mort == True:
                nbPalourde += 1
        
        if self.frameFin <= 0:
            self.evenementObjet()
        else:
            self.frameFin -= 1
        if self.frameFin == 1:
            self.retourMenu()
        

        self.PALOURDE.framePalourde(self.CAMERA.getSpriteActual())
        pygame.display.update()        
    
    def updateOtherPalourde(self):
        data = self.NETWORK_OBJECT.getData()

        # Vérifie si toutes les palourdes on bien été connecté
        for id in data.keys():
            if id not in self.ALL_PALOURDES.keys() and self.NETWORK_OBJECT.ID_CLIENT_HOST != int(id) \
            and "connected" in data[id] and data[id]["connected"] != False:
                
                self.ALL_PALOURDES[id] = OtherPalourde(self.SCREEN, 0, 0, id) 
                if self.MENU.mode == self.MENU.MODE_VERSUS:
                    self.ALL_PALOURDES[id].changementModeVersus()


            elif int(id) != self.NETWORK_OBJECT.ID_CLIENT_HOST and id in data and data[id]["connected"] == False:
                self.playerLeave(id)

        # Met à jour la scène pour les autres palourdes
        for id in self.ALL_PALOURDES.keys():
            if int(id) != self.NETWORK_OBJECT.ID_CLIENT_HOST and data[id]["sante"] > 0:   
                self.ALL_PALOURDES[id].x = data[id]["x"] + self.CAMERA.startX
                self.ALL_PALOURDES[id].y = data[id]["y"] + self.CAMERA.startY

                self.ALL_PALOURDES[id].angle = data[id]["angle"]
                self.ALL_PALOURDES[id].rotation(1)
                self.ALL_PALOURDES[id].placement()
                self.CAMERA.appendPalourde(self.ALL_PALOURDES[id].rect)
            


        

    def background(self) -> None:
        self.cooBackground[0][0]= self.PALOURDE.xCamera // 1920 * 1920 - self.PALOURDE.xCamera 
        self.cooBackground[1][0]= (self.PALOURDE.xCamera // 1920 + 1) * 1920 - self.PALOURDE.xCamera 
        
        for i in range(2):
            self.SCREEN.blit(self.spriteBackground[i], (self.cooBackground[i][0], self.cooBackground[i][1]))

    def lockCamera(self, x : int = 500, y : int = 250) -> None:
      
        self.PALOURDE.lockCamera(x,y)
        self.CAMERA.lockCamera()

    def unlockCamera(self) -> None:
        self.PALOURDE.cameraLock = False
        self.CAMERA.unlockCamera()

    def tranformCoo(self, xUser : str | int |float , yUser: str | int |float ) -> int | float:
        if xUser == "center":
            x = (self.PALOURDE.surface.get_width() - self.PALOURDE.LARGEUR) // 2
        elif xUser == "end":
            x = self.PALOURDE.surface.get_width() - self.PALOURDE.LARGEUR - 10
        elif xUser == "start":
            x = 0
        elif xUser == "current":
            x = self.PALOURDE.x
        else:
            x = xUser

        if yUser == "center":
            y = (self.PALOURDE.surface.get_height()-self.PALOURDE.HAUTEUR)//2
        elif yUser == "current":
            y = self.PALOURDE.y
        elif yUser == "start":
            y = 0
        elif yUser == "end":
            y = self.PALOURDE.y - self.PALOURDE.HAUTEUR- 10
        else:
            y = yUser
        
        return x, y

    def waitGameStarted(self) -> None:

        while not self.NETWORK_OBJECT.gameStarted:
            time.sleep(0.5)
            
        self.gameStarted = True
        self.MENU.mode = self.NETWORK_OBJECT.mode

        # Mettre les bonnes options suivant le mode
        if self.MENU.mode == self.MENU.MODE_VERSUS:
            self.PALOURDE.changementModeVersus()
        else:
            self.PALOURDE.changementModeNormal()

        time.sleep(1) # laisse un peu de temps au chargement
        self.loadMap(self.NETWORK_OBJECT.levelName)

    def gameOver(self):
        self.MENU.listObjectInstancies["text"]["gameOver"].setText("Game Over!")
        self.NETWORK_OBJECT.gameStarted = False

    def loadMap(self, map : str) -> None:
        testMap = Map()

 
        
        testMap.traitement(map)
  
        listObject = testMap.listObject
        self.MENU.listObjectInstancies = testMap.get_ObjectInstancies()

        xSpawn, ySpawn = self.tranformCoo(testMap.spawnCoordonate["x"], testMap.spawnCoordonate["y"])
        self.PALOURDE.x, self.PALOURDE.y = xSpawn, ySpawn
      
        # Configure la Caméra
        self.CAMERA.loadGame(listSprites=listObject)

        if testMap.lockCamera:
            self.lockCamera(xSpawn,ySpawn)
        else:
            self.unlockCamera()

            
        # Afficher les textes
        self.MENU.loadInput()
        self.MENU.loadButton()
        self.MENU.loadText()

        if self.MENU.NAME_MENU["waitStart"]["path"] == self.MENU.map:
            self.createParty()
            self.MENU.listObjectInstancies["text"]["code"].setText("code : " + self.NETWORK_OBJECT.CODE)
            self.MENU.listObjectInstancies["button"]["startGame"].setCommand(self.startParty)

        elif self.MENU.NAME_MENU["wait"]["path"] == self.MENU.map and not self.clientEnable:
            self.joinParty()
            self.clientEnable = True   

   
   
    def createParty(self) -> None:
        self.NETWORK_OBJECT = Server(self.PALOURDE)
   
        threading.Thread(target=self.NETWORK_OBJECT.startServer, daemon=True).start()
        self.NETWORK_OBJECT.setTypeGame(self.MENU.mode,self.MENU.mapChose)


    def startParty(self):
        time.sleep(1)

        self.NETWORK_OBJECT.startGame()
        self.gameStarted = True

        time.sleep(1)
        self.MENU.startParty()


    def joinParty(self) -> None:
        self.NETWORK_OBJECT = Client(self.PALOURDE)
        self.MENU.listObjectInstancies["input"]["networkCode"].setCommand(self.checkCode)
   

    def checkCode(self, code) -> None:
        self.NETWORK_OBJECT.setMacServerAddress(code)
        if self.NETWORK_OBJECT.startClient():
            threading.Thread(target=self.waitGameStarted, daemon=True).start()
            self.MENU.listObjectInstancies["text"]["probleme"].setText("Le client s'est connecté. Attend que le serveur lance la partie...")
        else:
            self.MENU.listObjectInstancies["text"]["probleme"].setText(self.NETWORK_OBJECT.problem)

    def playerLeave(self, idPalourde : int) -> None:
        if idPalourde in self.ALL_PALOURDES:
            self.ALL_PALOURDES.pop(idPalourde)

    
    def detectionCoupPalourde(self):
        for id, autrePalourde in self.ALL_PALOURDES.items():
            for rect in autrePalourde.rect:
                if pygame.Rect.colliderect(rect,self.PALOURDE.brasGaucheRectRotation):
                    self.NETWORK_OBJECT.sendTemporyParameter("sens", -1,id)

                if pygame.Rect.colliderect(rect,self.PALOURDE.brasDroitRectRotation):
                    self.NETWORK_OBJECT.sendTemporyParameter( "sens", -1,id)

    def retourMenu(self):
        if len(self.palourdeEvenement) > 1 :
            self.NETWORK_OBJECT.close()
        self.MENU.switchMenu("title")
        self.lockCamera                 

    def evenementObjet(self) -> None:
        if "ligneArrivee" in self.MENU.listObjectInstancies:
            for ligneArrivee in self.MENU.listObjectInstancies["ligneArrivee"].values():
                if ligneArrivee.verification(self.palourdeEvenement,self.PALOURDE.xCamera,self.PALOURDE.yCamera) == True:
                    self.frameFin = 200

if __name__ == "__main__":
    game = Game()
    game.run()