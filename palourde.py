import pygame
from os import path

class palourde:


    def __init__(self,surface,x,y):
        self.surface = surface
        self.x = x
        self.y = y

        self.HAUTEUR = 276/5
        self.LARGEUR = 616/5

        self.PALOURDE_IMAGE = pygame.image.load(path.join("palourde.png"))

        # 682 et 366 sont les dimensions de l'image de la palourde
        self.PALOURDE_SPRITE = pygame.transform.scale(self.PALOURDE_IMAGE, (self.LARGEUR, self.HAUTEUR))
        self.palourde_rect = pygame.Rect(self.x,self.y,self.LARGEUR,self.HAUTEUR)

        self.surface.blit(self.PALOURDE_SPRITE, (self.x, self.y))

        self.g = 9.81
        self.time_chute = 0
        self.m = 1

        self.vitesse_chute= 1
        self.jump_force = 250

        self.vitesse_avancement = 0
        self.speed = 0.1

        self.collison = False
        self.is_falling = True
        self.on_ground = False

    def remonter(self):
        #pour les tests
        self.x += self.LARGEUR
        self.y =0

    def tomber(self):
        self.time_chute+=1/60*self.m
        "Les moins sont là pour la formule"
        self.vitesse_chute = self.vitesse_chute- -self.g*self.time_chute

    def saut(self):
        self.on_ground = False
        self.vitesse_chute -= self.jump_force

    def mouvement_verticale(self):
        self.y += self.vitesse_chute/60


    def marche(self,sens):
        if self.speed < 5:
            self.speed += 0.1


        self.vitesse_avancement = self.speed *sens

        self.x += self.vitesse_avancement

    def placement(self):
        self.palourde_rect = pygame.Rect(self.x,self.y,self.LARGEUR,self.HAUTEUR)
        self.surface.blit(self.PALOURDE_SPRITE, (self.x, self.y))

    def collision(self,objet):
        """
        :param objet: normalement un Rect, c'est avec lui que l'on test la collision
        :return: True si il y à une collision
        """
        if self.palourde_rect.colliderect(objet) == True:
            self.y = objet.y - (objet.height + (self.HAUTEUR - objet.height)) + 2
            self.vitesse_chute = 0
            self.time_chute = 0

            if objet.collidepoint(self.palourde_rect.bottomleft) or objet.collidepoint(self.palourde_rect.bottomright) or objet.collidepoint(self.palourde_rect.midbottom):
                self.on_ground = True
            else:
                self.on_ground = False

            return True
        self.on_ground = False
        return False

    def frame_palourde(self,liste_objet_collision):
        """

        :param liste_objet_collision: liste d'objet auquel la palourde peut avoir des collisions
        :return:
        """


        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.marche(1)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.marche(-1)
        else:
            self.speed = 0.1


        for objet in liste_objet_collision:
            self.collison = self.collision(objet)
            if self.collison == True:
                if self.on_ground == True:
                    self.is_falling = False
                break

        if self.on_ground == False:
            self.is_falling = True


        if self.is_falling == True:
            self.tomber()
        else:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.saut()

        self.mouvement_verticale()

        self.placement()