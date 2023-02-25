import pygame
import sys
import random

class RandomObject(pygame.sprite.Sprite):
    def __init__(self, groups, intervalleX = (-10000,10000), intervalleY = (0,2000)) :
        super().__init__(*groups)
        self.TEST_IMAGE = pygame.image.load('tree.png')

        self.x, self.y = random.randint(*intervalleX), random.randint(*intervalleY)
        self.image = self.TEST_IMAGE
        self.rect = self.image.get_rect(topleft = (self.x, self.y))



class CameraGroup(pygame.sprite.Group):
    """
    Objet qui permet de faire la gestion d'une caméra qui se déplace dans un milieu.
    """

    def __init__(self, displaySurface, *sprites):
        """
        Initialise les variales et les constantes
        displaySurface -- Surface pygame où les sprites serant rajoutés
        sprites        -- Ajouter des sprites dés le début
        """
        super().__init__(*sprites)

        # ========= CONSTANTES ==========
        self.DISPLAY_SURFACE = displaySurface

        self.SCREEN_SIZE = (self.DISPLAY_SURFACE.get_size())

        # ========= VARIABLES ==========
        self.listSprites = []
        self.spriteActual = [] 

        self.startX = 0
        self.startY = 0

        self.intervalle = (0, 1)

        self.move = True

    
    def loadTest(self, n=20, intervalleX = (-1000,1000), intervalleY = (0,2000)):
        """
        Méthode pour tester le déplacement de la caméra avec des arbres
        n           -- nomber d'élément dans la fenètre
        intervalleX -- intervalle de l'aléatoire pour défénir les coordonnées X
        intervalleY -- intervalle de l'aléatoire pour défénir les coordonnées Y
        """

        for _ in range(n):
            self.listSprites.append(RandomObject(self,intervalleX,intervalleY))

        self.listSprites.sort(key= lambda sprite : sprite.x) # trie la list en fonction deX

    def loadGame(self, listSprites):
        """
        Met en mémoire la liste des objets et les trie suivant les x : prépare la caméra
        listSprites  -- une liste de sprites où ils doivent contenir des coorodonnées x et y
        
        """

        self.listSprites = listSprites

        self.listSprites.sort(key= lambda sprite : sprite.x) # trie la list en fonction deX
        
    def partWorld(self):
        """
        Retroune la liste des objets qui peuvent être visible par le joueur. On utilise une recherche Dichotomie pour trouver l'encadrement
        
        """
        start_i = self.binarySearch(self.listSprites, -self.startX - 150 , key = lambda sprite : sprite.x)
        end_i = self.binarySearch(self.listSprites, -self.startX + 100 + self.SCREEN_SIZE[0], key = lambda sprite : sprite.x)

        self.intervalle = ( start_i ,end_i)
        
        return self.listSprites[start_i : end_i] 

    def getSpriteActual(self):
        return self.spriteActual


    def updateDisplay(self):
        """
        Met à jour la caméra en replaçant les objets (seulement eux visibles)
        """

        self.spriteActual = []
        

        # if self.cameraMove:

        for sprite in self.partWorld():
                
            # self.DISPLAY_SURFACE.blit(sprite.image, (sprite.x + self.startX, sprite.y + self.startY))
            # pygame.draw.rect(screen,(100+i*11,255-20*i,255 - i*10),liste_bloc[i])
            rect = pygame.Rect(sprite.x + self.startX,  sprite.y+ self.startY, sprite.width, sprite.height)
            pygame.draw.rect(self.DISPLAY_SURFACE,(100,1,100),rect)

            self.spriteActual.append(rect)
        # else:
            
        #     for sprite in self.getSpriteActual():
        #         rect = pygame.Rect(sprite.x,  sprite.y, 100, 200)
        #         pygame.draw.rect(self.DISPLAY_SURFACE,(100,1,100),rect)

        #         self.spriteActual.append(rect)


                
                
        self.update()


    def go_Left(self, n = 2):
        """
        Ajoute n à la varialbe START_X
        n -- le nombre ajouté
        """
        if self.move:
            self.startX += n

    def go_Right(self, n = 2):
        """
        Ajoute n à la varialbe START_X : pour déplacer les éléments vers la gauche
        n -- le nombre ajouté
        """
        if self.move:
            self.startX -= n

    def go_Top(self, n = 2):
        """
        Ajoute n à la varialbe START_Y  : pour déplacer les éléments vers la bas
        n -- le nombre ajouté
        """
        if self.move:
            self.startY += n

    def go_Bottom(self, n = 2):
        """
        Soustrait n à la varialbe START_Y  : pour déplacer les éléments vers la haut
        n -- le nombre ajouté
        """
        if self.move:
            self.startY -= n


    def binarySearch (self, tableau, valeur, key=lambda x : x):
        """
        Renvoie l'indice de "valeur" ou une valeur vers où la valeur devrai se trouver si celle-ci n'a pas été trouvée

        Paramètres :
        tableau -- tableau trié dans lequel effectuer la recherche
        valeur  -- valeur recherchée
        """

        indice_debut = 0
        indice_fin = len(tableau) - 1

        while indice_debut <= indice_fin:
            indice_milieu = (indice_debut + indice_fin) // 2

            valueFound = key(tableau[indice_milieu])

            if valueFound == valeur:
                return indice_milieu
            elif valueFound > valeur:
                indice_fin = indice_milieu - 1
            else:
                indice_debut = indice_milieu + 1
        return indice_milieu

    def toggleCameraMove(self):
        """
        Permet de passer du mode caméra qui bouge au mode qui de la caméra qui ne bouge pas et inversement
        """

        if self.move:
            self.move = False
        else:
            self.move = True
