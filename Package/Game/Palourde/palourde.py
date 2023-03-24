import pygame
import math
from os import path

class Palourde:

    def __init__(self,surface,x,y):
        self.surface = surface
        self.x = x
        self.y = y

        # 616 et 276 sont les dimensions de l'image de la palourde
        self.HAUTEUR = 198//4
        self.LARGEUR = 344//4

        self.centrePalourde = (self.x+self.LARGEUR/2,self.y+self.HAUTEUR/2)

        self.PALOURDE_IMAGE = pygame.image.load(path.join("Assets/Entity/Player/palourde.png"))
        self.PALOURDE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_IMAGE, (self.LARGEUR, self.HAUTEUR))


        self.palourdeSprite = self.PALOURDE_IMAGE_RESIZED

        #permet de former un tuple qui possède les coordonnés de la palourde et de sa taille lors des rotation
        self.rectRotation =  self.palourdeSprite.get_rect(center = self.PALOURDE_IMAGE_RESIZED.get_rect(topleft = (self.x,self.y)).center)

        self.palourdeRect = pygame.Rect(self.rectRotation[0],self.rectRotation[1],self.LARGEUR,self.HAUTEUR)

        self.surface.blit(self.palourdeSprite, (self.x, self.y))

        self.g = 9.81
        self.timeChute = 0
        self.m = 1

        self.vitesseChute= 1
        self.jumpForce = 250

        self.vitesseAvancement = 0
        self.speed = 0.1

        self.collison = False
        self.isFalling = True
        self.onGround = False

        self.angle = 0

        self.creationPoint()



    def calcPositionPoint(self,angle,cos,sin):
        return (self.centrePalourde[0] + math.cos((self.angle+angle)*math.pi/180)*cos, self.centrePalourde[1] + -math.sin((self.angle+angle)*math.pi/180)*sin)


    def creationPoint(self):

        
        self.listePoint = []
        points = [ 
            (90,24,24), (55,27,27), (30,35,35), (12, 40, 40), (-5, 42, 42), (-23, 40, 40), 
            (-42, 33, 33), (-90, 24, 24), (-132, 32, 32), (-157, 40, 40), (-175, 42, 42), 
            (168, 37, 37), (150, 33, 33), (125, 27, 27),
        ]

        for point in points:
            self.listePoint.append(self.calcPositionPoint(*point))
        


    def rotation(self,degree):
        self.angle += degree
        self.angle %= 360

        self.palourdeSprite = pygame.transform.rotate(self.PALOURDE_IMAGE_RESIZED, self.angle)

        # permet de former un tuple qui possède les coordonnés de la palourde et de sa taille lors des rotation
        self.rectRotation =  self.palourdeSprite.get_rect(center = self.PALOURDE_IMAGE_RESIZED.get_rect(topleft = (self.x,self.y)).center)

    def remonter(self):
        #pour les tests
        self.x += self.LARGEUR
        self.y =0

    def tomber(self):
        self.timeChute+=1/60*self.m

        self.vitesseChute = self.vitesseChute + self.g*self.timeChute

    def saut(self):
        self.onGround = False
        self.vitesseChute -= self.jumpForce

    def mouvementVerticale(self):
        self.y += self.vitesseChute/60


    def marche(self,sens):
        if self.speed < 5:
            self.speed += 0.1


        self.vitesseAvancement = self.speed *sens

        self.x += self.vitesseAvancement

    def placement(self):
        self.centrePalourde = (self.x + self.LARGEUR/2,self.y + self.HAUTEUR/2)

        self.rectRotation = self.palourdeSprite.get_rect(
            center=self.PALOURDE_IMAGE_RESIZED.get_rect(topleft=(self.x, self.y)).center)
        self.palourdeRect = pygame.Rect(self.rectRotation[0],self.rectRotation[1] ,self.LARGEUR,self.HAUTEUR)

        #self.surface.blit(self.palourde_sprite, (self.x, self.y))
        self.surface.blit(self.palourdeSprite, self.rectRotation)

        self.creationPoint()


    def calcPointSol(self):
        self.pointPlusBas = []
        for point in self.listePoint:
            self.pointPlusBas.append(point[1])
        self.pointPlusBas.sort()

        if 45<self.angle<135 or 225<self.angle<315:
            return self.pointPlusBas[-2]
        else:
            return self.pointPlusBas[-3]

    def calcPointPlafond(self):
        self.pointPlusHaut = []
        for point in self.listePoint:
            self.pointPlusHaut.append(point[1])
        self.pointPlusHaut.sort()

        if 45<self.angle<135 or 225<self.angle<315:
            return self.pointPlusHaut[1]
        else:
            return self.pointPlusHaut[2]




    def collision(self,objet):
        """
        :param objet: normalement un Rect, c'est avec lui que l'on test la collision
        :return: True si il y à une collision
        """
        pass
        self.pointTouche = []

        for point in self.listePoint:
            if objet.collidepoint(point):
                self.pointTouche.append(point)

        if len(self.pointTouche) >0:
            self.pointXMax = self.pointTouche[0][0]
            self.pointYMax = self.pointTouche[0][1]
            self.pointXMin = self.pointTouche[0][0]
            self.pointYMin = self.pointTouche[0][1]

            self.indiceXMax = 0
            self.indiceXMin = 0
            self.indiceYMin = 0


            for i in range(len(self.pointTouche)):
                if self.pointTouche[i][0] > self.pointXMax:
                    self.pointXMax = self.pointTouche[i][0]
                    self.indiceXMax = i
                if self.pointTouche[i][1] > self.pointYMax:
                    self.pointYMax = self.pointTouche[i][1]
                if self.pointTouche[i][0] < self.pointXMin:
                    self.pointXMin = self.pointTouche[i][0]
                    self.indiceXMin = i
                if self.pointTouche[i][1] < self.pointYMin:
                    self.pointYMin = self.pointTouche[i][1]
                    self.indiceYMin = i

            if self.onGround == False:
                if self.pointYMax >= self.pointSol:
                    self.onGround = True
                else:
                    self.onGround = False

            #Si onGround vaut True, alors la collision est causée par une chute
            #Si il vaut False, la collision est causée par un mouvement horizontal

            if self.sol == False and self.onGround == True:
                self.y = objet.y + (self.y-self.pointYMax)

                self.timeChute = 0
                self.vitesseChute = 0
                self.sol = True

                return True

            elif self.plafond == False and self.sol == False  and objet.collidepoint(self.pointTouche[self.indiceYMin]) and self.pointYMin < self.pointPlafond :
                self.y = objet.y+objet.height + (self.y-self.pointYMin)
                self.vitesseChute = 5
                self.plafond = True

            elif self.murGauche == False and self.plafond == False and objet.collidepoint(self.pointTouche[self.indiceXMin]) and self.pointXMin < self.centrePalourde[0]:
                self.x =objet.x + objet.width + (self.x-self.pointXMin)
                self.murGauche = True
                return True

            elif self.murDroit == False and self.plafond == False and objet.collidepoint(self.pointTouche[self.indiceXMax]) and self.pointXMax > self.centrePalourde[0] :
                self.x = objet.x + (self.x-self.pointXMax)
                self.murDroit = True
                return True





            return True
        if self.onGround == False:
            self.onGround = False
        return False



    def framePalourde(self,listeObjetCollision):
        """

        :param liste_objet_collision: liste d'objet auquel la palourde peut avoir des collisions
        :return:
        """

        self.pointSol = self.calcPointSol()
        self.pointPlafond = self.calcPointPlafond()
        self.onGround = False
        self.sol = False
        self.murGauche = False
        self.murDroit = False
        self.plafond = False

        for objet in listeObjetCollision:
            self.collison = self.collision(objet)

        if self.onGround == False:
            self.isFalling = True
        else:
            self.isFalling = False


        if self.isFalling == True:
            self.tomber()
        elif pygame.key.get_pressed()[pygame.K_SPACE]:
                self.saut()

        self.mouvementVerticale()

        self.placement()