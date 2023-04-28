import random

import pygame
import math
from os import path

class Palourde:


    def __init__(self,surface,x : float,y : float):
        #Créé par Robin
        self.surface = surface
        self.x : float = self.surface.get_width()//2
        self.y : float = self.surface.get_height()//2

        self.xCamera : float = x
        self.yCamera : float = y

        self.xVoulut : float = self.x
        self.yVoulut : float = self.y

        # 616 et 276 sont les dimensions de l'image de la palourde
        self.HAUTEUR : int = 185//4
        self.LARGEUR : int = 354//4

        self.centrePalourde : tuple = (self.x+self.LARGEUR/2,self.y+self.HAUTEUR/2)

        self.PALOURDE_IMAGE : pygame.image = pygame.image.load(path.join("Assets/Entity/Player/palourde2.png"))
        self.PALOURDE_IMAGE_RESIZED : pygame.image = pygame.transform.scale(self.PALOURDE_IMAGE, (self.LARGEUR, self.HAUTEUR))

        self.CALQUE_PALOURDE_DEGAT : pygame.image = pygame.image.load(path.join("Assets/Entity/Player/calque_degat.png"))
        self.CALQUE_PALOURDE_DEGAT_RESIZED : pygame.image = pygame.transform.scale(self.CALQUE_PALOURDE_DEGAT, (self.LARGEUR, self.HAUTEUR))

        self.PALOURDE_BRAS_GAUCHE_IMAGE : pygame.image = pygame.image.load(path.join("Assets/Entity/Player/bras_gauche.png"))
        self.PALOURDE_BRAS_DROIT_IMAGE : pygame.image = pygame.image.load(path.join("Assets/Entity/Player/bras_droit.png"))

        self.PALOURDE_BRAS_GAUCHE_GANT_IMAGE : pygame.image = pygame.image.load(path.join("Assets/Entity/Player/bras_gauche_gant.png"))
        self.PALOURDE_BRAS_DROIT_GANT_IMAGE : pygame.image = pygame.image.load(path.join("Assets/Entity/Player/bras_droit_gant.png"))

        self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED : pygame.image = pygame.transform.scale(self.PALOURDE_BRAS_GAUCHE_IMAGE, (121//4, 199//4))
        self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED : pygame.image = pygame.transform.scale(self.PALOURDE_BRAS_DROIT_IMAGE, (149//4, 199//4))


        self.palourdeSprite : pygame.image= self.PALOURDE_IMAGE_RESIZED
        self.calquePalourdeDegatSprite : pygame.image = self.CALQUE_PALOURDE_DEGAT_RESIZED

        self.brasGaucheSprite : pygame.image = self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED
        self.brasDroitSprite : pygame.image = self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED

        #Le sprite de la palourde et des autree image subiront des rotation ce qui ne changera pas les dimensions des image et donc les distordra
        #Pour contrer cela, on utilise un rect créer ci dessous qui perme d'obtenir les bonnes dimensions pour les sprites et donc les afficher correctement plus tard
        self.rectRotation : pygame.Rect =  self.palourdeSprite.get_rect(center = self.PALOURDE_IMAGE_RESIZED.get_rect(topleft = (self.x,self.y)).center)

        self.palourdeRect : pygame.Rect = pygame.Rect(self.rectRotation[0],self.rectRotation[1],self.LARGEUR,self.HAUTEUR)

        self.surface.blit(self.palourdeSprite, self.palourdeRect)

        self.g : float = 9.81
        self.timeChute : int = 0

        self.vitesseChute : float = 1
        self.jumpForce : int = 250

        self.vitesseAvancement : float = 0
        self.speed : float = 0.1

        self.collison : bool = False
        self.isFalling : bool = True
        self.onGround : bool = False

        self.angle : float = 0
        self.pointRotation1 : float = self.g
        self.pointRotation2 : float = self.g
        self.retenuPoint1 : float = 0
        self.retenuPoint2 :float = 0

        self.angleBras : list = [self.angle,self.angle]
        self.coefAngleBras : list = [1,1]
        self.ancienSens : int = 0

        self.roule : bool = False
        self.ySol : float = self.y

        self.creationPoint()

        self.cameraLock : bool = False

        self.modeVersus : bool = False
        self.rayonPointBras : int = 28
        self.degreeBrasGauche : float = 300
        self.degreeBrasDroit : float = 234
        self.isKicking : bool = False
        self.etapeKick : int = 1
        self.sante : float = 100
        self.recoitDegat : bool = False
        self.frameRouge : int = 0
        self.mort : bool = False

        self.tempsDernierCoup : int = 0


    def calcPositionPoint(self,angle,rayon) -> tuple:
        """summary
        Renvoie un tuple de coordonné (x,y) qui se trouve à un rayon et un angle définit par rapport au centre de la palourde

        Args:
            angle (int): Définit l'angle auquel se trouve le point par rapport à l'angle de la palourde
            rayon (int): Définit le rayon auquel le point se trouvera par rapport au centre de la palourde
        """
        # Créé par Robin
        return (self.centrePalourde[0] + math.cos((self.angle+angle)*math.pi/180)*rayon, self.centrePalourde[1] + -math.sin((self.angle+angle)*math.pi/180)*rayon)

    def calcPositionPointRect(self,angle,rayon) -> pygame.Rect:
        """summary
        Renvoie un rect avec des cordonné (x,y) qui se trouve à un rayon et un angle définit par rapport au centre de la palourde
        Sert principalement au débogage

        Args:
            angle (int): Définit l'angle auquel se trouve le point par rapport à l'angle de la palourde
            rayon (int): Définit le rayon auquel le point se trouvera par rapport au centre de la palourde
        """
        # Créé par Robin
        return pygame.Rect(self.centrePalourde[0] + math.cos((self.angle+angle)*math.pi/180)*rayon, self.centrePalourde[1] + -math.sin((self.angle+angle)*math.pi/180)*rayon, 2, 2)


    def creationPoint(self) -> None:
        """summary
            Permet de créer/actualiser l'emplacement de point qui se trouve autour de la palourde afin d'effectuer plusieurs tâches plus tard comme les collisions
        """
        # Créé par Robin
        self.centrePalourde = (self.x + self.LARGEUR/2,self.y + self.HAUTEUR/2)

        #Calcule l'emplacement de tous les points de collisions autour de la palourde
        self.listePoint = [
            self.calcPositionPoint(80,23),
            self.calcPositionPoint(55,27),
            self.calcPositionPoint(30,35),
            self.calcPositionPoint(12, 40),
            self.calcPositionPoint(-5, 42),
            self.calcPositionPoint(-23, 35),
            self.calcPositionPoint(-42, 28),
            self.calcPositionPoint(-64, 26),
            self.calcPositionPoint(-106, 24),
            self.calcPositionPoint(-132, 26),
            self.calcPositionPoint(-152, 36),
            self.calcPositionPoint(-168, 42),
            self.calcPositionPoint(-180, 40),
            self.calcPositionPoint(168, 37),
            self.calcPositionPoint(150, 33),
            self.calcPositionPoint(125, 27),
            self.calcPositionPoint(100, 23),
        ]


        #Création de Rect qui permettent de voir l'emplacement de chaque point de collisions
        #Sert principalement pour le débogage
        self.listeRecte = [
            self.calcPositionPointRect(80, 23),
            self.calcPositionPointRect(55,27),
            self.calcPositionPointRect(30,35),
            self.calcPositionPointRect(12, 40),
            self.calcPositionPointRect(-5, 42),
            self.calcPositionPointRect(-23, 35),
            self.calcPositionPointRect(-42, 28),
            self.calcPositionPointRect(-64, 26),
            self.calcPositionPointRect(-106, 24),
            self.calcPositionPointRect(-132, 26),
            self.calcPositionPointRect(-152, 36),
            self.calcPositionPointRect(-168, 42),
            self.calcPositionPointRect(-180, 40),
            self.calcPositionPointRect(168, 37),
            self.calcPositionPointRect(150, 33),
            self.calcPositionPointRect(125, 27),
            self.calcPositionPointRect(100, 23),
        ]
        #Calcule l'emplacement des point de rotation/gravité de la palourde quand elle se trouve au sol
        self.xPointRotation1 = self.calcPositionPoint(180,24)
        self.xPointRotation2 = self.calcPositionPoint(0, 24)

        # Création de Rect qui permettent de voir l'emplacement de chaque point de rotation
        # Sert principalement pour le débogage
        self.rectPointRotation1 = self.calcPositionPointRect(180,24)
        self.rectPointRotation2 = self.calcPositionPointRect(0, 24)


        #Calcule de l'emplacement des bras de la palourde
        self.listePointMain = [
            self.calcPositionPoint(0, 42),
            self.calcPositionPoint(180, 42)
        ]

    def rotation(self,degree : float) -> None:
        """summary
            Change l'angle actuel de la palourde

            Args:
                degree (float): Le nombre de degré de rotation que la palourde doit faire
        """
        # Créé par Robin
        self.angle += degree
        self.angle %= 360

        for i in range(2):
            self.angleBras[i] += degree*self.coefAngleBras[i]
            self.angleBras[i] %= 360

        #Change l'angle de chaque sprite de la palourde
        self.palourdeSprite = pygame.transform.rotate(self.PALOURDE_IMAGE_RESIZED, self.angle)
        self.calquePalourdeDegatSprite = pygame.transform.rotate(self.CALQUE_PALOURDE_DEGAT_RESIZED, self.angle)

        self.brasGaucheSprite = pygame.transform.rotate(self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED, self.angleBras[0])
        self.brasDroitSprite = pygame.transform.rotate(self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED, self.angleBras[1])

        # permet de former un tuple qui possède les coordonnés de la palourde et de sa taille lors des rotation
        self.rectRotation =  self.palourdeSprite.get_rect(center = self.PALOURDE_IMAGE_RESIZED.get_rect(topleft = (self.x,self.y)).center)



    def roulement(self,sens : float) -> None:
        # Créé par Robin
        """summary
                Effectue toutes les étapes suivent permettant d'effectuer le mouvement du joueur suite à la pression d'une touche

            Args:
                sens (int): Vaut soit -1 (pour à droite), soit 1 (pour à gauche), permet d'adapté les calcules au sens
        """
        self.roule = True
        self.peutRouler = False

        #Limite la vitesse de la palourde
        if sens == 1:
            if self.vitesseAvancement > -10:
                self.peutRouler = True
        else:
            if self.vitesseAvancement < 10:
                self.peutRouler = True

        #Change le coefficient de changement d'angle des bras afin d'avoir des mouvements plus dynamiques
        #S'active quand le joueur change de sens
        if self.ancienSens != sens :
            for i in range(2):
                self.coefAngleBras[i] = random.randint(-150,150)
                self.coefAngleBras[i] /= 100

        self.ancienSens = sens


        if self.onGround == True and self.peutRouler:
            #Change la vitesse et la vitesse de rotation de la palourde en fonction de sa vitesse
            if sens == 1:
                self.vitesseAvancement += (math.cos((self.angle + 90)%180 *math.pi/180) /10 + 0.09)*-1
            else:
                self.vitesseAvancement += (math.cos((180-(self.angle + 90)%180) *math.pi/180) /10 + 0.09)

            self.forceRotationBase( -sens + self.vitesseAvancement)

        elif self.onGround == True:
            #Change la rotation de la palourde en fonction de sa vitesse
            self.forceRotationBase( -sens + self.vitesseAvancement)

        else:
            #Change la rotation de la palourde en fonction d'une valeur prédéfini
            self.forceRotationBase(3*-sens)


    def calcForcePointRotation(self,chute : bool,x : float,y : float ) -> float:
        """summary
            'Simple' calcule permettant le fonctionnement de 'calcForceRotation' et donc d'effectuer les rotations qui arrivent suite à une collision

        :param x: l'emplacement en x de l'impact
        :param y: l'emplacement en y de l'impact
        :param chute: booléen qui vaut True si c'est un impact verticale
        """
        # Créé par Robin
        if chute == True:
            return math.sqrt(abs(math.sqrt(((x-self.centrePalourde[0])**2 + (
                    y-self.centrePalourde[1])**2))/25 * self.vitesseChute/100 * math.sqrt(
                abs((x-self.centrePalourde[1])))))
        else:
            return math.sqrt(abs(math.sqrt(((x - self.centrePalourde[0]) ** 2 + (
                    y - self.centrePalourde[1]) ** 2)) / 25 * self.vitesseAvancement * math.sqrt(
                abs((y - self.centrePalourde[1])))))

    def calcForceRotation(self,x,y,verticale) -> None:
        """
        Calcule les forces de collision que sur la gauche et la droite de la palourde ce qui permet de déterminer sa rotation

        :param x: l'emplacement en x de l'impact
        :param y: l'emplacement en y de l'impact
        :param verticale: booléen qui vaut True si c'est un impact verticale
        """
        # Créé par Robin

        #Détermination de quelle type de collision la pallourde reçoit afin de tourner dans le bon sens
        if verticale == True :
            #On arrete de faire des rotation à un certain angle quand la palourde est au sol
            #Sinon elle ne se stopera jamais et fera une rotation à gauche puis une à droite
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
                        self.pointRotation2 += self.calcForcePointRotation(True,x,y)
                    else:
                        self.pointRotation1 += self.calcForcePointRotation(True,x,y)
                else:
                    if x > self.centrePalourde[0]:
                        self.pointRotation1 -= self.calcForcePointRotation(True,x,y)
                    else:
                        self.pointRotation2 -= self.calcForcePointRotation(True,x,y)
        else:
            if 90 < self.angle < 270:
                if x < self.centrePalourde[0]:
                    if y < self.centrePalourde[1]:
                        self.pointRotation2 += self.calcForcePointRotation(False,x,y)
                    else:
                        self.pointRotation2 -= self.calcForcePointRotation(False,x,y)

                else:
                    if y < self.centrePalourde[1]:
                        self.pointRotation1 += self.calcForcePointRotation(False,x,y)
                    else:
                        self.pointRotation1 -= self.calcForcePointRotation(False,x,y)
            else:
                if x < self.centrePalourde[0]:
                    if y < self.centrePalourde[1]:
                        self.pointRotation1 -= self.calcForcePointRotation(False,x,y)
                    else:
                        self.pointRotation1 += self.calcForcePointRotation(False,x,y)
                else:
                    if y < self.centrePalourde[1]:
                        self.pointRotation2 -= self.calcForcePointRotation(False,x,y)
                    else:
                        self.pointRotation2 += self.calcForcePointRotation(False,x,y)


    def rotationAvecForce(self) -> None:
        """summary
           Effectue la rotation de la palourde suite aux forces émise au deux point de rotation
        """
        # Créé par Robin

        self.rotation((self.pointRotation1-self.pointRotation2)/10)
        self.creationPoint()


        if self.sol == True:
            #Permet de faire que la palourde reste sur le sol quand elle roulle elle se trouve sur le sol, et évite alors qu'elle se décroche du sol quand elle roule
            self.yMax = self.listePoint[0][1]

            for y in self.listePoint:
                if y[1] > self.yMax:
                    self.yMax = y[1]

            self.y = self.ySol + (self.y - self.yMax)

            #Permet d'effectuer les mouvement de la palourde quand elle ne bouge pas et qu'elle est en train de tourner d'elle même suite à la gravité
            if self.roule == False and abs(self.pointRotation1-self.pointRotation2) > 0.1:
                if self.pointRotation1-self.pointRotation2 > 0:
                    self.vitesseAvancement += -0.2 * abs(self.angle%180 - 90) / 90
                else:
                    self.vitesseAvancement += 0.2* abs(self.angle%180 - 90) / 90

    def forceRotationMoyenne(self) -> None:
        """summary
        Met les forces des deux points de force à leur moitié
        """
        # Créé par Robin
        self.pointRotation1 = (self.pointRotation1 + self.g)/2
        self.pointRotation2 = (self.pointRotation2 + self.g)/2

    def forceRotationBase(self,multiplicateur : float) -> None:
        """summary
        Change les points de forces en fonctions d'un coef prédéfini

        Args:
            multiplicateur (float): coefficient pour le changement de valeur de forces de rotation
        """
        # Créé par Robin

        self.pointRotation1 = self.g
        self.pointRotation2 = self.g

        if multiplicateur > 0:
            self.pointRotation2 = self.g * multiplicateur
        else:
            self.pointRotation1 = -self.g * multiplicateur



    def tomber(self) -> None:
        """summary
        Permet de changer la vitesse à laquelle la palourde tombe on fonction du temps qu'elle tombe
        """
        # Créé par Robin
        self.timeChute+=1/60

        self.vitesseChute += self.g*self.timeChute

    def saut(self) -> None:
        """summary
        Effectue un mouvement que l'on peut catégoriser de saut
        """
        # Créé par Robin
        self.forceRotationMoyenne()
        self.onGround = False
        self.vitesseChute -= self.jumpForce

    def mouvementVerticale(self) -> None:
        """summary
        Change la coordonnée y de la palourde en fonction de la variable vitesseChute
        """
        # Créé par Robin

        #Nous changeons la variable yCamera quand la caméra n'est pas lock vu que pour
        #faire bougez les objets aux alentours de la palourde, nous faisons bougez les objets
        #autour de la palourde et pas bouger la palourde .
        #Si nous faisons bouger la palourde en même temps que les objets aux alentours, elle finira par s'afficher en dehors
        #de la fenetre d'affichage (vu que ses coordonnées dépasserront la taille de la fenetre)
        if self.cameraLock == False:
            self.yCamera += self.vitesseChute/60
        else:
            self.y += self.vitesseChute / 60

    def mouvementHorizontal(self) -> None:
        """summary
        Change la coordonée x de la palourde en fonction de la variable vitesseAvancement
        """
        # Créé par Robin

        self.xCamera += self.vitesseAvancement
    
    def updateTotalCo(self):
        self.xTotal = self.x + self.xCamera
        self.yTotal = self.y + self.yCamera
        return self.xTotal, self.yTotal


    def marche(self,sens) -> None:
        """summary
        Permet à la palourde de se déplacer sans rouler

        Sert uniquement pour les test et le débogage
        """
        # Créé par Robin
        if self.speed < 5:
            self.speed += 0.1

        self.vitesseAvancement = self.speed *sens

    def reaparitionApresChute(self) -> None:
        """summary
        Permet à la palourde de réapparaître à un certain point en hauteur

        S'active quand la palourde tombe dans le vide
        """
        # Créé par Robin
        self.y = -750
        self.vitesseChute = -100
        self.timeChute = 0
        self.vitesseAvancement = random.randint(-50,50) / 10

    def changementModeNormal(self) -> None:
        """summary
        Permet une réinitialisation de la palourde pour son fonctionnement normale
        """
        # Créé par Robin
        self.modeVersus = False
        self.sante = 100
        self.mort = False
        self.PALOURDE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_IMAGE, (self.LARGEUR, self.HAUTEUR))

        self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_GAUCHE_IMAGE,(121 // 4, 199 // 4))
        self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_DROIT_IMAGE,(149 // 4, 199 // 4))

        self.rayonPointBras = 28
        self.degreeBrasGauche = 300
        self.degreeBrasDroit = 234

    def changementModeVersus(self) -> None:
        """summary
        Permet une réinitialisation de la palourde pour son mode versus
        """
        # Créé par Robin
        self.modeVersus = True
        self.sante = 100
        self.mort = False
        self.PALOURDE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_IMAGE, (self.LARGEUR, self.HAUTEUR))

        self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_GAUCHE_GANT_IMAGE,(142 // 4, 202 // 4))
        self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_DROIT_GANT_IMAGE,(106 // 4, 222 // 4))

        self.rayonPointBras = 27
        self.degreeBrasGauche = 312
        self.degreeBrasDroit = 243

    def attaquePalourde(self) -> None:
        """summary
        Permet d'indiquer que la palourde lance une attaque
        """
        # Créé par Robin
        self.isKicking = True

    def mouvementAttaquePalourde(self) -> None:
        """summary
        Etape prédéfinit permettant de lancer une petite animation des bras de la palourde afin qu'elle puisse attaquer
        """
        # Créé par Robin
        if self.etapeKick < 25:
            self.angleBras[0] += 0.9 * math.log10(self.etapeKick)**2
            self.angleBras[1] -= 0.9 * math.log10(self.etapeKick)**2
        elif self.etapeKick < 46:
            self.angleBras[0] -= 1.2 * math.log10(self.etapeKick) ** 3
            self.angleBras[1] += 1.2 * math.log10(self.etapeKick) ** 3
        else:
            self.angleBras[0] += 4.5
            self.angleBras[1] -= 4.5

        self.etapeKick += 1

        if self.etapeKick >= 52:
            self.isKicking = False
            self.etapeKick = 1

    def coupSubi(self,sens) -> None:
        """summary
        Projette la palourde, permettant alors qu'elle se prenne des dégats

        S'active suite à avoir reçut un coup de la part d'une autre palourde
        """
        # Créé par Robin
        if pygame.time.get_ticks() - self.tempsDernierCoup > 800:
            self.vitesseAvancement += 15 * sens
            self.saut()
            self.tempsDernierCoup = pygame.time.get_ticks()

    def analyseVie(self) -> None:
        """summary
        Permet de changer l'état de la palorde en fonction de sa vie
        """
        # Créé par Robin
        if 20 < self.sante < 50 :
            self.PALOURDE_IMAGE_RESIZED = pygame.transform.scale(pygame.image.load(path.join("Assets/Entity/Player/palourde2_endommage1.png")), (self.LARGEUR, self.HAUTEUR))
        elif self.sante < 20:
            self.PALOURDE_IMAGE_RESIZED = pygame.transform.scale(
                pygame.image.load(path.join("Assets/Entity/Player/palourde2_endommage2.png")),(self.LARGEUR, self.HAUTEUR))

        if self.sante <= 0:
            self.mort = True

        if self.recoitDegat == True:
            self.frameRouge = 5
            self.recoitDegat = False

        if self.frameRouge > 0:
            self.frameRouge -= 1

    def placementBras(self) -> None:
        """summary
        Permet de placer les bras de la palourde au bon endroit avec la bonne rotation
        """
        # Créé par Robin
        self.brasGaucheRectRotation = self.brasGaucheSprite.get_rect(center = self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED.get_rect(bottomright = self.listePointMain[1]).center)
        self.brasDroitRectRotation = self.brasDroitSprite.get_rect(center=self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED.get_rect(bottomleft=self.listePointMain[0]).center)

        #Calcul permettant de placer le début des bras de la palourde au bon emplacement
        self.cooBrasGauche = (self.brasGaucheRectRotation.centerx + math.cos((self.angleBras[0]+self.degreeBrasGauche) * math.pi / 180) * self.rayonPointBras,
                                self.brasGaucheRectRotation.centery + -math.sin((self.angleBras[0]+self.degreeBrasGauche) * math.pi / 180) * self.rayonPointBras)
        self.cooBrasDroit = (self.brasDroitRectRotation.centerx + math.cos((self.angleBras[1] + self.degreeBrasDroit) * math.pi / 180) * self.rayonPointBras,
                              self.brasDroitRectRotation.centery + -math.sin((self.angleBras[1] + self.degreeBrasDroit) * math.pi / 180) * self.rayonPointBras)

        self.brasGaucheRectRotation = self.brasGaucheSprite.get_rect(
            center=self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED.get_rect(bottomright= (self.listePointMain[1][0] + (self.listePointMain[1][0] - self.cooBrasGauche[0]),self.listePointMain[1][1] + (self.listePointMain[1][1] - self.cooBrasGauche[1]))).center)
        self.brasDroitRectRotation = self.brasDroitSprite.get_rect(
            center=self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED.get_rect(bottomleft= (self.listePointMain[0][0] + (self.listePointMain[0][0] - self.cooBrasDroit[0]),self.listePointMain[0][1] + (self.listePointMain[0][1] - self.cooBrasDroit[1]))).center)



    def placement(self) -> None:
        """summary
        Effectue tout l'affichage en rapport avec la palourde
        """
        # Créé par Robin
        self.centrePalourde = (self.x + self.LARGEUR/2,self.y + self.HAUTEUR/2)

        self.rectRotation = self.palourdeSprite.get_rect(
            center=self.PALOURDE_IMAGE_RESIZED.get_rect(topleft=(self.x, self.y)).center)
        self.palourdeRect = pygame.Rect(self.rectRotation[0],self.rectRotation[1] ,self.LARGEUR,self.HAUTEUR)


        self.placementBras()

        #Affiche le sprite potententiellement tourné de la pallourde en fonction d'un rect qui aura les dimensions
        #qui permettent d'afficher le sprite sans déformation
        self.surface.blit(self.palourdeSprite, self.rectRotation)

        #Si la palourde se trouve dans le mode versus et reçois des dégats, on affiche un calque par
        #dessu étant donné que c'était la solution la plus simple à faire avec pygame
        if self.frameRouge > 0:
            self.surface.blit(self.calquePalourdeDegatSprite, self.rectRotation)

        self.surface.blit(self.brasGaucheSprite, self.brasGaucheRectRotation)
        self.surface.blit(self.brasDroitSprite, self.brasDroitRectRotation)

        #Permet l'affichage de l'emplacement de chaque point de collision de la palourde
        # for i in range (len(self.listeRecte)):
        #     pygame.draw.rect(self.surface, (100+i*5,255-10*i,255 - i*5), self.listeRecte[i])

        self.creationPoint()


    def calcPointSol(self) -> None:
        """summary
        Permet de savoir quelle point de collision de la palourde sont éligibles à avoir une collision avec le sol
        """
        # Créé par Robin
        self.pointPlusBas = []
        for point in self.listePoint:
            self.pointPlusBas.append(point[1])
        self.pointPlusBas.sort()

        #Les indices placés dans le return permettent de choisir le nombre de point que l'on veut éligible à avoir une collision avec le sol
        #Cela permet d'éviter quelque bugs de collision
        if 45<self.angle<135 or 225<self.angle<315:
            return self.pointPlusBas[-2]
        else:
            return self.pointPlusBas[-3]

    def calcPointPlafond(self) -> None:
        """summary
        Permet de savoir quelle points de collisions de la palourde sont éligibles à avoir une collision avec le 'plafond'
        """
        # Créé par Robin
        self.pointPlusHaut = []
        for point in self.listePoint:
            self.pointPlusHaut.append(point[1])
        self.pointPlusHaut.sort()

        #Les indices placés dans le return permettent de choisir le nombre de point que l'on veut éligible à avoir une collision avec le palfond
        #Cela permet d'éviter quelque bugs de collision
        if 45<self.angle<135 or 225<self.angle<315:
            return self.pointPlusHaut[1]
        else:
            return self.pointPlusHaut[2]


    def collision(self,objet : pygame.Rect) -> bool:
        """summary
        Permet de détecter des collisions avec l'ensemble un bloc de la carte

        Args:
            objet (float): Rect avec lequel on regarde si la palourde a des collisions
        """
        # Créé par Robin
        collisionFrame = False

        for _ in range(4):
            collision = False
            self.pointTouche = []

            #enregitre tous les points de collision de la pallourde qui entre en collision avec le rect objet
            for point in self.listePoint:
                if objet.collidepoint(point):
                    self.pointTouche.append(point)

            if len(self.pointTouche) > 0:
                #Enregistre les coordonnées extreme de collision
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

                #Des dégats sont ajoutés à la palourde dans chaque type de collision si
                #le mode versus est activé et que la palourde possède aussi une vitesse minimum

                #Collision avec le sol
                if self.sol == False and self.onGround == True and collision == False and ((self.pointTouche[self.indiceYMax][1] < objet.y + objet.height//3 and self.vitesseChute < 300) or (self.pointTouche[self.indiceYMax][1] < objet.y + objet.height//2 and self.vitesseChute >= 300)):
                    self.calcForceRotation(self.pointTouche[self.indiceYMax][0],self.pointTouche[self.indiceYMax][1],True)

                    self.ySol = objet.y

                    self.y = self.ySol + (self.y-self.pointYMax)

                    if abs(self.vitesseChute) > 5*60 and self.modeVersus == True:
                        self.sante -= abs(self.vitesseChute) / 60
                        self.recoitDegat = True
                    self.timeChute = 0
                    self.vitesseChute = 0

                    if abs(self.vitesseAvancement) >0.1 and self.roule == False:
                        self.vitesseAvancement /= 1.1
                    elif self.roule == False:
                        self.vitesseAvancement = 0
                    self.sol = True
                    self.creationPoint()

                    collision = True

                #Collsion avec le 'plafond' sans collsion avec le sol
                elif self.plafond == False and self.sol == False  and objet.collidepoint(self.pointTouche[self.indiceYMin]) and self.pointYMin < self.pointPlafond and collision == False and self.pointTouche[self.indiceYMin][1] > objet.y + objet.height//4:
                    self.calcForceRotation(self.pointTouche[self.indiceYMin][0], self.pointTouche[self.indiceYMin][1], True)
                    self.y = objet.y+objet.height + (self.y-self.pointYMin)
                    if abs(self.vitesseChute) > 5*60 and self.modeVersus == True:
                        self.sante -= abs(self.vitesseChute) / 60
                        self.recoitDegat = True
                    self.vitesseChute = 5
                    self.plafond = True
                    self.creationPoint()

                    collision = True

                #Collision avec le 'plafond' avec collision avec le sol
                elif self.plafond == False and self.sol == True  and objet.collidepoint(self.pointTouche[self.indiceYMin]) and self.pointYMin < self.pointPlafond and collision == False:
                    self.calcForceRotation(self.pointTouche[self.indiceYMin][0], self.pointTouche[self.indiceYMin][1], True)
                    if abs(self.vitesseChute) > 5*60 and self.modeVersus == True:
                        self.sante -= abs(self.vitesseChute) / 60
                        self.recoitDegat = True
                    self.vitesseChute = 5
                    self.plafond = True
                    self.creationPoint()

                    collision = True

                #Collision avec un mur gauche
                elif self.murGauche == False and self.plafond == False and objet.collidepoint(self.pointTouche[self.indiceXMin]) and self.pointXMin < self.centrePalourde[0] and objet.y + 1 < self.pointTouche[self.indiceXMin][1] < objet.y + objet.height - 1 and collision == False:
                    self.calcForceRotation(self.pointTouche[self.indiceXMin][0], self.pointTouche[self.indiceXMin][1], False)
                    self.x =objet.x + objet.width + (self.x-self.pointXMin)
                    self.murGauche = True
                    self.creationPoint()

                    if abs(self.vitesseAvancement) > 5 and self.modeVersus == True:
                        self.sante -= abs(self.vitesseAvancement)
                        self.recoitDegat = True

                    self.vitesseAvancement = math.sqrt(abs(self.vitesseAvancement)) / 3

                    collision = True

                #Collision avec un mur droit
                elif self.murDroit == False and self.plafond == False and objet.collidepoint(self.pointTouche[self.indiceXMax]) and self.pointXMax > self.centrePalourde[0] and objet.y+1 < self.pointTouche[self.indiceXMax][1] < objet.y + objet.height - 1  and collision == False:
                    self.calcForceRotation(self.pointTouche[self.indiceXMax][0], self.pointTouche[self.indiceXMax][1], False)
                    self.x = objet.x + (self.x-self.pointXMax)
                    self.murDroit = True
                    self.creationPoint()

                    if abs(self.vitesseAvancement) > 5 and self.modeVersus == True:
                        self.sante -= abs(self.vitesseAvancement)
                        self.recoitDegat = True

                    self.vitesseAvancement = -1 * math.sqrt(abs(self.vitesseAvancement)) / 3

                    collision = True
            else:
                break

        return collisionFrame

    def replacementCameraApresCollision(self) -> None:
        """summary
        Permet de replacer la caméra suite un écart des coordonnées suite à un trop grand mouvement

        Le fait de manière fluide lorsque la palourde ne touche pas le sol
        """
        # Créé par Robin
        self.xCamera += self.x - self.xVoulut
        self.x = self.xVoulut

        if self.yCamera > 1000 :
            self.y += self.yCamera - 1000
            self.yCamera = 1000
        elif self.onGround == True :
            self.yCamera += self.y - self.yVoulut
            self.yCamera -= (self.y - self.yVoulut)
        else:
            if abs(self.y - self.yVoulut) < 0.5:
                self.yCamera += self.y - self.yVoulut
                self.y = self.yVoulut
            else:
                self.yCamera += (self.y - self.yVoulut) * 0.05
                self.y -= (self.y - self.yVoulut) * 0.05

    def lockCamera(self,x : float,y : float) -> None:
        """summary
        Bloque les changements de caméra et fait apparaître la palourde à des coordonnées prédéfinit

        Args:
            x (float): coordonnée x où la palourde va spawn dans l'écran
            y (float): coordonnée y où la palourde va spawn dans l'écran
        """
        # Créé par Robin
        self.cameraLock = True

        self.x = x
        self.y = y

        self.xCamera = 0
        self.yCamera = 0

    def unlockCamera(self,x : float,y : float) -> None:
        """summary
        Débloque la caméra et la met à des coordonnées préciser dans les paramètres

        Args:
            x (float): coordonnée x où la caméra va apparaître
            y (float): coordonnée y où la caméra va apparaître
        """
        # Créé par Robin
        self.cameraLock = False
        self.xCamera = x
        self.yCamera = y

        #Replace la palourde à l'endroit voulut sur l'écran
        self.x = self.xVoulut
        self.y = self.yVoulut


    def framePalourde(self,listeObjetCollision) -> None:
        """summary
        Effectue l'entièreté des actions que la palourde doit effectuer à chaque frame

        Args:
            listeObjetCollision (array): Liste de rect qui auront un test de collision avec la palourde
        """
        # Créé par Robin
        #Si la palourde est considéré comme 'morte', elle ne s'affichera plus
        if self.mort == False:

            self.mouvementHorizontal()

            if self.onGround == False:
                self.isFalling = True
            else:
                self.isFalling = False

            if self.isFalling == True:
                self.tomber()

            if self.isKicking == True:
                self.mouvementAttaquePalourde()


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

            if self.modeVersus == True:
                self.analyseVie()


            if self.cameraLock == False:
                #Replacement de la caméra suite et des changements de position suite aux collisions
                self.replacementCameraApresCollision()
            else:
                #Placement de la caméra fixe
                self.x += self.xCamera
                self.y += self.yCamera

                self.xCamera = 0
                self.yCamera = 0

            self.rotationAvecForce()

            #Permet de faire réapparaître la palourde en hateur suite à une chute dans le vide
            if self.y > 2000 or self.yCamera > 2000:
                self.reaparitionApresChute()

            self.placement()


class OtherPalourde:


    def __init__(self,surface,x : float,y : float):
        # Créé par Robin

        #Cette objet est permet d'afficher uniquement la position des palourdes des autres joueurs avec leurs états

        self.surface = surface
        self.x = x
        self.y = y

        # 185 et 354 sont les dimensions de l'image de la palourde
        self.HAUTEUR = 185//4

        self.LARGEUR = 354//4

        self.centrePalourde = (self.x+self.LARGEUR/2,self.y+self.HAUTEUR/2)

        self.PALOURDE_IMAGE = pygame.image.load(path.join("Assets/Entity/Player/palourde2.png"))
        self.PALOURDE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_IMAGE, (self.LARGEUR, self.HAUTEUR))

        self.palourdeSprite = self.PALOURDE_IMAGE_RESIZED

        # Le sprite de la palourde et des autree image subiront des rotation ce qui ne changera pas les dimensions des image et donc les distordra
        # Pour contrer cela, on utilise un rect créer ci dessous qui perme d'obtenir les bonnes dimensions pour les sprites et donc les afficher correctement plus tard
        self.rectRotation =  self.palourdeSprite.get_rect(center = self.PALOURDE_IMAGE_RESIZED.get_rect(topleft = (self.x,self.y)).center)

        self.PALOURDE_BRAS_GAUCHE_IMAGE = pygame.image.load(path.join("Assets/Entity/Player/bras_gauche.png"))
        self.PALOURDE_BRAS_DROIT_IMAGE = pygame.image.load(path.join("Assets/Entity/Player/bras_droit.png"))

        self.PALOURDE_BRAS_GAUCHE_GANT_IMAGE = pygame.image.load(path.join("Assets/Entity/Player/bras_gauche_gant.png"))
        self.PALOURDE_BRAS_DROIT_GANT_IMAGE = pygame.image.load(path.join("Assets/Entity/Player/bras_droit_gant.png"))

        self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_GAUCHE_IMAGE, (121//4, 199//4))
        self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_DROIT_IMAGE, (149//4, 199//4))

        self.brasGaucheSprite = self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED
        self.brasDroitSprite = self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED

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

        self.angleBras = [self.angle,self.angle]
        self.coefAngleBras = [0.2,1]
        self.ancienSens = 1
        self.listePointMain = [
            self.placementPoint(0, 42, 42),
            self.placementPoint(180, 42, 42)
        ]

        self.modeVersus = False
        self.rayonPointBras = 28
        self.degreeBrasGauche = 300
        self.degreeBrasDroit = 234

        self.pointsCollisions = []

        #on initialise avec des rect qui changeront plus tard, cela permet d'éviter de réinitialiser la variable à chaque fois
        self.rect = [pygame.Rect(self.x,self.y,5,5) for _ in range(5)]


    def rotation(self,degree) -> None:
        """summary
        Change l'angle actuel de la palourde

        Args:
            degree (float): Le nombre de degré de rotation que la palourde doit faire
        """
        # Créé par Robin
        self.angle += degree
        self.angle %= 360


        #Permet de vérifier si la palorde des autres joueurs continu de tourner dans le même sens
        #Si ce n'est pas le cas, cela change les coefficients qui vont changer l'angles des bras des autres palourdes
        if degree > 0 :
            sens = 1
        elif degree < 0 :
            sens = -1

        if self.ancienSens != sens:
            for i in range(2):
                self.coefAngleBras[i] = random.randint(-150,150) / 100
            self.ancienSens = sens

        #Change l'angle de chaque bras de la palourde
        for i in range(2):
            self.angleBras[i] += degree * self.coefAngleBras[i]
            self.angleBras[i] %= 360

        self.palourdeSprite = pygame.transform.rotate(self.PALOURDE_IMAGE_RESIZED, self.angle)

        self.brasGaucheSprite = pygame.transform.rotate(self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED, self.angleBras[0])
        self.brasDroitSprite = pygame.transform.rotate(self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED, self.angleBras[1])

        # permet de former un tuple qui possède les coordonnés de la palourde et de sa taille lors des rotation
        self.rectRotation =  self.palourdeSprite.get_rect(center = self.PALOURDE_IMAGE_RESIZED.get_rect(topleft = (self.x,self.y)).center)

    def changementModeVersus(self) -> None:
        """summary
        Change l'image de la palourde et l'emplacement des bras pour qu'ils soit adapté au mode versus ou non
        """
        # Créé par Robin
        self.modeVersus = not self.modeVersus

        #On doit prendre d'autre valeur vu que nous utilisons une image avec d'autre dimensions
        if self. modeVersus == True:
            self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_GAUCHE_GANT_IMAGE,(142 // 4, 202 // 4))
            self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_DROIT_GANT_IMAGE,(106 // 4, 222 // 4))

            self.rayonPointBras = 27
            self.degreeBrasGauche = 312
            self.degreeBrasDroit = 243


        else:
            self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_GAUCHE_IMAGE,(121 // 4, 199 // 4))
            self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED = pygame.transform.scale(self.PALOURDE_BRAS_DROIT_IMAGE,(149 // 4, 199 // 4))

            self.rayonPointBras = 28
            self.degreeBrasGauche = 300
            self.degreeBrasDroit = 234


    def placementBras(self) -> None:
        """summary
        Permet de placer les bras de la palourde au bon endroit avec la bonne rotation
        """
        # Créé par Robin
        self.listePointMain = [
            self.placementPoint(0, 42, 42),
            self.placementPoint(180, 42, 42)
        ]

        self.brasGaucheRectRotation = self.brasGaucheSprite.get_rect(center = self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED.get_rect(bottomright = self.listePointMain[1]).center)
        self.brasDroitRectRotation = self.brasDroitSprite.get_rect(center=self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED.get_rect(bottomleft=self.listePointMain[0]).center)

        # Calcul permettant de placer le début des bras de la palourde au bon emplacement
        self.cooBrasGauche = (self.brasGaucheRectRotation.centerx + math.cos((self.angleBras[0]+self.degreeBrasGauche) * math.pi / 180) * self.rayonPointBras,
                                self.brasGaucheRectRotation.centery + -math.sin((self.angleBras[0]+self.degreeBrasGauche) * math.pi / 180) * self.rayonPointBras)
        self.cooBrasDroit = (self.brasDroitRectRotation.centerx + math.cos((self.angleBras[1] + self.degreeBrasDroit) * math.pi / 180) * self.rayonPointBras,
                              self.brasDroitRectRotation.centery + -math.sin((self.angleBras[1] + self.degreeBrasDroit) * math.pi / 180) * self.rayonPointBras)

        self.brasGaucheRectRotation = self.brasGaucheSprite.get_rect(
            center=self.PALOURDE_BRAS_GAUCHE_IMAGE_RESIZED.get_rect(bottomright= (self.listePointMain[1][0] + (self.listePointMain[1][0] - self.cooBrasGauche[0]),self.listePointMain[1][1] + (self.listePointMain[1][1] - self.cooBrasGauche[1]))).center)
        self.brasDroitRectRotation = self.brasDroitSprite.get_rect(
            center=self.PALOURDE_BRAS_DROIT_IMAGE_RESIZED.get_rect(bottomleft= (self.listePointMain[0][0] + (self.listePointMain[0][0] - self.cooBrasDroit[0]),self.listePointMain[0][1] + (self.listePointMain[0][1] - self.cooBrasDroit[1]))).center)



    def centre(self) -> tuple:
        """summary
        Renvoie un tuple avec les coordonnées du centre de la paloude
        """
        # Créé par Robin
        return (self.x + self.LARGEUR//2, self.y + self.HAUTEUR//2)


    def placementPoint(self ,angle,cos : int,sin : int) -> tuple:
        """summary
        Renvoie un tuple possédant de coodonnées par rapport au centre de la palourde, un angle et un rayon donné

        Args:
            angle (float): angle par lequel se trouve le point par rapport à l'angle de la palourde
            cos (int): rayon en cosinus du point
            sin (int): rayon en sinus du point
        """
        # Créé par Robin
        return (self.centre()[0] + math.cos((self.angle + angle) * math.pi / 180) * cos,
                self.centre()[1] + -math.sin((self.angle + angle) * math.pi / 180) * sin)

    def placementRect(self) -> None:
        """summary
        Créer/Actualise l'ensemble des Rect que la palourde du joueur de cette machine pourra avoir en collision
        """
        # Créé par Robin
        #Pour créer les Rect, on place des point sur la palourde qui resteront toujours au même endroit
        #par rapport à la palourde et qui forme alours un rectangle qui est le Rect
        for i in range(5):
            if self.pointsCollisions[i][0] < self.pointsCollisions[i + 5][0]:
                x = self.pointsCollisions[i][0]
                largeur = self.pointsCollisions[i + 5][0] - self.pointsCollisions[i][0]
            else:
                x = self.pointsCollisions[i+5][0]
                largeur = self.pointsCollisions[i][0] - self.pointsCollisions[i + 5][0]

            if self.pointsCollisions[i][1] < self.pointsCollisions[i + 5][1]:
                y = self.pointsCollisions[i][1]
                hauteur = self.pointsCollisions[i + 5][1] - self.pointsCollisions[i][1]
            else:
                y = self.pointsCollisions[i+5][1]
                hauteur = self.pointsCollisions[i][1] - self.pointsCollisions[i + 5][1]

            self.rect[i] = pygame.Rect(x,y,largeur,hauteur)
            if self.rect[i].height == 0:
                self.rect[i].height = 10
            elif self.rect[i].width == 0:
                self.rect[i].width = 10


    def placement(self) -> None:
        """summary
        Actualise tous les affichages de la palourde
        """
        # Créé par Robin
        self.centrePalourde = (self.x + self.LARGEUR/2,self.y + self.HAUTEUR/2)

        self.rectRotation = self.palourdeSprite.get_rect(
            center=self.PALOURDE_IMAGE_RESIZED.get_rect(topleft=(self.x, self.y)).center)
        self.palourdeRect = pygame.Rect(self.rectRotation[0],self.rectRotation[1] ,self.LARGEUR,self.HAUTEUR)

        self.placementBras()

        #self.surface.blit(self.palourde_sprite, (self.x, self.y))
        self.surface.blit(self.palourdeSprite, self.rectRotation)

        self.surface.blit(self.brasGaucheSprite, self.brasGaucheRectRotation)
        self.surface.blit(self.brasDroitSprite, self.brasDroitRectRotation)

        self.pointsCollisions = [
            self.placementPoint(173, 43, 43),
            self.placementPoint(152, 35, 35),
            self.placementPoint(125, 27, 27),
            self.placementPoint(56, 23, 23),
            self.placementPoint(28, 34, 34),
            self.placementPoint(210, 35, 35),
            self.placementPoint(232, 25, 25),
            self.placementPoint(298, 24, 24),
            self.placementPoint(333, 34, 34),
            self.placementPoint(346, 42, 42),
        ]

        self.placementRect()
