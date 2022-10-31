from abc import ABC, abstractmethod
from pygame.math import Vector2 as vec
import pygame

class Camera:
    def __init__(self, player, screen_width, screen_height)  -> None:
        self.player = player
        self.offset = vec(0,0)
        self.offset_float = vec(0,0)
        self.SCREEN_W, self.SCREEN_H = screen_width, screen_height
        self.CONST = vec(-self.SCREEN_W//2 + player.getWidth()//2, -self.SCREEN_H//2 + self.player.getHeight()//2)

    def setMethod(self, method) -> None:
        self.method = method

    def scroll(self) -> None:
        self.method.scroll()

class CamScroll(ABC):
    def __init__(self, camera, player) -> None:
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera, player) -> None:
        super().__init__(camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.getX() - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.getY() - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

class Camera2(pygame.sprite.Group):
    def __init__(self, screen) -> None:
        super().__init__()
        self.screen = screen
        self.half_w = screen.get_size()[0] // 2
        self.half_h = screen.get_size()[1] // 2

        # camera offset
        self.offset = pygame.math.Vector2()

        # zoom control
        self.zoom_scale = 1.25
        self.internal_surface_size = (32*32,32*32*0.75)#tile size in px x number of tiles on screen (in a row/col)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_w,self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)

        # zoomed camera offset
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_h

        #camera rotation (does nothing)
        self.internal_rotation = 45
        self.rotation_offset = pygame.math.Vector2()
        self.rotation_offset.x = 0
        self.rotation_offset.y = 0
    
    def set_zoom_scale(self, scale) -> None:
        self.zoom_scale = max(min(1.75,self.zoom_scale + scale), 1)

    def set_rotation(self, x):
        self.internal_rotation = (self.internal_rotation + x) % 360

    def get_rotation_offset(self):
        return self.rotation_offset

    def center_target(self, entity):
        self.offset.x = entity.getRect().centerx - self.half_w
        self.offset.y = entity.getRect().centery - self.half_h

    def get_camera_x(self):
        return self.offset.x + self.internal_offset.x

    def get_camera_y(self):
        return self.offset.y + self.internal_offset.y

    def draw(self, entities, target):

        self.center_target(target)

        for entity in sorted(entities, key = lambda entity: entity.centerY() + entity.getZ()):
            offset_pos = entity.getRectCorner() - self.offset + self.internal_offset
            #print(entity.getRectCorner(),entity.getX(),entity.getY())
            #self.screen.blit(entity.getImage(), offset_pos)
            self.internal_surface.blit(entity.getImage(), offset_pos)

        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        if self.screen.get_size() > scaled_surface.get_size():
            scaled_surface = pygame.transform.scale(scaled_surface, self.screen.get_size())
        scaled_rect = scaled_surface.get_rect(center = (self.half_w, self.half_h))
        
        self.screen.blit(scaled_surface,scaled_rect)

    def draw_background(self, entities, target):

        self.center_target(target)

        for entity in entities:
            offset_pos = entity.getRectCorner() - self.offset + self.internal_offset
            #print(entity.getRectCorner(),entity.getX(),entity.getY())
            #self.screen.blit(entity.getImage(), offset_pos)
            self.internal_surface.blit(entity.getImage(), offset_pos)

        # scale the surface with the drawings to the appropriate size
        scaled_surface = pygame.transform.scale(self.internal_surface,self.internal_surface_size_vector * self.zoom_scale)
        # if the surface is smaller than the window, make it fit the screen
        if self.screen.get_size() > scaled_surface.get_size():
            scaled_surface = pygame.transform.scale(scaled_surface, self.screen.get_size())
        scaled_rect = scaled_surface.get_rect(center = (self.half_w,self.half_h))

        #scaled_rect = scaled_surface.get_rect(center = (self.half_w,self.half_h))
        self.screen.blit(scaled_surface,scaled_rect)
