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

        self.PALOURDE_IMAGE = pygame.image.load(path.join("palourde.png"))
        self.PALOURDE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_IMAGE, (self.LARGEUR, self.HAUTEUR))


        self.palourdeSprite = self.PALOURDE_IMAGE_RESIZED

        #permet de former un tuple qui possède les coordonnés de la palourde et de sa taille lors des rotation
        self.rectRotation =  self.palourdeSprite.get_rect(center = self.PALOURDE_IMAGE_RESIZED.get_rect(topleft = (self.x,self.y)).center)

        self.palourdeRect = pygame.Rect(self.rectRotation[0],self.rectRotation[1],self.LARGEUR,self.HAUTEUR)

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
        self.pointRotation1 = 0
        self.pointRotation2 = 0

        self.creationPoint()





    def calcPositionPoint(self,angle,cos,sin):
        return (self.centrePalourde[0] + math.cos((self.angle+angle)*math.pi/180)*cos, self.centrePalourde[1] + -math.sin((self.angle+angle)*math.pi/180)*sin)


    def creationPoint(self):

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
            self.calcPositionPoint(-175, 42, 42),
            self.calcPositionPoint(168, 37, 37),
            self.calcPositionPoint(150, 33, 33),
            self.calcPositionPoint(125, 27, 27),
        ]


    def rotation(self,degree):
        self.angle += degree
        self.angle %= 360

        self.palourdeSprite = pygame.transform.rotate(self.PALOURDE_IMAGE_RESIZED, self.angle)

        # permet de former un tuple qui possède les coordonnés de la palourde et de sa taille lors des rotation
        self.rectRotation =  self.palourdeSprite.get_rect(center = self.PALOURDE_IMAGE_RESIZED.get_rect(topleft = (self.x,self.y)).center)


    def roulement(self,sens):

        self.rotation(1*sens)

        if self.onGround == True:
            self.vitesseAvancement = (math.cos(self.angle*math.pi/180*2) + 1.5) * -sens



    def calcForceRotation(self,x,y,verticale):
        """
        Calcule les forces sur la gauche et la droite de la palourde ce qui permet de déterminer sa rotation

        :param x: l'emplacement en x de l'impact
        :param y: l'emplacement en y de l'impact
        :param verticale: booléen qui vaut True si c'est un impact verticale
        """
        if verticale == True :

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


    def forceRotationBase(self):
        self.pointRotation1 = self.g
        self.pointRotation2 = self.g

    def remonter(self):
        #pour les tests
        self.x += self.LARGEUR
        self.y =0

    def tomber(self):
        self.timeChute+=1/60

        self.vitesseChute += self.g*self.timeChute

    def saut(self):
        self.onGround = False
        self.vitesseChute -= self.jumpForce

    def mouvementVerticale(self):
        self.y += self.vitesseChute/60

    def mouvementHorizontal(self):
        self.x += self.vitesseAvancement


    def marche(self,sens):
        if self.speed < 5:
            self.speed += 0.1

        self.vitesseAvancement = self.speed *sens

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

                self.y = objet.y + (self.y-self.pointYMax)

                self.timeChute = 0
                self.vitesseChute = 0
                if abs(self.vitesseAvancement) >0.1:

                    self.vitesseAvancement /= 1.1
                else:
                    self.vitesseAvancement = 0
                self.sol = True

                return True

            elif self.plafond == False and self.sol == False  and objet.collidepoint(self.pointTouche[self.indiceYMin]) and self.pointYMin < self.pointPlafond :
                self.calcForceRotation(self.pointTouche[self.indiceYMin][0], self.pointTouche[self.indiceYMin][1], True)
                self.y = objet.y+objet.height + (self.y-self.pointYMin)
                self.vitesseChute = 5
                self.plafond = True


            elif self.plafond == False and self.sol == True  and objet.collidepoint(self.pointTouche[self.indiceYMin]) and self.pointYMin < self.pointPlafond :
                self.calcForceRotation(self.pointTouche[self.indiceYMin][0], self.pointTouche[self.indiceYMin][1], True)
                self.vitesseChute = 5
                self.plafond = True

            elif self.murGauche == False and self.plafond == False and objet.collidepoint(self.pointTouche[self.indiceXMin]) and self.pointXMin < self.centrePalourde[0]:
                self.calcForceRotation(self.pointTouche[self.indiceXMin][0], self.pointTouche[self.indiceXMin][1], False)
                self.x =objet.x + objet.width + (self.x-self.pointXMin)
                self.murGauche = True

                self.vitesseAvancement = math.sqrt(abs(self.vitesseAvancement)) / 3
                return True

            elif self.murDroit == False and self.plafond == False and objet.collidepoint(self.pointTouche[self.indiceXMax]) and self.pointXMax > self.centrePalourde[0] :
                self.calcForceRotation(self.pointTouche[self.indiceXMax][0], self.pointTouche[self.indiceXMax][1], False)
                self.x = objet.x + (self.x-self.pointXMax)
                self.murDroit = True

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


        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            self.marche(1)
        elif pygame.key.get_pressed()[pygame.K_LEFT]or pygame.key.get_pressed()[pygame.K_q]:
            self.marche(-1)
        elif pygame.key.get_pressed()[pygame.K_z]:
            self.vitesseAvancement = 0
        else:
            self.speed = 0.1

        if pygame.key.get_pressed()[pygame.K_e]:
            self.roulement(-1)
        elif pygame.key.get_pressed()[pygame.K_a]:
            self.roulement(1)


        self.mouvementHorizontal()


        if self.onGround == False:
            self.isFalling = True
        else:
            self.isFalling = False


        if self.isFalling == True:
            self.tomber()
        elif self.timeChute <= 6/30:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.saut()

        self.mouvementVerticale()

        #Aide pour le fonctionnement des collisions
        self.pointSol = self.calcPointSol()
        self.pointPlafond = self.calcPointPlafond()
        self.onGround = False
        self.sol = False
        self.murGauche = False
        self.murDroit = False
        self.plafond = False

        if self.isFalling == False:
            self.forceRotationBase()

        #Teste les collisions avec tous objet de la liste listeObjetCollision
        for objet in listeObjetCollision:
            self.collison = self.collision(objet)

        self.rotationAvecForce()



        self.placement()