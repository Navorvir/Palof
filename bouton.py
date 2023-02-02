import pygame

class bouton :

    def __init__(self, x, y, surface, image):
        self.x = x
        self.y = y
        self.image = image
        self.surface = surface
        self.height = pygame.Surface.get_height(self.image)
        self.width = pygame.Surface.get_width(self.image)
        self.bouton_rect = pygame.Rect(self.x,self.y,self.width, self.height)

    def draw (self):
        self.surface.blit(self.image, self.bouton_rect)
        
    def pressed(self):
        if self.bouton_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == True:
                return True
            return False