import pygame

# par Robin


class Line():
    """Objet qui représente la Ligne d'arrivée 
    """

    def __init__(self, x: int | float, y: int | float) -> None:
        """Initilise l'objet Line

        Args:
            x (int | float): coordonnée x où la ligne d'arrivée se place
            y (int | float): coordonnée y où la ligne d'arrivée se place
        """
        self.x = x
        self.y = y
        self.lineRect = pygame.Rect(x, y, 50, 100)

    def IsCrossed(self, PALOURDE) -> bool:
        """Verifie si la ligne est traversée

        Args:
            PALOURDE (Palourde): test si l'objet Palourde a traversé

        Returns:
            bool: si il a traversé True sinon False
        """
        if self.lineRect.collidepoint(PALOURDE):
            return True
        return False