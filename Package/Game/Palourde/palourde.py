import random

import pygame
import math
from os import path

class Palourde:


    def __init__(self,surface,x,y):
        self.surface = surface
        self.x = 500
        self.y = 500

        self.xCamera = x
        self.yCamera = y

        # 616 et 276 sont les dimensions de l'image de la palourde
        self.HAUTEUR = 185//4
        self.LARGEUR = 354//4

        self.centrePalourde = (self.x+self.LARGEUR/2,self.y+self.HAUTEUR/2)

        self.PALOURDE_IMAGE = pygame.image.load(path.join("Assets/Entity/Player/palourde2.png"))
        self.PALOURDE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_IMAGE, (self.LARGEUR, self.HAUTEUR))

        self.PALOURDE_BRAS_GAUCHE_IMAGE = pygame.image.load(path.join("Assets/Entity/Player/bras_gauche.png"))
        self.PALOURDE_BRAS_DROIT_IMAGE = pygame.image.load(path.join("Assets/Entity/Player/bras_droit.png"))

        self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_GAUCHE_IMAGE, (121//4, 199//4))
        self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_DROIT_IMAGE, (149//4, 199//4))



        self.palourdeSprite = self.PALOURDE_IMAGE_RESIZED

        self.brasGaucheSprite = self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED
        self.brasDroitSprite = self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED

        #permet de former un tuple qui possède les coordonnés de la palourde et de sa taille lors des rotation
        self.rectRotation =  self.palourdeSprite.get_rect(center = self.PALOURDE_IMAGE_RESIZED.get_rect(topleft = (self.x,self.y)).center)

        self.palourdeRect = pygame.Rect(self.rectRotation[0],self.rectRotation[1],self.LARGEUR,self.HAUTEUR)

        #Initialisation des rect des bras
        #self.brasGaucheRectRotation
        #self.brasDroitRectRotation

        self.surface.blit(self.palourdeSprite, (self.x, self.y))

        self.g = 9.81
        self.timeChute = 0

        self.vitesseChute= 1
        self.jumpForce = 250

        self.vitesseAvancement = 0
        self.speed = 0.1

        self.collison = False
        self.isFalling = True
        self.onGround = False

        self.angle = 0
        self.pointRotation1 = self.g
        self.pointRotation2 = self.g
        self.retenuPoint1 = 0
        self.retenuPoint2 = 0

        self.angleBras = [self.angle,self.angle]
        self.coefAngleBras = [1,1]
        self.ancienSens = 0

        self.roule = False
        self.ySol = self.y

        self.creationPoint()





    def calcPositionPoint(self,angle,cos,sin):
        return (self.centrePalourde[0] + math.cos((self.angle+angle)*math.pi/180)*cos, self.centrePalourde[1] + -math.sin((self.angle+angle)*math.pi/180)*sin)

    def calcPositionPoints(self,angle,cos,sin):
        return pygame.Rect(self.centrePalourde[0] + math.cos((self.angle+angle)*math.pi/180)*cos, self.centrePalourde[1] + -math.sin((self.angle+angle)*math.pi/180)*sin, 2, 2)


    def creationPoint(self):

        self.centrePalourde = (self.x + self.LARGEUR/2,self.y + self.HAUTEUR/2)

        self.listePoint = [
            self.calcPositionPoint(90,24,24),
            self.calcPositionPoint(55,27,27),
            self.calcPositionPoint(30,35,35),
            self.calcPositionPoint(12, 40, 40),
            self.calcPositionPoint(-5, 42, 42),
            self.calcPositionPoint(-23, 40, 40),
            self.calcPositionPoint(-42, 33, 33),
            self.calcPositionPoint(-90, 24, 24),
            self.calcPositionPoint(-132, 32, 32),
            self.calcPositionPoint(-157, 40, 40),
            self.calcPositionPoint(-168, 42, 42),
            self.calcPositionPoint(-180, 40, 40),
            self.calcPositionPoint(168, 37, 37),
            self.calcPositionPoint(150, 33, 33),
            self.calcPositionPoint(125, 27, 27),
        ]

        self.xPointRotation1 = self.calcPositionPoint(180,24,24)
        self.xPointRotation2 = self.calcPositionPoint(0, 24, 24)

        self.listeRecte = [
            self.calcPositionPoints(90,24,24),
            self.calcPositionPoints(55,27,27),
            self.calcPositionPoints(30,35,35),
            self.calcPositionPoints(12, 40, 40),
            self.calcPositionPoints(-5, 42, 42),
            self.calcPositionPoints(-23, 40, 40),
            self.calcPositionPoints(-42, 33, 33),
            self.calcPositionPoints(-90, 24, 24),
            self.calcPositionPoints(-132, 32, 32),
            self.calcPositionPoints(-157, 40, 40),
            self.calcPositionPoints(-168, 42, 42),
            self.calcPositionPoints(-180, 40, 40),
            self.calcPositionPoints(168, 37, 37),
            self.calcPositionPoints(150, 33, 33),
            self.calcPositionPoints(125, 27, 27),
        ]

        self.listePointMain = [
            self.calcPositionPoint(0, 42, 42),
            self.calcPositionPoint(180, 42, 42)
        ]

        self.rectPointRotation1 = self.calcPositionPoints(180,24,24)
        self.rectPointRotation2 = self.calcPositionPoints(0, 24, 24)

    def rotation(self,degree):
        self.angle += degree
        self.angle %= 360

        for i in range(2):
            self.angleBras[i] += degree*self.coefAngleBras[i]
            self.angleBras[i] %= 360

        self.palourdeSprite = pygame.transform.rotate(self.PALOURDE_IMAGE_RESIZED, self.angle)

        self.brasGaucheSprite = pygame.transform.rotate(self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED, self.angleBras[0])
        self.brasDroitSprite = pygame.transform.rotate(self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED, self.angleBras[1])

        # permet de former un tuple qui possède les coordonnés de la palourde et de sa taille lors des rotation
        self.rectRotation =  self.palourdeSprite.get_rect(center = self.PALOURDE_IMAGE_RESIZED.get_rect(topleft = (self.x,self.y)).center)



    def roulement(self,sens):

        self.roule = True
        self.peutRouler = False

        if sens == 1:
            if self.vitesseAvancement > -10:
                self.peutRouler = True
        else:
            if self.vitesseAvancement < 10:
                self.peutRouler = True

        if self.ancienSens != sens :
            for i in range(2):
                self.coefAngleBras[i] = random.randint(-150,150)
                self.coefAngleBras[i] /= 100

        self.ancienSens = sens

        if self.onGround == True and self.peutRouler:

            if sens == 1:
                self.vitesseAvancement += (math.cos((self.angle + 90)%180 *math.pi/180) /10 + 0.09)*-1
            else:
                self.vitesseAvancement += (math.cos((180-(self.angle + 90)%180) *math.pi/180) /10 + 0.09)

            self.forceRotationBase( -sens + self.vitesseAvancement)

        elif self.onGround == True:
            self.forceRotationBase( -sens + self.vitesseAvancement)

        else:
            self.forceRotationBase(3*-sens)




    def calcForceRotation(self,x,y,verticale):
        """
        Calcule les forces sur la gauche et la droite de la palourde ce qui permet de déterminer sa rotation

        :param x: l'emplacement en x de l'impact
        :param y: l'emplacement en y de l'impact
        :param verticale: booléen qui vaut True si c'est un impact verticale
        """
        if verticale == True :
            if self.vitesseChute == 0 and 4 < self.angle < 356 and not 176 < self.angle < 184 and self.roule == False:
                if self.speed < 1:
                    self.speed *= 1.02

                if x-self.centrePalourde[0] < 0:
                    self.multiplicateurRotation = abs(self.xPointRotation2[0] - self.centrePalourde[0]) / (self.LARGEUR / 2)
                else:
                    self.multiplicateurRotation = abs(self.xPointRotation1[0] - self.centrePalourde[0]) / (self.LARGEUR / 2)



                if 90 < self.angle < 270:
                    if x > self.centrePalourde[0]:

                        self.pointRotation1 += self.g * self.multiplicateurRotation
                    else:
                        self.pointRotation2 += self.g * self.multiplicateurRotation
                else:
                    if x > self.centrePalourde[0]:
                        self.pointRotation2 -= self.g * self.multiplicateurRotation
                    else:
                        self.pointRotation1 -= self.g * self.multiplicateurRotation


            elif self.onGround == False:
                self.speed = 0.1
                if 90 < self.angle < 270:
                    if x > self.centrePalourde[0]:
                        self.pointRotation2 += math.sqrt(abs(math.sqrt(((x-self.centrePalourde[0])**2 + (y-self.centrePalourde[1])**2))/25 * self.vitesseChute/100 * math.sqrt(abs((x-self.centrePalourde[1])))))
                    else:
                        self.pointRotation1 += math.sqrt(abs(math.sqrt(((x-self.centrePalourde[0])**2 + (y-self.centrePalourde[1])**2))/25 * self.vitesseChute/100 * math.sqrt(abs((x-self.centrePalourde[1])))))
                else:
                    if x > self.centrePalourde[0]:
                        self.pointRotation1 -= math.sqrt(abs(math.sqrt(((x-self.centrePalourde[0])**2 + (y-self.centrePalourde[1])**2))/25 * self.vitesseChute/100 * math.sqrt(abs((x-self.centrePalourde[1])))))
                    else:
                        self.pointRotation2 -= math.sqrt(abs(math.sqrt(((x-self.centrePalourde[0])**2 + (y-self.centrePalourde[1])**2))/25 * self.vitesseChute/100 * math.sqrt(abs((x-self.centrePalourde[1])))))
        else:
            if 90 < self.angle < 270:
                if x < self.centrePalourde[0]:
                    if y < self.centrePalourde[1]:
                        self.pointRotation2 += math.sqrt(abs(math.sqrt(((x-self.centrePalourde[0])**2 + (y-self.centrePalourde[1])**2))/25 * self.vitesseAvancement * math.sqrt(abs((y-self.centrePalourde[1])))))
                    else:
                        self.pointRotation2 -= math.sqrt(abs(math.sqrt(((x - self.centrePalourde[0]) ** 2 + (y - self.centrePalourde[1]) ** 2)) / 25 * self.vitesseAvancement * math.sqrt(abs((y - self.centrePalourde[1])))))

                else:
                    if y < self.centrePalourde[1]:
                        self.pointRotation1 += math.sqrt(abs(math.sqrt(((x - self.centrePalourde[0]) ** 2 + (
                                    y - self.centrePalourde[1]) ** 2)) / 25 * self.vitesseAvancement * math.sqrt(
                            abs((y - self.centrePalourde[1])))))
                    else:
                        self.pointRotation1 -= math.sqrt(abs(math.sqrt(((x - self.centrePalourde[0]) ** 2 + (
                                    y - self.centrePalourde[1]) ** 2)) / 25 * self.vitesseAvancement * math.sqrt(
                            abs((y - self.centrePalourde[1])))))
            else:
                if x < self.centrePalourde[0]:
                    if y < self.centrePalourde[1]:
                        self.pointRotation1 -= math.sqrt(abs(math.sqrt(((x - self.centrePalourde[0]) ** 2 + (
                                    y - self.centrePalourde[1]) ** 2)) / 25 * self.vitesseAvancement * math.sqrt(
                            abs((y - self.centrePalourde[1])))))
                    else:
                        self.pointRotation1 += math.sqrt(abs(math.sqrt(((x - self.centrePalourde[0]) ** 2 + (
                                    y - self.centrePalourde[1]) ** 2)) / 25 * self.vitesseAvancement * math.sqrt(
                            abs((y - self.centrePalourde[1])))))
                else:
                    if y < self.centrePalourde[1]:
                        self.pointRotation2 -= math.sqrt(abs(math.sqrt(((x - self.centrePalourde[0]) ** 2 + (
                                    y - self.centrePalourde[1]) ** 2)) / 25 * self.vitesseAvancement * math.sqrt(
                            abs((y - self.centrePalourde[1])))))
                    else:
                        self.pointRotation2 += math.sqrt(abs(math.sqrt(((x - self.centrePalourde[0]) ** 2 + (
                                    y - self.centrePalourde[1]) ** 2)) / 25 * self.vitesseAvancement * math.sqrt(
                            abs((y - self.centrePalourde[1])))))


    def rotationAvecForce(self):
        self.rotation((self.pointRotation1-self.pointRotation2)/10)
        self.creationPoint()

        if self.sol == True:
            self.yMax = self.listePoint[0][1]

            for y in self.listePoint:
                if y[1] > self.yMax:
                    self.yMax = y[1]

            self.yCamera = self.ySol + (self.yCamera - self.yMax)

            if self.roule == False and abs(self.pointRotation1-self.pointRotation2) > 0.1:
                if self.pointRotation1-self.pointRotation2 > 0:
                    self.vitesseAvancement += -0.2 * abs(self.angle%180 - 90) / 90
                else:
                    self.vitesseAvancement += 0.2* abs(self.angle%180 - 90) / 90

    def forceRotationMoyenne(self):
        self.pointRotation1 = (self.pointRotation1 + self.g)/2
        self.pointRotation2 = (self.pointRotation2 + self.g)/2

    def forceRotationBase(self,multiplicateur):

        self.pointRotation1 = self.g
        self.pointRotation2 = self.g

        if multiplicateur > 0:
            self.pointRotation2 = self.g * multiplicateur
        else:
            self.pointRotation1 = -self.g * multiplicateur



    def tomber(self):
        self.timeChute+=1/60

        self.vitesseChute += self.g*self.timeChute

    def saut(self):
        self.forceRotationMoyenne()
        self.onGround = False
        self.vitesseChute -= self.jumpForce

    def mouvementVerticale(self):
        self.yCamera += self.vitesseChute/60

    def mouvementHorizontal(self):

        self.xCamera += self.vitesseAvancement


    def marche(self,sens):
        if self.speed < 5:
            self.speed += 0.1

        self.vitesseAvancement = self.speed *sens

    def placementBras(self):
        self.brasGaucheRectRotation = self.brasGaucheSprite.get_rect(center = self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED.get_rect(bottomright = self.listePointMain[1]).center)
        self.brasDroitRectRotation = self.brasDroitSprite.get_rect(center=self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED.get_rect(bottomleft=self.listePointMain[0]).center)

        self.cooBrasGauche = (self.brasGaucheRectRotation.centerx + math.cos((self.angleBras[0]+300) * math.pi / 180) * 28,
                                self.brasGaucheRectRotation.centery + -math.sin((self.angleBras[0]+300) * math.pi / 180) * 28)
        self.cooBrasDroit = (self.brasDroitRectRotation.centerx + math.cos((self.angleBras[1] + 234) * math.pi / 180) * 28,
                              self.brasDroitRectRotation.centery + -math.sin((self.angleBras[1] + 234) * math.pi / 180) * 28)


        self.brasGaucheRectRotation = self.brasGaucheSprite.get_rect(
            center=self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED.get_rect(bottomright= (self.listePointMain[1][0] + (self.listePointMain[1][0] - self.cooBrasGauche[0]),self.listePointMain[1][1] + (self.listePointMain[1][1] - self.cooBrasGauche[1]))).center)
        self.brasDroitRectRotation = self.brasDroitSprite.get_rect(
            center=self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED.get_rect(bottomleft= (self.listePointMain[0][0] + (self.listePointMain[0][0] - self.cooBrasDroit[0]),self.listePointMain[0][1] + (self.listePointMain[0][1] - self.cooBrasDroit[1]))).center)



    def placement(self):
        self.centrePalourde = (self.x + self.LARGEUR/2,self.y + self.HAUTEUR/2)

        self.rectRotation = self.palourdeSprite.get_rect(
            center=self.PALOURDE_IMAGE_RESIZED.get_rect(topleft=(self.x, self.y)).center)
        self.palourdeRect = pygame.Rect(self.rectRotation[0],self.rectRotation[1] ,self.LARGEUR,self.HAUTEUR)

        self.placementBras()

        #self.surface.blit(self.palourde_sprite, (self.x, self.y))
        self.surface.blit(self.palourdeSprite, self.rectRotation)

        self.surface.blit(self.brasGaucheSprite, self.brasGaucheRectRotation)
        self.surface.blit(self.brasDroitSprite, self.brasDroitRectRotation)

        for i in range (len(self.listeRecte)):
            pygame.draw.rect(self.surface, (100+i*5,255-10*i,255 - i*5), self.listeRecte[i])




        pygame.draw.rect(self.surface, (100,200,150), self.rectPointRotation1)
        pygame.draw.rect(self.surface, (200,150,100), self.rectPointRotation2)

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
            self.indiceYMax = 0


            for i in range(len(self.pointTouche)):
                if self.pointTouche[i][0] > self.pointXMax:
                    self.pointXMax = self.pointTouche[i][0]
                    self.indiceXMax = i
                if self.pointTouche[i][1] > self.pointYMax:
                    self.pointYMax = self.pointTouche[i][1]
                    self.indiceYMax = i
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
                self.calcForceRotation(self.pointTouche[self.indiceYMax][0],self.pointTouche[self.indiceYMax][1],True)

                self.ySol = objet.y

                self.y = self.ySol + (self.y-self.pointYMax)

                self.timeChute = 0
                self.vitesseChute = 0

                if abs(self.vitesseAvancement) >0.1 and self.roule == False:
                    self.vitesseAvancement /= 1.1
                elif self.roule == False:
                    self.vitesseAvancement = 0
                self.sol = True
                self.creationPoint()

                return True

            elif self.plafond == False and self.sol == False  and objet.collidepoint(self.pointTouche[self.indiceYMin]) and self.pointYMin < self.pointPlafond :
                self.calcForceRotation(self.pointTouche[self.indiceYMin][0], self.pointTouche[self.indiceYMin][1], True)
                self.y = objet.y+objet.height + (self.y-self.pointYMin)
                self.vitesseChute = 5
                self.plafond = True
                self.creationPoint()


            elif self.plafond == False and self.sol == True  and objet.collidepoint(self.pointTouche[self.indiceYMin]) and self.pointYMin < self.pointPlafond :
                self.calcForceRotation(self.pointTouche[self.indiceYMin][0], self.pointTouche[self.indiceYMin][1], True)
                self.vitesseChute = 5
                self.plafond = True
                self.creationPoint()

            elif self.murGauche == False and self.plafond == False and objet.collidepoint(self.pointTouche[self.indiceXMin]) and self.pointXMin < self.centrePalourde[0]:
                self.calcForceRotation(self.pointTouche[self.indiceXMin][0], self.pointTouche[self.indiceXMin][1], False)
                self.x =objet.x + objet.width + (self.x-self.pointXMin)
                self.murGauche = True
                self.creationPoint()

                self.vitesseAvancement = math.sqrt(abs(self.vitesseAvancement)) / 3
                return True

            elif self.murDroit == False and self.plafond == False and objet.collidepoint(self.pointTouche[self.indiceXMax]) and self.pointXMax > self.centrePalourde[0] :
                self.calcForceRotation(self.pointTouche[self.indiceXMax][0], self.pointTouche[self.indiceXMax][1], False)
                self.x = objet.x + (self.x-self.pointXMax)
                self.murDroit = True
                self.creationPoint()

                self.vitesseAvancement = -1 * math.sqrt(abs(self.vitesseAvancement)) / 3
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



        if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.roulement(-1)
        elif pygame.key.get_pressed()[pygame.K_q] or pygame.key.get_pressed()[pygame.K_LEFT]:
            self.roulement(1)
        else:
            self.roule = False



        self.mouvementHorizontal()


        if self.onGround == False:
            self.isFalling = True
        else:
            self.isFalling = False


        if self.isFalling == True:
            self.tomber()
        elif self.timeChute <= 6/30:
            if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_UP]:
                self.saut()

        self.mouvementVerticale()

        #Aide pour le fonctionnement des collisions
        self.creationPoint()
        self.pointSol = self.calcPointSol()
        self.pointPlafond = self.calcPointPlafond()
        self.onGround = False
        self.sol = False
        self.murGauche = False
        self.murDroit = False
        self.plafond = False

        if self.isFalling == False:
            self.forceRotationMoyenne()

        #Teste les collisions avec tous objet de la liste listeObjetCollision
        for objet in listeObjetCollision:
            self.collison = self.collision(objet)

        self.xCamera += self.x - 500
        self.yCamera += (self.y - 500)

        self.x = 500
        if self.yCamera > 1000 :
            self.y = 500 + self.yCamera - 1000
            self.yCamera = 1000
        elif self.onGround == True :
            self.yCamera -= (self.y - 500)
        else:
            self.y = 500

        self.rotationAvecForce()

        self.placement()
