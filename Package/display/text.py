import pygame
from Package.display.objectDislay import BasicDisplay
 
class Text(BasicDisplay):
    def __init__(self,name,x,y,width, height,text, color=(0,0,0)):
        super().__init__(name,x,y,width, height)

        self.FONT = pygame.font.Font("Assets/sigmar.ttf", 40)
        self.FONT_COLOR : tuple(int,int,int) = color

        self.listObject = []

        self.text = text
        self.lastText = None
        # self.setText()


    def setText(self, text : str = None):
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

