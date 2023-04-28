import pygame

class Arrivee():
    def __init__(self,x,y,width,height):
        # Créé par Robin
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zoneArrivee = pygame.Rect(self.x,self.y,self.width,self.height)

        self.NAME = "ligneArrivee"

    def verification(self,listePalourde,x : float,y : float) -> bool:
        """summary
        Renvoie un tuple possédant de coodonnées par rapport au centre de la palourde, un angle et un rayon donné

        Args:
            listePalourde (array): Liste des objets palourdes de chaque joueur
            x (float): La coordonnée x de la caméra
            y (float): rLa coordonnée y de la caméra
        """
        # Créé par Robin

        self.zoneArrivee = pygame.Rect(self.x - x,self.y - y,self.width,self.height)
        nb_bon = 0
        for i in range(len(listePalourde)):
            dedans = False
            #On fait un traitement différent pour chaque type de palourde car elles possèdent chaqune un type de collision différent
            #La palourde du joueur se trouve forcément à l'indice 0 de la liste et est aussi forcément unique
            if i == 0:
                if abs(self.x - x) < 2000:
                    for point in  listePalourde[i].listePoint:
                        if self.zoneArrivee.collidepoint(point):
                            dedans = True
            else:
                for rectPalourde in listePalourde[i].rect:
                    if pygame.Rect.colliderect(rectPalourde, self.zoneArrivee):
                        dedans = True
            if dedans == True :
                nb_bon += 1
            else:
                return False

        if nb_bon == len(listePalourde):
            print("finit !!!!!!!!")
            return True
        return False