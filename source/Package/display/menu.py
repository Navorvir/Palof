from os.path import exists
from Package.Game.palourde import Palourde
from Package.display.input import Input
from Package.display.text import Text
import pygame
import time

class Menu():
    def __init__(self, screen_width, screen_height, screen, palourde, CAMERA):

        # ==================== CONSTANTES ==================

        # self.NONE : int = 0
        self.MODE_COOP : int = 2
        self.MODE_VERSUS = 3


        self.PATH_COOP : str = "./Assets/levels/coop/"
        self.PATH_VERSUS : str = "./Assets/levels/versus/"
        self.PATH_MENU : str = "./Assets/menu/"

        self.SCREEN_HEIGHT : int = screen_width
        self.SCREEN_WIDTH : int = screen_height
        self.BACKGROUND : tuple(int, int, int) = (120,120,120)

        self.CAMERA = CAMERA        
        self.PALOURDE : Palourde = palourde
        self.SCREEN = screen

        self.INPUT_IMAGE = "Assets/Button/input_code.png"

        self.NAME_LEVELS = {
            "level1" : "level1.json",
            "level2" : "level2.json",
            "level3" : "level3.json",
            "level4" : "level4.json",
            "level5" : "level5.json",
        }

        self.NAME_MAP_VERUS = {
            "versus" : self.PATH_VERSUS + "versus.json"

        }

        self.NAME_MENU : dict = {
            "mode" :{"path": self.PATH_MENU + "menu_choice_mode.json", "methUpdt":self.choseMenu},
            "wait" : {"path" : self.PATH_MENU + "menu_wait.json", "methUpdt":self.waitNetwork},
            "title" : {"path": self.PATH_MENU + "menu_title.json", "methUpdt":self.title},
            "level" : {"path": self.PATH_MENU + "menu_choice_niveau.json"},
            "player" : {"path": self.PATH_MENU + "menu_choice_player.json", "methUpdt":self.chosePlayer},
            "waitStart" : {"path": self.PATH_MENU + "menu_run_game.json"},
        }

        self.MANAGEMENT_BUTTON : dict= {
            "goVersus" : self.goVersus,
            "switchMenu" : self.switchMenu,
            "goLevel" : self.goLevel,
            "solo" : self.startParty,
        }

        self.MANAGEMENT_INPUT = {
            "checkCode" : print
        }
   
        # ==================== VARIABLES ===================

        self.stepMenu : str = "title"
        self.switchSceneEnable : bool = True        
        self.map = self.NAME_MENU["title"]["path"]
        self.mapChose = None

        self.runServer = False
        self.sceneEnable = False

        self.listObjectInstancies : dict = {"button":{},"input":{},"text":{}}

        
    def startG(self):
        pass

    def title(self) -> None:
        # par Lucie
        """
        met à jour à l'écran titre
        """
        if self.map != self.NAME_MENU["title"]["path"]:
            self.switchMenu("title")
 
        if self.PALOURDE.palourdeRect.clipline(0,0,0,self.SCREEN_WIDTH):
            self.switchMenu("wait")
        
        elif self.PALOURDE.palourdeRect.clipline(self.SCREEN_HEIGHT,0,self.SCREEN_HEIGHT,self.SCREEN_WIDTH):
            
            self.switchMenu("mode")
            
        
    def checkButton(self):
        # par Nathan
        """
        Regarde si les boutons de la scène sont pressé et si oui execute leur commande
        """
        for key, objectButton in self.listObjectInstancies["button"].items():
            if objectButton.pressed():   
                if  objectButton.directCommand:
                    objectButton.command()
                elif objectButton.command in self.MANAGEMENT_BUTTON:
                    self.MANAGEMENT_BUTTON[objectButton.command](*objectButton.arguments)
                time.sleep(0.2)

    def checkInput(self, event) -> None:
        # par Nathan
        """
        Pour chaque input de la scène, regarde les entrés claviers pour les stockés en mémoire et l'affiché
        """
        if "input" in self.listObjectInstancies:
            for key, objectInput in self.listObjectInstancies["input"].items():

                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    objectInput.text = objectInput.getUnicode(objectInput.text)
                    if objectInput.command != None and type(objectInput.command) != str:
                        objectInput.command(objectInput.text)


                elif event.key == pygame.K_BACKSPACE:
                    objectInput.text = objectInput.text[:-1]
                else:
                    objectInput.text += event.unicode

                objectInput.update()

    def waiGameStarted(self):
        # par Nathan
        """
        lance un niveau en multijoueur
        """
        self.runServer = True


    def choseMenu(self) -> None:
        # par Lucie
        """
        met à jour le menu du choix du mode de jeu
        """
        # Changer de menu
        if self.PALOURDE.palourdeRect.clipline(0,0,0,self.SCREEN_WIDTH):
            self.PALOURDE.x = self.SCREEN_HEIGHT - self.PALOURDE.LARGEUR
            self.switchMenu("title")
         
        
        if self.stepMenu == None :
            self.lockCamera()
            if self.CAMERA.lock:
                    self.PALOURDE.x = 0
                    self.PALOURDE.y = 0

    def chosePlayer(self):
        # par Nathan
        """
        correspond au menu pour choisir si on est en solo ou mutijoueur
        """
        self.switchMenu("player")
    

    def startParty(self, *args):
        # par Nathan
        """
        lance la partie
        """
        self.map = self.mapChose
        self.switchMenu(None)

    def multiPlayer(self):
        # par Nathan
        """
        lance un niveau en multijoueur
        """
        self.runServer = True
        self.map = self.mapChose
        self.switchMenu(None)
        

    def goVersus(self, levelName :str = "versus", modeServer : bool = True, *args):
        """
        lance le mode versus
        """
        # par Nathan
        self.mode = self.MODE_VERSUS
        self.mapChose = self.NAME_MAP_VERUS["versus"] 

        self.PALOURDE.changementModeVersus()

        self.chosePlayer()

    def goLevel(self, levelName : str =None, modeServer : bool = False, allPath : str=None) -> None:
        """
        defini la map du jeu en fonction du niveau pris
        """
        # par Nathan
        self.mode = self.MODE_COOP
        self.PALOURDE.changementModeNormal()

        map = None

        if allPath == None and levelName != None:
            if levelName in self.NAME_LEVELS and exists(self.PATH_COOP + self.NAME_LEVELS[levelName]):
                map = self.PATH_COOP + self.NAME_LEVELS[levelName]
        elif exists(allPath):
            map = allPath

        if map != None:
            self.mapChose = map
            self.chosePlayer()


  
    def waitNetwork(self) -> None:
        """
        met à jour le menu pour se connecter en réseau
        """
        # par Nathan
        if self.PALOURDE.palourdeRect.clipline(self.SCREEN_HEIGHT,0,self.SCREEN_HEIGHT,self.SCREEN_WIDTH):
            self.PALOURDE.x = 0
            self.switchMenu("title")


    def switchMenu(self, name : str | None, *args) -> None:
        # par Nathan
        """
        Change de scène en prenant en paramètre le nom de la scène
        """
        if name != None:
            self.map = self.NAME_MENU[name]["path"]
            
        self.stepMenu = name
        self.switchSceneEnable = True
    

    def update(self) -> None:
        # par Nathan et Lucie
        """
        Met à jour le menu
        """
        if self.stepMenu in self.NAME_MENU and "methUpdt" in self.NAME_MENU[self.stepMenu]:
            self.NAME_MENU[self.stepMenu]["methUpdt"]()
        elif  self.stepMenu not in self.NAME_MENU and self.stepMenu != None:
            print("Le menu n'existe pas", self.stepMenu)
            self.stepMenu = "title"

        self.checkButton()

    # Méthodes Load
    def loadText(self):
        # par Nathan
        """
        Ajoute les objets texte à la caméra
        """
        if "text" in self.listObjectInstancies:
            for key, objectText in self.listObjectInstancies["text"].items():
                objectText.setText()
                self.appendListSprite(key, objectText)

    def loadButton(self):
        # par Nathan
        """
        Ajoute les boutons à la caméra
        """
        if "button" in self.listObjectInstancies:
            for key, objectButton in self.listObjectInstancies["button"].items():
                self.appendListSprite(key, objectButton)

    def loadInput(self):
        # par Nathan
        """
        Ajoute les inputs à la caméra
        """
        if "input" in self.listObjectInstancies:
            for key, objectInput in self.listObjectInstancies["input"].items():
                self.appendListSprite(key, objectInput)
               
        
    def lockCamera(self, x : int = 500, y : int = 250) -> None:
        # par Nathan et Robin
        """
        Bloque la caméra en fonction des des coordonnées x et y
        """
        self.PALOURDE.lockCamera(x,y)
        self.CAMERA.lockCamera()

    def unlockCamera(self, x : int = 0, y : int = 0) -> None:
        # par Nathan et Robin
        """
        Débloque la caméra en la réinitialisant aux coordonnée x et y
        """
        self.PALOURDE.lockCamera(x,y)
        self.CAMERA.unlockCamera()

    def appendListSprite(self,name, listSprite):
        # par Lucie et Nathan
        """
        Envoie listSprite à la caméra
        """
        self.CAMERA.listSpritesChange[name] = listSprite
        
