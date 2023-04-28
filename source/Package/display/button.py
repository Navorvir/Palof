import pygame
from Package.display.objectDislay import BasicDisplay

class Button(BasicDisplay) :

    def __init__(self,name, x, y, width, height, image,command : str, arguments : tuple |list = None):
        super().__init__(name,x,y,width, height, pathImage=image)
        self.x = x
        self.y = y
        self.height = pygame.Surface.get_height(self.IMAGE)
        self.width = pygame.Surface.get_width(self.IMAGE)
        self.bouton_rect = pygame.Rect(self.x,self.y,self.width, self.height)
        self.command = command
        self.directCommand = False

        self.buttonObject= {"x":self.x, "y":self.y, "rect":self.bouton_rect, "image":self.IMAGE, "object" : self}

        self.arguments = arguments

        self.listObject = [self.buttonObject]
        
    def pressed(self):
        # par Lucie
        if self.bouton_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == True:
                return True
            return False
        
    def setCommand(self, command):
        # par Nathan
        self.command = command
        self.directCommand = True
