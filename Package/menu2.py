import sys
import pygame
from Package.Game.Palourde.palourde import Palourde
from Package.Game.Palourde.camera2 import CameraGroup
import time
from Package.bouton import Button

class Menu():
    def __init__(self, largeur_ecran, hauteur_ecran, screen, palourde, CAMERA ):
        self.NONE = 0
        self.MODE_COURSE = 1
        self.MODE_COOP = 2
        self.MODE_VERSUS = 3
        self.TITRE = 1
        self.CHOIX_MENU = 2
        self.CHOIX_NIVEAU = 3
        
        self.CAMERA = CAMERA
        
        self.PALOURDE = palourde
        
        self.etape_menu = self.TITRE
        
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.screen = screen
        self.background = (120,120,120)
        self.changeScene = True
        
        self.map_choice_mode = "Package/Game/json/menu_choice_mode.json"
        self.map_title = "Package/Game/json/menu_title.json"
        self.map_level_choice = "Package/Game/json/menu_choice_niveau.json"
        
        self.map = self.map_title
        
        self.listObjectInstancies = {}
        
    def titre(self):
        if self.map != self.map_title:
            self.map = self.map_title
            self.changeScene = True

        r=0
        g=0
        b=0
        if self.PALOURDE.palourdeRect.clipline(self.largeur_ecran,0,self.largeur_ecran,self.hauteur_ecran):
            self.PALOURDE.x = 5
            self.etape_menu = self.CHOIX_MENU
            self.map = self.map_choice_mode
            self.changeScene = True
            
    
    def choix_menu(self):
        if self.PALOURDE.palourdeRect.clipline(0,0,0,self.hauteur_ecran):
            self.PALOURDE.x = self.largeur_ecran - self.PALOURDE.LARGEUR
            self.etape_menu = self.TITRE
            
            
        for button in self.listObjectInstancies["button"]:
            if button.pressed():
                #if button.name == "mode_course":
                #   self.mode = self.MODE_COURSE
                #   self.etape_menu = self.NONE

                #elif button.name == "mode_versus":
                #   self.mode = self.MODE_VERSUS
                #   self.etape_menu = self.NONE
                    
                    
                if button.name == "mode_coop":
                    self.mode = self.MODE_COOP
                    self.etape_menu = self.CHOIX_NIVEAU
                    self.map = self.map_level_choice
                    self.changeScene = True

        
        if self.etape_menu == self.NONE :
            if self.CAMERA.move == False:
                    self.CAMERA.toggleCameraMove()
                    self.PALOURDE.x = 0
                    self.PALOURDE.y = 0
                    
    def choix_niveau(self):
        if self.etape_menu == self.CHOIX_NIVEAU:
            for levelButton in self.listObjectInstancies["button"]:
                if levelButton.pressed():
                    if levelButton.name == "level1":
                        self.map = "Package/Game/json/level1.json"
                    if levelButton.name == "level2":
                        pass
                        
                        
                        self.changeScene = True
                        self.PALOURDE.x = 0
                        self.PALOURDE.y = 0
                        self.etape_menu = self.NONE
            
            
    #def get_mode(self):
    #    return self.mode
                
    def update(self, scene):
        if self.etape_menu == self.TITRE:
            self.titre()
        elif self.etape_menu == self.CHOIX_MENU:            
            self.choix_menu()
        elif self.etape_menu == self.CHOIX_NIVEAU:
            self.choix_niveau()
        
