import json
import pygame

class Map():
    
    def __init__(self):
        self.layer0 = []
        self.layer1 = []
        self.layer2 = []
        self.listObject = [self.layer0, self.layer1, self.layer2]
        
        
        
    def traitement(self, directory):
        
        with open(directory) as file:
            self.data = json.load(file)
            self.imagePath = self.data["header"]["imagePath"]
        
            for object in self.data["listeObject"]:
                self.sprite = {"x":object["x"], "y":object["y"]}
                
                if "x" in object and "y" in object:
                    
                    if "image" not in object and "color" not in object:
                        object["color"] = "black"
                        
                    
                    if "image" in object:
                        if object["image"] in self.data["header"]["images"]:
                            self.image = pygame.image.load(self.imagePath + self.data["header"]["images"][object["image"]])
                        
                    else :
                        self.sprite["color"] = object["color"]
                        self.image = pygame.Surface((object["width"],object["height"]))
                        self.image.fill(object["color"])
                            
                    #if "angle" in object:
                    #    self.image = pygame.transform.rotate(self.image, object["angle"])
                            
                    self.rect = self.image.get_rect(topleft = (object["x"], object["y"]))
                    
                        
                    self.sprite["image"] = self.image
                    self.sprite["rect"] = self.rect
                                                                                    
                        
                    if "layer" not in object:
                        self.object["layer"] = 1                
                    
                
                    self.listObject[object["layer"]].append(self.sprite)
                    
                    
                        
                
                
                