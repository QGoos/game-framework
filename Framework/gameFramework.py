import pygame
import sys
import components.player as player
import components.worldObjects as worldObjects
import random
from Framework.camera import *
from Framework.levelHandler import *
import os
import time

class Game():
    def __init__(self,tick_rate,display_width,display_height,game_name) -> None:
        ''' Initializes and runs a game
        
        Arguments:
        tick_rate: the number of updates per second
        display_width: window width in pixels
        display_height: window width in pixels
        game_name: the name of the game
        '''
        self.tick_rate = tick_rate
        self.display_width = display_width
        self.display_height = display_height
        self.game_name = game_name
        self.chunk_size = 8
        self.tile_size = 16

        self.CG = None
        self.LH = None
       
        # create clock
        self.clock = pygame.time.Clock()

        # create screen
        self.screen = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption(self.game_name)

        self.last_time = time.time()
        self.dt = time.time() - self.last_time

    def check_dt(self):
        '''return the delta time since last check'''
        self.dt = time.time() - self.last_time

    def set_dt(self, multiplier):
        '''scale the delta time'''
        self.check_dt()
        self.dt *= multiplier

    def set_last_time(self):
        '''initialize last time checked'''
        self.last_time = time.time()

    def set_up_camera_group(self) -> None:
        '''create camera group'''
        self.CG = Camera2(self.screen, self.tile_size)

    def set_up_level_handler(self) -> None:
        '''create a level handler'''
        self.LH = LevelHandler(self.tile_size, self.chunk_size)
        
    def run_game(self) -> None:
        '''runs a game'''
        pygame.init()
        
        self.set_up_camera_group()
        self.set_up_level_handler()

        # a temp player
        main_player = player.Player(0,0,self.tile_size,self.tile_size,3, self.CG)

        # generate forest
        world_objects = []

        entities = []
        entities.extend(world_objects)
        entities_to_draw = [main_player]
        entities_to_draw.extend(world_objects)
        background_entities = []

        chunks = {} # 5 (6) x 4 (5) showing (or 12x10)
        current_chunk = 'n;n'
        last_chunk = 'm;m'

        last_time = time.time()

        while True:
            # framerate independende
            self.set_dt(60)
            self.set_last_time()

            # close on x button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    #pygame.quit()
                if event.type == pygame.MOUSEWHEEL:
                    self.CG.set_zoom_scale(event.y * 0.03)

            # load chunks into entities, load chunks when we switch chunks
            if current_chunk != last_chunk:
                entities_to_draw = [main_player]
                background_entities = []
                entities = []

                loaded = self.LH.load_chunks((self.CG.get_camera_x(), self.CG.get_camera_y()), self.CG)

                background_entities.extend(loaded[1])
                entities_to_draw.extend(loaded[0])
                entities = entities_to_draw[1:]

                # add objects that need to be updated separate from unchanging objects
                self.CG.add(entities)
                self.CG.add(background_entities)

            last_chunk = self.LH.which_chunk(main_player.getRect())#f'{main_player.getRect().centerx // (self.chunk_size*self.tile_size)};{main_player.getRect().centery // (self.chunk_size*self.tile_size)}'
            
            self.CG.update(self.dt)
            for entity in entities:
                # to implement check if on screen, then add to an on screen list then draw from top down
                main_player.collide(entity)
            
            # move the camera
            self.CG.draw_background(background_entities, main_player)
            self.CG.draw(entities_to_draw, main_player)

            # check player chunk
            if current_chunk != last_chunk:
                self.CG.remove(entities)
                self.CG.remove(background_entities)
                
            current_chunk = self.LH.which_chunk(main_player.getRect())#f'{main_player.getRectCorner()[0] // (self.chunk_size*self.tile_size)};{main_player.getRectCorner()[1] // (self.chunk_size*self.tile_size)}'

            # tick rate
            self.clock.tick(self.tick_rate)
            pygame.display.update()
