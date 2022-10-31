import pygame
from components import entity

class BackgroundBlock(entity.Entity):
    def __init__(self, x, y, width, height, group) -> None:
        super().__init__(x, y, width, height, group)
        self.group = None
        self.z = -1
        self.image = pygame.image.load('./components/graphics/grass.png')#.fill((181,230,29))

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
        if(not self.trunk):
            trunk_width = 4
            trunk_height = 24
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

