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
    """Objet Primaire de ce projet permetant de relier toutes les fonctionnalités du jeu. De plus, il permet de controler de le jeu
    """

    def __init__(self):
        """Initialise les variables et les constantes
        """

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
        self.modeVersus : bool = False

        self.problem : str = ""

        self.frameFin : int = 0
        self.etapeEscape : int = 0
        
        # Background
        self.spriteBackground : list = [self.BACKGROUND_IMAGE,self.BACKGROUND_IMAGE]
        self.cooBackground :list = [[0,-500],[1920,-500]]


    # ================== METHODES =======================

    # --------------- Methodes Principale ----------------
    def run(self) -> None:
        """Lance la boucle du jeu mettant à jour l'affichage
        """

        # Par Tout le monde


        self.lockCamera()

        # Boucle Principale du jeu
        while self.running:
            self.CLOCK.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    self.MENU.checkInput(event)

                    if event.key == pygame.K_ESCAPE:

                        if self.MENU.stepMenu == None:
                            if self.etapeEscape == 0:
                                self.timeMesure = pygame.time.get_ticks()
                                self.etapeEscape = 1
                            elif pygame.time.get_ticks()-self.timeMesure <2000:
                                self.retourMenu()
                                self.etapeEscape = 0
                            else :
                                self.etapeEscape=0   
         
            self.updateGame()
            pygame.display.update()           
                
    def quit(self) -> None:
        """Arrête le programme
        """

        # Par Nathan

        self.running = False
        pygame.quit()
        sys.exit()
        

    # --------------- Methodes Updates ----------------
    def updateGame(self) -> None:
        """Met à jour et vérifie de nombreux paramètres avec les entrées du joueur
        """

        # par Nathan et Robin

        self.SCREEN.fill(self.BACKGROUND)
        # self.background() # si vous avez un bon pc vous pouvez tester ça

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

        if keys[pygame.K_LSHIFT] and self.PALOURDE.modeVersus == True:
            self.PALOURDE.attaquePalourde()
            self.detectionCoupPalourde()

        if self.PALOURDE.timeChute <= 6 / 30 and self.PALOURDE.onGround == True and (keys[pygame.K_SPACE] or keys[pygame.K_UP]):
            self.PALOURDE.saut()


        # Update Affichage
        self.CAMERA.moveCamera(self.PALOURDE.xCamera,self.PALOURDE.yCamera)
        self.CAMERA.updateDisplay(self.PALOURDE)

        # Initialisation de la sauvegarde des palourde pour effectuer les événements des objets spéciaux
        self.palourdeEvenement = [self.PALOURDE]

        if self.NETWORK_OBJECT != None and self.gameStarted and self.NETWORK_OBJECT.gameStarted:
            self.updateOtherPalourde()

        # Traitement pour déterminer si la partie est finie
        if self.PALOURDE.modeVersus == True and self.frameFin <= 0 and self.MENU.stepMenu != "waitStart" and self.MENU.stepMenu != "player":
            nbPalourdeMorte = 0
            if self.PALOURDE.mort == True:
                nbPalourdeMorte += 1
            for palourde in self.ALL_PALOURDES.values():
                if palourde.sante <= 0:
                    nbPalourdeMorte += 1
                if nbPalourdeMorte >= len(self.palourdeEvenement) - 1 :
                        self.frameFin = 200

        if self.frameFin <= 0:
            self.evenementObjet()
        else:
            self.frameFin -= 1
        if self.frameFin == 1:
            self.retourMenu()
        
        # Met à jour la position de la palourde
        self.PALOURDE.framePalourde(self.CAMERA.getSpriteActual())
    
    def updateOtherPalourde(self) -> None:
        """Met à jour la position des autres palourdes, des autres joueurs avec les valeurs du client/serveur
        """

        # Par Nathan

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

                self.ALL_PALOURDES[id].sante = data[id]["sante"]

                self.ALL_PALOURDES[id].angle = data[id]["angle"]
                self.ALL_PALOURDES[id].rotation(1)
                self.ALL_PALOURDES[id].placement()
                self.CAMERA.appendPalourde(self.ALL_PALOURDES[id].rect)
                
                self.palourdeEvenement.append(self.ALL_PALOURDES[id])

    def loadMap(self, map : str) -> None:
        """Charge la map en récupérant le fichier, en positionnant la palourde et en mettant à jour les variable de la camera

        Args:
            map (str): chemin du fichier map
        """

        # Par Tout le monde

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

        elif self.MENU.NAME_MENU["wait"]["path"] == self.MENU.map and not self.MENU.clientEnable:
            self.joinParty()
            self.MENU.clientEnable = True   
   

    # --------------- Methodes Réseaux ----------------
    def joinParty(self) -> None:
        """Permet de transfomer le joueur en mode client afin de pouvoir rejoindre un serveur
        """
        # Par Nathan

        self.NETWORK_OBJECT = Client(self.PALOURDE)
        self.MENU.listObjectInstancies["input"]["networkCode"].setCommand(self.checkCode)
   
    def createParty(self) -> None:
        """Permet de transfomer le joueur en mode server afin de pouvoir faire rejoindre d'autres joueurs
        """
        # Par Nathan

        self.NETWORK_OBJECT = Server(self.PALOURDE)
   
        threading.Thread(target=self.NETWORK_OBJECT.startServer, daemon=True).start()
        self.NETWORK_OBJECT.setTypeGame(self.MENU.mode,self.MENU.mapChose)

    def startParty(self) -> None:
        """Permet de lancer la partie coté serveur
        """

        # Par Nathan

        time.sleep(1)

        self.NETWORK_OBJECT.startGame()
        self.gameStarted = True

        time.sleep(1)
        self.MENU.startParty()
    
    def waitGameStarted(self) -> None:
        """ Coté client attend que le serveur lance pour changer de scène
        """

        # Par Nathan

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

    def checkCode(self, code : str) -> None:
        """Tente de se connecter au serveur. Si il arrive il affiche un message de succès et il le waitGameStarted mais si il ne réussit pas
           il affiche un message d'erreur

        Args:
            code (str): code provenant du seveur
        """
        # Nathan

        self.NETWORK_OBJECT.setMacServerAddress(code)
        if self.NETWORK_OBJECT.startClient():
            threading.Thread(target=self.waitGameStarted, daemon=True).start()
            self.MENU.listObjectInstancies["text"]["probleme"].setText("Le client s'est connecté. Attend que le serveur lance la partie...")
        else:
            self.MENU.listObjectInstancies["text"]["probleme"].setText(self.NETWORK_OBJECT.problem)
    
    
    # --------------- Methodes Cameras ----------------
    def background(self) -> None:
        """ Génére le déplacement du fond d'écran (optionelle car consomme beaucoup)
        """
        # Robin

        self.cooBackground[0][0]= self.PALOURDE.xCamera // 1920 * 1920 - self.PALOURDE.xCamera 
        self.cooBackground[1][0]= (self.PALOURDE.xCamera // 1920 + 1) * 1920 - self.PALOURDE.xCamera 
        
        for i in range(2):
            self.SCREEN.blit(self.spriteBackground[i], (self.cooBackground[i][0], self.cooBackground[i][1]))

    def lockCamera(self, x : int = 500, y : int = 250) -> None:
        """Permet de bloqué la caméra

        Args:
            x (int, optional): coordonné x où elle doit se bloqué. Defaults to 500.
            y (int, optional): coordonné y où elle doit se bloqué. Defaults to 250.
        """

        # Nathan et Robin
      
        self.PALOURDE.lockCamera(x,y)

    def unlockCamera(self) -> None:
        """Permet de débloqué la caméra pour qu'elle bouge suivant la position de la palourde
        """

        self.PALOURDE.cameraLock = False
        self.CAMERA.unlockCamera()


    # ----- Methodes Controle etat du jeu --------
    def gameOver(self) -> None:
        """Afficher le Game Over dans le Versus avec l'aide de l'objet text qui a comme name "gameOver"
        """
        # Nathan

        self.MENU.listObjectInstancies["text"]["gameOver"].setText("Game Over!")
        self.NETWORK_OBJECT.gameStarted = False
    
    def detectionCoupPalourde(self) -> None:
        """Envoie une requete si il y a un contacte entre la palourde et l'une des autres palourdes
        """

        # Par Robin et Nathan

        for id, autrePalourde in self.ALL_PALOURDES.items():
            for rect in autrePalourde.rect:
                if pygame.Rect.colliderect(rect,self.PALOURDE.brasGaucheRectRotation):
                    if 90 < self.PALOURDE.angle < 270 : 
                        self.NETWORK_OBJECT.sendTemporyParameter("sens", 1,id)
                    else:
                        self.NETWORK_OBJECT.sendTemporyParameter("sens", -1,id)

                if pygame.Rect.colliderect(rect,self.PALOURDE.brasDroitRectRotation):
                    if 90 < self.PALOURDE.angle < 270 : 
                        self.NETWORK_OBJECT.sendTemporyParameter("sens", -1,id)
                    else:
                        self.NETWORK_OBJECT.sendTemporyParameter("sens", 1,id)

    def evenementObjet(self) -> None:
        """Vérifie les collisions avec la ligne d'arrivée (peut être transformé pour accueuillir d'autres objets spéciaux)
        """

        # Robin

        if "ligneArrivee" in self.MENU.listObjectInstancies:
            for ligneArrivee in self.MENU.listObjectInstancies["ligneArrivee"].values():
                if ligneArrivee.verification(self.palourdeEvenement,self.PALOURDE.xCamera,self.PALOURDE.yCamera) == True:
                    print("Finit")
                    self.retourMenu()

                    self.frameFin = 200

    def playerLeave(self, idPalourde : int) -> None:
        """Enlève une palourde

        Args:
            idPalourde (int): l'id de la palourde qu'il faut enlever
        """

        # Nathan

        if idPalourde in self.ALL_PALOURDES:
            self.ALL_PALOURDES.pop(idPalourde)


    # --------------- Methodes Menu ----------------
    def retourMenu(self):
        """Revient au menu title
        """

        # Par Lucie

        if self.NETWORK_OBJECT != None:
            self.NETWORK_OBJECT.close()
            self.NETWORK_OBJECT = None
        self.ALL_PALOURDES = {}
        self.PALOURDE.changementModeNormal()
        self.MENU.switchMenu("title")

    
    # ------------ Methodes Utilitaires ------------
    def tranformCoo(self, xUser : str | int |float , yUser: str | int |float ) -> int | float:
        """Transforme les racourcis x et y en nombre.

        Args:
            xUser (str | int | float): coordonnée x a transformée
            yUser (str | int | float): coordonnée y a transformée

        Returns:
            int | float: retourne les coordonnées transformées
        """

        # Par Nathan

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


if __name__ == "__main__":
    game = Game()
    game.run()