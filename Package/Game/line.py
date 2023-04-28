import pygame

class Line():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.lineRect = pygame.Rect(x,y,50,100)
        
    def IsCrossed(self, PALOURDE):
        if self.lineRect.collidepoint(PALOURDE):
            return True
        return False