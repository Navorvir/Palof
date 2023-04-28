import json
import pygame
from Package.display.button import Button
from Package.display.text import Text
from Package.display.input import Input
from Package.display.arriver import Arrivee

class Map():
    
    def __init__(self, width : int = 1280, height : int = 720):
        self.layer0 = []
        self.layer1 = []
        self.layer2 = []
        self.listObject = [self.layer0, self.layer1, self.layer2]
        self.listObjectInstancies : dict = {"button":{},"input":{},"text":{}}

        self.SCREEN_WIDTH : int = width
        self.SCREEN_HEIGHT : int = height  
        
    def traitement(self, directory):
        # par Nathan et Lucie
        with open(directory) as file:
            self.data = json.load(file)
            self.imagePath = self.data["header"]["imagePath"]

            if "lockCamera" in self.data["header"]:
                self.lockCamera = self.data["header"]
            else:
                self.lockCamera = False
            if "spawnCoordonate" in self.data["header"]:
                self.spawnCoordonate = self.data["header"]["spawnCoordonate"]
            else:
                self.spawnCoordonate = {"x": 0, "y":"current"}

        
            for i in range(len(self.data["listeObject"])):
                object = self.data["listeObject"][i]

                object["x"] = self.tranformX(object["x"], object["width"])
                object["y"] = self.tranformY(object["y"], object["height"])

                self.sprite = {"x":object["x"], "y":object["y"]}
                
                if "x" in object and "y" in object:
                    
                    if "image" not in object and "color" not in object:
                        object["color"] = "black"
                                    
           
                    # Si c'est une image
                    if "image" in object:
                        if object["image"] in self.data["header"]["images"]:
                            self.image = pygame.image.load(self.imagePath + self.data["header"]["images"][object["image"]])
                        
                    elif "text" not in object :
                        self.sprite["color"] = object["color"]
                        self.image = pygame.Surface((object["width"],object["height"]))
                        self.image.fill(object["color"])
                    else:
                        self.image = pygame.Surface((object["width"],object["height"]))
                            
                    if "angle" in object:
                        self.image = pygame.transform.rotate(self.image, object["angle"])
                            
                    self.rect = self.image.get_rect(topleft = (object["x"], object["y"]))
                    
                    self.sprite["image"] = self.image
                    self.sprite["rect"] = self.rect

                    if "type" in object:
                        self.object_Instancy(object["type"], object)                                                       
                        
                    if "layer" not in object:
                        object["layer"] = 1                
                    
                    if "type" not in object:
                        self.listObject[object["layer"]].append(self.sprite)
                    
    def object_Instancy(self, type, object):
        # par Nathan et Lucie
        objectInstancy = None

        if type == "button":
            if "command" not in object:
                object["command"] = None
            if "args" not in object:
                object["args"] = None
            objectInstancy = Button(object["name"], object["x"], object["y"],object["width"],object["height"],self.image, object["command"], object["args"])

        elif type == "text" :
            objectInstancy = Text(object["name"],object["x"], object["y"],object["width"],object["height"], object["text"], color=object["color"])
        elif type=="input":
            objectInstancy = Input(object["name"],object["x"], object["y"],object["width"],object["height"], pathImage= self.image, command=object["command"])
        elif type == "ligneArrivee":
            objectInstancy = Arrivee(object["x"],object["y"],object["width"],object["height"])

        if type not in self.listObjectInstancies:
            self.listObjectInstancies[type] = {}
        
        if objectInstancy != None:
            self.listObjectInstancies[type][objectInstancy.NAME] = objectInstancy
        else:
            print(type, object)
        
    def get_ObjectInstancies(self):
        
        return self.listObjectInstancies       
    

    def tranformX(self, x : str | int |float | list, width : int|float) -> int | float:
        # par Nathan
        xTotal = 0
        if type(x) != list:
            x = [x]

        for n in x:
            if n == "center":
                xTotal += (self.SCREEN_WIDTH - width) // 2
            elif n == "right":
                xTotal += self.SCREEN_WIDTH - width
            elif n == "left":
                xTotal += 0
            else:
                xTotal += n
            
        return xTotal
    
    def tranformY(self, y : str | int |float | list, height : int|float) -> int | float:
        # par Nathan
        yTotal = 0
        if type(y) != list:
            y = [y]
        
        for n in y:
            if n == "center":
                yTotal += (self.SCREEN_HEIGHT - height) // 2
            elif n == "bottom":
                yTotal += self.SCREEN_HEIGHT - height
            elif n == "top":
                yTotal += 0
            else:
                yTotal += n
            
        return yTotal
