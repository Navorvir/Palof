from properties import Base, Dynamic


class StructureStatic(Base):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

class StructureDynamic(StructureStatic, Dynamic):
    def __init__(self, x, y, width, height):

        super(StructureStatic, self).__init__( x, y, width, height)
        super(Dynamic, self).__init__()
