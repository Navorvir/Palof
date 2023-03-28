import sys
import pygame
from Package.Game.Palourde.palourde import Palourde
from Package.Game.Palourde.camera2 import CameraGroup
import time
from Package.bouton import bouton

class Menu():
    def __init__(self, largeur_ecran, hauteur_ecran, screen, palourde, CAMERA ):
        self.NONE = 0
        self.MODE_COURSE = 1
        self.MODE_COOP = 2
        self.MODE_VERSUS = 3
        self.TITRE = 1
        self.CHOIX_MENU = 2
        self.CAMERA = CAMERA
        
        self.PALOURDE = palourde
        
        self.etape_menu = self.TITRE
        
        self.image_mode_course_bouton = pygame.image.load("Assets/Button/Bouton_mode_course.png")
        self.image_mode_coop_bouton = pygame.image.load("Assets/Button/Bouton_mode_coop.png")
        self.image_mode_versus_bouton = pygame.image.load("Assets/Button/Bouton_mode_versus.png")
        
        self.mode_course_bouton = bouton(largeur_ecran-pygame.Surface.get_width(self.image_mode_course_bouton), hauteur_ecran/3, screen, self.image_mode_course_bouton)
        self.mode_coop_bouton = bouton(0,hauteur_ecran/3, screen, self.image_mode_coop_bouton)
        self.mode_versus_bouton = bouton(largeur_ecran/2, 0, screen, self.image_mode_versus_bouton)
        
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.screen = screen
        self.background = (120,120,120)
    
        self.map = "Package/Game/json/test.json"
        
        
    def titre(self):
        r=0
        g=0
        b=0
        if self.PALOURDE.palourdeRect.clipline(self.largeur_ecran,0,self.largeur_ecran,self.hauteur_ecran):
            self.PALOURDE.x = 5
            self.etape_menu = self.CHOIX_MENU
    
    def choix_menu(self):
        if self.PALOURDE.palourdeRect.clipline(0,0,0,self.hauteur_ecran):
            self.PALOURDE.x = self.largeur_ecran - self.PALOURDE.LARGEUR
            self.etape_menu = self.TITRE
        self.mode_course_bouton.draw()
        self.mode_coop_bouton.draw()
        self.mode_versus_bouton.draw()
        
        if self.mode_course_bouton.pressed():
            self.mode = self.MODE_COURSE
            self.etape_menu = self.NONE

        if self.mode_versus_bouton.pressed():
            self.mode = self.MODE_VERSUS
            self.etape_menu = self.NONE

        
        if self.etape_menu == self.NONE :
            if self.CAMERA.move == False:
                    self.CAMERA.toggleCameraMove()
                    self.PALOURDE.x = 0
                    self.PALOURDE.y = 0
                
    def update(self):
        if self.etape_menu == self.TITRE:
            self.titre()
        elif self.etape_menu == self.CHOIX_MENU:
            self.choix_menu()
        