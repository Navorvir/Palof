from properties import Entity

class Item(Entity):
    def __init__(self, x, y, width, height):
        super(Entity).__init__()

class Consumable(Item):
    def __init__(self, x, y, width, height):
        super(Item).__init__()

class Tool(Item):
    def __init__(self, x, y, width, height):
        super(Item).__init__()