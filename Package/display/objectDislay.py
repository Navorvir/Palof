class BasicDisplay(object):

    def __init__(self,name :str, x :int | float, y:int|float, width:int|float, height: int |float, pathImage : str = None,
                  color : tuple= (234,215,157)) -> None:
        
        self.COLOR : tuple(int,int,int)= color
        self.WIDTH : int = width
        self.HEIGHT : int = height
        self.NAME = name
        self.IMAGE = pathImage

        self.x = x
        self.y = y

        self.displayChange = True
        self.index = None