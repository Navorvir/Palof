class BasicDisplay(object):
    """Objet de base qui possède des caractéristiques pour interagir avec le sytème d'affichage
    """

    # par Nathan

    def __init__(self, name: str, x: int | float, y: int | float, width: int | float, height: int | float, pathImage: str = None,
                 color: tuple = (234, 215, 157)) -> None:
        """Méthode qui initailise les valeurs nécessaires

        Args:
            name (str): nom pour retrouver l'objet
            x (int | float): coordonnée x de l'objet
            y (int | float): coordonnée y de l'objet
            width (int | float): largeur de l'objet
            height (int | float): hauteur de l'objet
            pathImage (str, optional): surface de l'image ou chemin de l'image. Defaults to None.
            color (tuple, optional): couleur de l'élément(si vous avez une image, elle prend le dessus sur la couleur). Defaults to (234,215,157).
        """

        self.COLOR: tuple(int, int, int) = color
        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.NAME: str = name
        self.IMAGE = pathImage

        self.x: int | float = x
        self.y: int | float = y

        self.displayChange: bool = True
        self.index: int = None
