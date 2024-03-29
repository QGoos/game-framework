import pygame
from components import entity

class BackgroundBlock(entity.Entity):
    def __init__(self, x, y, size, type_value, group) -> None:
        super().__init__(x, y, size, size, group)
        self.group = None
        self.z = -1
        self.bg_value = type_value
        self.image = pygame.image.load(f'./components/graphics/{self.get_background_type(self.bg_value)}.png').convert()
    
    def set_default_chunk_image(self):
        self.image = pygame.image.load(f'./components/graphics/{self.get_background_type(self.bg_value)}_chunk_default.png').convert()

    def get_background_type(self, value):
        values = ['grass2','ice','water','sand','rock']
        return values[value]

class Tree(entity.Entity):
    def __init__(self, x, y, width, height, group) -> None:
        super().__init__(x, y, width, height, group)
        self.group = group
        self.z = 1
        self.image.fill((29, 110, 39))
        self.trunk = None

    def getImage(self) -> None:
        return self.image

    def getTrunk(self) -> pygame.Surface:
        '''generate a corresponding trunk to the tree'''
        if(not self.trunk):
            trunk_width = self.width//4
            trunk_height = self.height*3//4
            trunk_x = self.x + (self.width//2) - trunk_width//2
            trunk_y = self.y + self.height

            self.trunk = Trunk(trunk_x,trunk_y,trunk_width,trunk_height,self.group)

        return self.trunk

class Trunk(entity.Entity):
    def __init__(self, x, y, width, height, group) -> None:
        super().__init__(x, y, width, height, group)
        self.image.fill((61,39,21))
        self.setHitbox(width,height//3)

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

class Rock(entity.Entity):
    def __init__(self, x, y, width, height, group) -> None:
        super().__init__(x, y, width, height, group)
        self.image.fill((127,127,127))

