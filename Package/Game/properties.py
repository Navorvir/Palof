class Base(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.WIDTH = width
        self.HEIGHT = height

class Dynamic(object):
    """
    Lois de Physique
    
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.WIDTH = width
        self.HEIGHT = height
        
class Entity(Base, Dynamic):
    def __init__(self, x, y, width, height):
        super(Base, self).__init__(x, y, width, height)
        super(Dynamic, self).__init__()
