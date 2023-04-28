import pygame
from Package.display.objectDislay import BasicDisplay
from Package.display.text import Text
 
class Input(Text):
    def __init__(self,name,x,y,width, height,pathImage, command, maxChar : int =10):
        super().__init__(name,x+x-maxChar*10,y-10,width, height, "")

        self.IMAGE = pathImage
        
        self.MAX_CHAR = maxChar        
        

        self.prompt = self.FONT.render("",True, self.FONT_COLOR)
        self.promptRect = self.prompt.get_rect(center = (self.x,self.y))

        self.listObject = []
        self.command = command

        
        self.textRender = None
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
 