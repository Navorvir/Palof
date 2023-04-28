import pygame
from Package.display.objectDislay import BasicDisplay


class Button(BasicDisplay):
    """Objet permettant de créer un bouton dans un environement pygame. De plus cet objet active une méthode à son clique
    """

    def __init__(self, name:  str, x: int | float, y: int | float, width: int | float, height: int | float, image: pygame.Surface, command: str, arguments: tuple | list = None) -> None:
        """Méthode d'initialisation de l'objet Bouton 

        Args:
            name (str): nom pour retrouver l'objet
            x (int | float): coordonnée x du bouton
            y (int | float): coordonnée y du bouton
            width (int | float): largeur du bouton
            height (int | float): hauteur du bouton
            image (pygame.Surface): surface qui contient l'image
            command (): case de mémoire de la méthode ou nom pour le gestionnaire de boutons dans menu
            arguments (tuple | list, optional): ajouter des arguments à la méthode (command). Defaults to None.
        """
        super().__init__(name, x, y, width, height, pathImage=image)

        self.x: int | float = x
        self.y: int | float = y
        self.height: int | float = pygame.Surface.get_height(self.IMAGE)
        self.width: int | float = pygame.Surface.get_width(self.IMAGE)
        self.bouton_rect: pygame.Rect = pygame.Rect(
            self.x, self.y, self.width, self.height)
        self.command = command

        self.directCommand: bool = False

        self.buttonObject: dict = {
            "x": self.x, "y": self.y, "rect": self.bouton_rect, "image": self.IMAGE, "object": self}

        self.arguments: tuple | list = arguments

        self.listObject: list = [self.buttonObject]

    def pressed(self) -> bool:
        """Vérifie si le joueur a cliqué sur le bouto,

        Returns:
            bool: si le bouton a été cliqué True sinon False
        """

        # par Lucie
        if self.bouton_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == True:
                return True
            return False

    def setCommand(self, command) -> None:
        """Mettre en place une méthode ou une fonction qui s'exécute lors du clique

        Args:
            command (fonction, méthode): fonction ou méthode qui devra s'exécuter lors du clique
        """

        # par Nathan
        self.command = command
        self.directCommand = True
