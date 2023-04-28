import pygame
from Package.display.objectDislay import BasicDisplay
from Package.display.text import Text
 
class Input(Text):
    """Objet qui permet de créer un champ de texte pour récupérer les valeurs saisies des valeurs entre 0 et 9 et de "a" à "z"
    """

    def __init_(self, name:  str, x: int | float, y: int | float, width: int | float, height: int | float, pathImage : str, command, maxChar : int =10):
        """_summary_

        Args:
            name (str): nom pour retrouver l'objet Input
            x (int | float): coordonnée x de l'objet Input
            y (int | float): coordonnée y de l'objet Input
            width (int | float): largeur de l'objet In Inputput
            height (int | float): hauteur de l'objet
            pathImage (str): chemin vers l'image
            command (): case de mémoire de la méthode ou nom pour le gestionnaire de boutons dans menu
            maxChar (int, optional): le nombre de caractères maximums dans le champ de texte. Defaults to 10.
        """
        super().__init__(name,x+x-maxChar*10,y-10,width, height, "")

        self.IMAGE : str = pathImage
        
        self.MAX_CHAR : int = maxChar        
        

        self.prompt = self.FONT.render("",True, self.FONT_COLOR)
        self.promptRect = self.prompt.get_rect(center = (self.x,self.y))

        self.listObject = []
        self.command = command

        
        self.textRender= None
        self.rectRender = None

        self.setText()

        self.isSend = False

        self.windowsImage = pygame.Surface((self.WIDTH,self.HEIGHT))

        if self.IMAGE != None:
            self.windowsImage .blit(self.IMAGE,(0,0))
        else:
            self.windowsImage.fill(self.COLOR)

        self.windowsRect = self.windowsImage.get_rect(center = (self.x+self.MAX_CHAR*14,self.y+30))
  
        self.update()
      
    def setCommand(self, command):
        """Mettre en place une nouvelle méthode ou fonction

        Args:
            command ( méthode ou fonction): est exécuter lorsqu'on fait entré
        """
        self.command = command
     
        
    def click(self):
        if len(self.text) <= self.MAX_CHAR:
            self.text = self.getUnicode(self.text)
            self.command(self.text)

    def getUnicode(self, text:str) -> str:
        result = ""
        for l in text:
            if ord("0") <= ord(l) <= ord("9") or  ord("a") <= ord(l) <= ord("z"):
                result += l
        return result

        
    def update(self):
        if len(self.text) > self.MAX_CHAR:
            self.text = self.text[:self.MAX_CHAR]

        self.setText()

        if self.displayChange:
            self.display()
        
            if self.isSend == True :
                self.code = self.text
                self.text = ""
                self.isSend = False
        
    def display(self):
        self.windowsObject = {"x":self.x, "y":self.y,"image":self.windowsImage,"rect":self.windowsRect}
        self.textObject= {"x":self.x, "y":self.y, "rect":self.rectRender, "image":self.textRender, "object" : self}

        self.rectRender = self.textRender.get_rect(topleft=self.promptRect.topright)
        self.listObject = [self.windowsObject, self.textObject]

        
    def getUserInput(self):
        return self.text
 