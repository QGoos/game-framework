from abc import ABC, abstractmethod
from pygame.math import Vector2 as vec
import pygame

class Camera(pygame.sprite.Group):
    def __init__(self, screen, tilesize) -> None:
        super().__init__()
        self.screen = screen
        self.half_w = screen.get_size()[0] // 2
        self.half_h = screen.get_size()[1] // 2
        self.tile_size = tilesize

        # camera offset
        self.offset = pygame.math.Vector2()

        # zoom control
        self.zoom_scale = 1.25
        self.internal_surface_size = (self.tile_size*32,self.tile_size*32*0.75)#tile size in px x number of tiles on screen (in a row/col)
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
        '''draw entities that need to be sorted'''

        self.center_target(target)

        # sort by y axis, account for height
        for entity in sorted(entities, key = lambda entity: entity.centerY() + entity.getZ()):
            offset_pos = entity.getRectCorner() - self.offset + self.internal_offset
            self.internal_surface.blit(entity.getImage(), offset_pos)

        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        #if self.screen.get_size() >= scaled_surface.get_size():
            #scaled_surface = pygame.transform.scale(scaled_surface, self.screen.get_size())
        scaled_rect = scaled_surface.get_rect(center = (self.half_w, self.half_h))
        
        self.screen.blit(scaled_surface,scaled_rect)

    def draw_background(self, entities, target):
        '''draw background seperately to avoid sorting'''
        self.center_target(target)
        self.internal_surface.fill((255,255,255))
        self.screen.fill((255,255,255))

        for entity in entities:
            offset_pos = entity.getRectCorner() - self.offset + self.internal_offset
            self.internal_surface.blit(entity.getImage(), offset_pos)

        # scale the surface with the drawings to the appropriate size
        #scaled_surface = pygame.transform.scale(self.internal_surface,self.internal_surface_size_vector * self.zoom_scale)
        # if the surface is smaller than the window, make it fit the screen
        #if self.screen.get_size() >= scaled_surface.get_size():
            #scaled_surface = pygame.transform.scale(scaled_surface, self.screen.get_size())
        #scaled_rect = scaled_surface.get_rect(center = (self.half_w,self.half_h))

        #scaled_rect = scaled_surface.get_rect(center = (self.half_w,self.half_h))
        #self.screen.blit(scaled_surface,scaled_rect)

class Camera2(pygame.sprite.Group):
    def __init__(self, screen, tilesize) -> None:
        super().__init__()
        self.screen = screen
        self.half_w = screen.get_size()[0] // 2
        self.half_h = screen.get_size()[1] // 2
        self.tile_size = tilesize

        self.offset = pygame.math.Vector2()

        self.blocks_on_width = 32
        self.blocks_on_height = self.blocks_on_width*0.75
        self.internal_screen_size = (tilesize*self.blocks_on_width, tilesize*self.blocks_on_height)
        self.half_w_2 = self.internal_screen_size[0] // 2
        self.half_h_2 = self.internal_screen_size[1] // 2
        self.internal_screen = pygame.Surface(self.internal_screen_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_screen.get_rect(center = (self.half_w,self.half_h))
        self.internal_screen_size_vector = pygame.math.Vector2(self.internal_screen_size)

    def center_target(self, entity):
        self.offset.x = entity.getRect().centerx - self.half_w_2
        self.offset.y = entity.getRect().centery - self.half_h_2

    def get_camera_x(self):
        return self.offset.x# + self.internal_offset.x

    def get_camera_y(self):
        return self.offset.y# + self.internal_offset.y
    
    def draw(self, entities, target):
        self.center_target(target)

        # sort by y axis, account for height
        for entity in sorted(entities, key = lambda entity: entity.centerY() + entity.getZ()):
            offset_pos = entity.getRectCorner() - self.offset
            self.internal_screen.blit(entity.getImage(), offset_pos)

        scaled_screen = pygame.transform.scale(self.internal_screen, self.screen.get_size())
        scaled_screen_rect = scaled_screen.get_rect(center = (self.half_w,self.half_h))
        self.screen.blit(scaled_screen, scaled_screen_rect)

    def draw_background(self, entities, target):
        self.center_target(target)

        for entity in entities:
            offset_pos = entity.getRectCorner() - self.offset
            self.internal_screen.blit(entity.getImage(), offset_pos)

    