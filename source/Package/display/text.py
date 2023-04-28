import pygame
from Package.display.objectDislay import BasicDisplay
 
class Text(BasicDisplay):
    def __init__(self,name :str, x :int | float, y:int|float, width:int|float, height: int |float,text : str, color : tuple=(0,0,0)) -> None:
        """_summary_

        Args:
             name (str): nom pour retrouver texte
            x (int | float): coordonnée x de l'objet texte
            y (int | float): coordonnée y de l'objet texte
            width (int | float): largeur de l'objet texte
            height (int | float): hauteur de l'objet texte
            text (str): texte dans l'objet qui s'affiche
            color (tuple, optional): _description_. Defaults to (0,0,0).
        """
        # par Nathan

        super().__init__(name,x,y,width, height)

        self.FONT : pygame.font.Font = pygame.font.Font("Assets/sigmar.ttf", 40)
        self.FONT_COLOR : tuple(int,int,int) = color

        self.listObject : list = []

        self.text : str = text
        self.lastText : str = None


    def setText(self, text : str = None) -> None:
        """Changer le texte de l'objet

        Args:
            text (str, optional): nouveau texte dans l'affichage. Defaults to None.
        """
        # par Nathan

        if text != None:
            self.text = text 

        if self.lastText != self.text:
            
            self.textRender = self.FONT.render(self.text, True, self.FONT_COLOR)
            self.rectRender = self.textRender.get_rect(topleft=(self.x, self.y))

            self.textObject= {"x":self.x, "y":self.y, "rect":self.rectRender, "image":self.textRender, "object" : self}

            self.listObject = [self.textObject]
            self.lastText = self.text
            self.displayChange = True
        else:
            self.displayChange = False

