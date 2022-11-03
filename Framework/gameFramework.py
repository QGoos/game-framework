import pygame
import sys
import components.player as player
import components.worldObjects as worldObjects
import random
from Framework.camera import *
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
        self.chunk_size = 4
        self.tile_size = 32
       
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
        self.CG = Camera(self.screen)

    def generate_chunk(self,x,y):
        '''generate a chunk of map, entities and background separate'''
        chunk_entities = []
        chunk_entity_tiles = self.generate_background(0,x,y)
        offset = [0,x * 32 * 2]

        for i in range(random.randrange(0,3)):#range(10):#
            tmp_wdth = random.randrange(8,24)
            tmp_hght = random.randrange(32,64)
            tmp_x = random.randrange(0,self.chunk_size) * self.tile_size + self.chunk_size * x * self.tile_size + offset[0]
            tmp_y = random.randrange(0,self.chunk_size) * self.tile_size + self.chunk_size * y * self.tile_size + offset[1]

            tmp_obj = worldObjects.Tree(tmp_x,tmp_y, tmp_wdth, tmp_hght, self.CG)
            chunk_entities.append(tmp_obj.getTrunk())
            chunk_entities.append(tmp_obj)

        for i in range(random.randrange(0,3)-1):
            tmp_wdth = random.randrange(16,32)
            tmp_x = random.randrange(0,self.chunk_size) * self.tile_size + self.chunk_size * x  * self.tile_size + offset[0]
            tmp_y = random.randrange(0,self.chunk_size) * self.tile_size + self.chunk_size * y  * self.tile_size + offset[1]

            tmp_obj = worldObjects.Rock(tmp_x,tmp_y, tmp_wdth, tmp_wdth, self.CG)
            chunk_entities.append(tmp_obj)

        return [chunk_entities,chunk_entity_tiles]

    def generate_background(self,tile_identifier,x,y):
        '''generate background tiles of map'''
        background = []
        offset = [0, x * self.tile_size * 2]
        for y_pos in range(self.chunk_size):
            for x_pos in range(self.chunk_size):
                target_x = x * self.chunk_size * self.tile_size + x_pos * self.tile_size + offset[0] # + (y * self.tile_size * self.chunk_size)
                target_y = y * self.chunk_size * self.tile_size + y_pos * self.tile_size + offset[1] # + (x * self.tile_size * self.chunk_size - y * self.tile_size* self.chunk_size)

                #logic for tile type
                if tile_identifier == 0:
                    background.append(worldObjects.BackgroundBlockIso(target_x, target_y, 32, 32, self.CG, x_pos, y_pos))

        return background
        
    def run_game(self) -> None:
        '''runs a game'''
        pygame.init()
        
        self.set_up_camera_group()

        # a temp player
        main_player = player.Player(0,0,32,32,3, self.CG)

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
                for y in range(-4,6,1):#11 #6 #or 10
                    for x in range(-4,6,1):#13 #7 #or 12
                        #offset chunks
                        target_x = x - 1 + int(self.CG.get_camera_x()/(self.chunk_size * self.tile_size))
                        target_y = y - 1 + int(self.CG.get_camera_y()/(self.chunk_size * self.tile_size))
                        target_chunk = str(target_x) + ';' + str(target_y)
                        # creat or load unloaded chunks
                        if target_chunk not in chunks:
                            chunks[target_chunk] = self.generate_chunk(target_x,target_y)
                        background_entities.extend(chunks[target_chunk][1])
                        entities_to_draw.extend(chunks[target_chunk][0])
                        entities.extend(chunks[target_chunk][0])

                # add objects that need to be updated separate from unchanging objects
                self.CG.add(entities)
                self.CG.add(background_entities)
            #print(current_chunk,last_chunk)
            #x_sign,y_sign = (main_player.getRect().centerx)/abs(main_player.getRect().centerx),(main_player.getRect().centery)/abs(main_player.getRect().centery)
            #chunk_dist = (abs(main_player.getRect().centerx*2) + abs(main_player.getRect().centery))//(32*16)
            #print(chunk_dist,main_player.getRect().centerx,main_player.getRect().centery)
            last_chunk = f'{main_player.getRect().centerx // (self.chunk_size*self.tile_size*2)};{main_player.getRect().centery // (self.chunk_size*self.tile_size)}'
            
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
                
            current_chunk = f'{main_player.getRect().centerx // (self.chunk_size*self.tile_size*2)};{main_player.getRect().centery // (self.chunk_size*self.tile_size*2)}'

            # tick rate
            self.clock.tick(self.tick_rate)
            pygame.display.update()
