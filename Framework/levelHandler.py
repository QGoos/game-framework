import random
import components.worldObjects as worldObjects
import components.player as player
from pygame import Rect


class LevelHandler():
    def __init__(self, tile_size: int, chunk_size: int) -> None:

        self.current_level: str = None
        self.level_chunks = {}
        self.old_chunks = {}
        self.new_chunks = {}
        self.level_live_entities = {}

        self.default_bg_value = 0

        self.tile_size = tile_size
        self.chunk_size = chunk_size


    def generate_new_chunk(self,chunk_name, CG):
        '''generate a chunk of map, entities and background separate'''
        chunk_entities = []
        # convert chunk name to integers
        x,y = chunk_name.split(';')
        x,y = int(x),int(y)

        # generate the background
        chunk_entity_tiles = self.generate_background(x, y, CG)

        # generate foreground objects
        # to be replaced with a function call to load/generate entities to be there
        for i in range(random.randrange(0,3)):
            tmp_wdth = random.randrange(self.tile_size//4,self.tile_size*0.75)
            tmp_hght = random.randrange(self.tile_size,self.tile_size*2)
            tmp_x = random.randrange(0,self.chunk_size) * self.tile_size + self.chunk_size * x * self.tile_size
            tmp_y = random.randrange(0,self.chunk_size) * self.tile_size + self.chunk_size * y * self.tile_size

            tmp_obj = worldObjects.Tree(tmp_x,tmp_y, tmp_wdth, tmp_hght, CG)
            chunk_entities.append(tmp_obj.getTrunk())
            chunk_entities.append(tmp_obj)

        for i in range(random.randrange(0,3)-1):
            tmp_wdth = random.randrange(self.tile_size//2,self.tile_size)
            tmp_x = random.randrange(0,self.chunk_size) * self.tile_size + self.chunk_size * x  * self.tile_size
            tmp_y = random.randrange(0,self.chunk_size) * self.tile_size + self.chunk_size * y  * self.tile_size

            tmp_obj = worldObjects.Rock(tmp_x,tmp_y, tmp_wdth, tmp_wdth, CG)
            chunk_entities.append(tmp_obj)

        self.level_chunks[chunk_name] = [chunk_entities,chunk_entity_tiles]

    def generate_background(self,x,y, CG):
        '''generate background tiles of map'''
        background = []

        # create the default background
        default_x = x * self.chunk_size * self.tile_size
        default_y = y * self.chunk_size * self.tile_size

        default_bg = worldObjects.BackgroundBlock(default_x, default_y, self.tile_size, self.default_bg_value, CG)
        default_bg.set_default_chunk_image()
        background.append(default_bg)

        return background

        # for more interesting backgrounds
        for y_pos in range(self.chunk_size):
            for x_pos in range(self.chunk_size):
                target_x = x * self.chunk_size * self.tile_size + x_pos * self.tile_size
                target_y = y * self.chunk_size * self.tile_size + y_pos * self.tile_size

                #logic for tile type
                if tile_map[y_pos][x_pos] == 0:
                    background.append(worldObjects.BackgroundBlock(target_x, target_y, self.tile_size, self.tile_size, CG))

        return background

    def which_chunk(self, coords: Rect) -> str:
        return f'{coords.centerx // (self.chunk_size*self.tile_size)};{coords.centery // (self.chunk_size*self.tile_size)}'

    def load_chunks(self, coord, CG):
        self.reset_new_chunks()
        onscreens = self.onscreen_chunks(coord)

        sortables = []
        background = []

        for target_chunk in onscreens:
            if target_chunk not in self.level_chunks:
                self.generate_new_chunk(target_chunk, CG)
        
            res = self.level_chunks[target_chunk]
            sortables.extend(res[0])
            background.extend(res[1])

        return[sortables,background]
        #self.add_new_chunk(target_chunk) this doenst actually happen here
        

    def onscreen_chunks(self, coord):
        result = []
        for y in range(-2,4,1):#6 #or 10
            for x in range(-3,5,1):#7 #or 12
                #offset chunks
                target_x = x + int(coord[0]/(self.chunk_size * self.tile_size))
                target_y = y + int(coord[1]/(self.chunk_size * self.tile_size))
                result.append(str(target_x) + ';' + str(target_y))

        return result

    def reset_new_chunks(self):
        self.new_chunks.clear()

    def add_new_chunk(self,chunk_name):
        self.new_chunks[chunk_name] = self.level_chunks[chunk_name]

    def get_chunk(self,chunk_name):
        return self.level_chunks[chunk_name]


