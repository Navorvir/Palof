import pygame


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

        self.MAX_SIZE_OBJECT = 1000

        # ========= VARIABLES ==========
        self.listSprites = []
        self.spriteActual = [] 

        self.listSpritesChange = {}
        self.indexSpriteChange = 0 # de la fin vers le debut

        self.startX = 0
        self.startY = 0
        
        self.intervalle = (0, 1)

        self.lock = True

    def loadGame(self, listSprites):
        """
        Met en mémoire la liste des objets et les trie suivant les x : prépare la caméra
        listSprites  -- une liste de sprites où ils doivent contenir des coorodonnées x et y
        
        """
        self.listSpritesChange = {}
        self.listSprites = listSprites
        for i in range(len(listSprites)):
            self.listSprites[i].sort(key= lambda sprite : sprite["x"]) # trie la list en fonction deX

    def partWorld(self):
        """
        Retroune la liste des objets qui peuvent être visible par le joueur. On utilise une recherche dichotomique pour trouver l'encadrement
        
        """
        localSprite = []
        start_i = 0
        end_i = 0
        
        for i in range(len(self.listSprites)):
            start_i = self.binarySearch(self.listSprites[i], -self.startX - self.MAX_SIZE_OBJECT , key = lambda sprite : sprite["x"])
            end_i = self.binarySearch(self.listSprites[i], -self.startX + self.MAX_SIZE_OBJECT + self.SCREEN_SIZE[0], key = lambda sprite : sprite["x"])
            localSprite.append (self.listSprites[i][start_i : end_i+1])
            
        self.intervalle = ( start_i ,end_i)
        
        return localSprite

    def getSpriteActual(self):
        return self.spriteActual

    def appendPalourde(self,listRectColision:list):
        for rect in listRectColision:
            self.spriteActual.append(rect)
        


    def updateDisplay(self, PALOURDE):
        """
        Met à jour la caméra en replaçant les objets (seulement eux visibles)
        """
        self.spriteActual = []
        # if len(self.listSprites) > 0:
        #     self.listSprites = self.listSprites[0][:len(self.listSprites[0])-self.indexSpriteChange] # supprime les éléments qui change


        # Les élément qui peuvent changer d'etat
        for keySprite, object in self.listSpritesChange.items():
            if object.displayChange:
                
                # Si l'objet est nouveau
                if object.index == None:
                    object.index = len(self.listSprites[1]) 
                    for sprite in object.listObject:
                        self.listSprites[1].append(sprite)

                else:
                    i = 0
                    for sprite in object.listObject:
                        index = object.index + i
                        self.listSprites[1][index] = sprite
                        i += 1



        listSprite = self.partWorld()


        for layer in listSprite:
            for keySprite in layer:                
                self.DISPLAY_SURFACE.blit(keySprite["image"], (keySprite["rect"].x + self.startX, keySprite["rect"].y + self.startY))

                if layer == listSprite[1]:
                    rect = pygame.Rect(keySprite["rect"].x + self.startX,  keySprite["rect"].y+ self.startY, keySprite["rect"].width, keySprite["rect"].height)
                    self.spriteActual.append(rect)
                

        self.update()

    def moveCamera(self, x, y):
        """
        Ajoute n à la varialbe START_X
        n -- le nombre ajouté
        """
        if not self.lock:
            self.startX = -x
            self.startY = -y


    def binarySearch (self, tableau, valeur, key=lambda x : x):
        """
        Renvoie l'indice de "valeur" ou une valeur vers où la valeur devrai se trouver si celle-ci n'a pas été trouvée

        Paramètres :
        tableau -- tableau trié dans lequel effectuer la recherche
        valeur  -- valeur recherchée
        """

        indice_debut = 0
        indice_fin = len(tableau) - 1
        indice_milieu = (indice_debut + indice_fin) // 2

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

    def lockCamera(self):
        """
        Permet de passer du mode caméra que la camera ne bouge pas
        """

        self.lock = True

    def unlockCamera(self):
        """
        Permet de passer du mode caméra qui bouge
        """
         
        self.lock = False