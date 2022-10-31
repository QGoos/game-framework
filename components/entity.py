from re import X
import pygame
from abc import ABC, abstractmethod

HEIGHT_MODIFIER = 225

class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y,  width, height, group) -> None:
        super().__init__(group)
        self.x = x
        self.y = y
        self.z = 0
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width,self.height])
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)#self.image.get_rect()
        self.hitbox = self.rect


    def getRectCorner(self):
        return self.rect.topleft

    def collisionRect(self) -> pygame.Rect:
        return self.hitbox #self.rect

    def setHitbox(self,width,height) -> None:
        self.hitbox = pygame.Rect(self.rect.x + (self.width//2) - (width//2), self.rect.y + self.height - height, width, height)
    
    def centerY(self) -> int:
        return self.rect.centery

    def colWidth(self) -> int:
        return self.width//2

    def getRect(self) -> pygame.Rect:
        return self.rect

    def getImage(self) -> pygame.Surface:
        '''return the visuals for the Entity'''
        return self.image

    def getWidth(self) -> int:
        return self.width

    def getHeight(self) -> int:
        return self.height
    
    def getX(self) -> int:
        return self.rect.x

    def increaseX(self, x) -> None:
        self.x += x

    def getY(self) -> int:
        return self.rect.y
    
    def increaseY(self, y) -> None:
        self.y += y

    def getZ(self) -> int:
        return self.z*HEIGHT_MODIFIER

    def increaseZ(self, z) -> None:
        self.z = min(self.z+z, 2)

    def decreaseZ(self,z) -> None:
        self.z = max(self.z-z, 0)
    
    def getImage(self) -> pygame.Surface:
        return self.image

    def isOnscreen(self, screen) -> bool:
        return self.rect.colliderect(screen.get_rect())