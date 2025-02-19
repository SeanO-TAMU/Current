import pygame 
import json

NEIGHBOR_OFFSETS = [(-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (0,0), (-1,1), (0,1), (1,1)]

PHYSICS_TILES = {'wall'}

AUTOTILE_TYPES = {'circuit', 'wall'}

FLOOR_TILES = {'circuit', 'circuitb', 'circuitr', 'start', 'end'}

AUTOTILE_CIRC_MAP = {
    tuple(sorted([(1,0), (-1,0)])): 0,
    tuple(sorted([(1,0)])): 13,
    tuple(sorted([(-1,0)])): 11,
    tuple(sorted([(0,1), (0,-1)])): 1,
    tuple(sorted([(0,1)])): 14,
    tuple(sorted([(0,-1)])): 12,
    tuple(sorted([(-1,0), (0,-1)])): 2,
    tuple(sorted([(-1,0), (0,1)])): 3,
    tuple(sorted([(1,0), (0,1)])): 4,
    tuple(sorted([(1,0), (0,-1)])): 5,
    tuple(sorted([(-1,0), (1,0), (0,-1)])): 6,
    tuple(sorted([(-1,0), (1,0), (0,1)])): 7,
    tuple(sorted([(-1,0), (0,-1), (0,1)])): 8,
    tuple(sorted([(1,0), (0,-1), (0,1)])): 9,
    tuple(sorted([(-1,0), (1,0), (0,-1), (0,1)])): 10,
}

AUTOTILE_WALL_MAP = {
    tuple(sorted([(0,1)])): 0,
    tuple(sorted([(0,1), (1,1)])): 0,
    tuple(sorted([(0,1), (-1,1)])): 0,
    tuple(sorted([(0,1), (-1,1), (1,1)])): 0,
    tuple(sorted([(0,-1)])): 1,
    tuple(sorted([(0,-1), (1,-1)])): 1,
    tuple(sorted([(0,-1), (-1,-1)])): 1,
    tuple(sorted([(0,-1), (1,-1), (-1,-1)])): 1,
    tuple(sorted([(-1,0)])): 2,
    tuple(sorted([(-1,0), (-1,1)])): 2,
    tuple(sorted([(-1,0), (-1,-1)])): 2,
    tuple(sorted([(-1,0), (-1,-1), (-1,1)])): 2,
    tuple(sorted([(1,0)])): 3,
    tuple(sorted([(1,0), (1,1)])): 3,
    tuple(sorted([(1,0), (1,-1)])): 3,
    tuple(sorted([(1,0), (1,-1), (1,1)])): 3,
    tuple(sorted([(0,1), (1,0), (1,1)])): 4,
    tuple(sorted([(0,1), (1,0), (1,1), (1,-1)])): 4,
    tuple(sorted([(0,1), (1,0), (1,1), (-1,1)])): 4,
    tuple(sorted([(0,1), (1,0), (1,1), (1, -1), (-1,1)])): 4,
    tuple(sorted([(0,1), (-1,0), (-1,1)])): 5,
    tuple(sorted([(0,1), (-1,0), (-1,1), (-1,-1)])): 5,
    tuple(sorted([(0,1), (-1,0), (-1,1), (1,1)])): 5,
    tuple(sorted([(0,1), (-1,0), (-1,1), (-1, -1), (1,1)])): 5,
    tuple(sorted([(0,-1), (1,0), (1,-1)])): 6,
    tuple(sorted([(0,-1), (1,0), (1,-1), (1, 1)])): 6,
    tuple(sorted([(0,-1), (1,0), (1,-1), (-1,-1)])): 6,
    tuple(sorted([(0,-1), (1,0), (1,-1), (1, 1), (-1,-1)])): 6,
    tuple(sorted([(0,-1), (-1,0), (-1,-1)])): 7,
    tuple(sorted([(0,-1), (-1,0), (-1,-1), (1,-1)])): 7,
    tuple(sorted([(0,-1), (-1,0), (-1,-1), (-1,1)])): 7,
    tuple(sorted([(0,-1), (-1,0), (-1,-1), (1, -1), (-1,1)])): 7,
    tuple(sorted([(1,-1)])): 8,
    tuple(sorted([(-1,-1)])): 9,
    tuple(sorted([(1,1)])): 10,
    tuple(sorted([(-1,1)])): 11,
}

class Tilemap:
    def __init__(self, game, tile_size=64):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} #pos in the lookup for this will be a string
        self.offgrid_tiles = [] #coordinates need to be in pixels for this one

        # for i in range(4):
        #     self.tilemap[str(2 + i) + ';3'] = {'type': 'circuit', 'variant': 0, 'pos': (2 + i, 3)}
        #     self.tilemap[str(2 + i) + ';2'] = {'type': 'wall', 'variant': 0, 'pos': (2 + i, 2)}

    def render(self, surf, offset=(0,0)):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

    def mask(self, pos):
        for tiles in self.tilemap.tiles_around(pos):
            pass #use the tiles_around function to only mask the tiles near player


    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def find_start(self):
        start_pos = [0,0]

        for loc in self.tilemap:
            if self.tilemap[loc]['type'] == 'start':
                start_pos[0] = self.tilemap[loc]['pos'][0] * 64 + 16
                start_pos[1] = self.tilemap[loc]['pos'][1] * 64 + 16

        return start_pos
    
        
    def at_end(self, pos):#returns true/end_rect once player collides with end_rect,
        end_rect = []
        for tile in self.tiles_around(pos):
            if tile['type'] == 'end':
                end_rect.append((pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)))
        return end_rect

    def num_starts(self):
        start_int = 0
        for loc in self.tilemap:
            if self.tilemap[loc]['type'] == 'start':
                start_int += 1

        return start_int
    
    def physics_rects_around(self, pos): #returns location of nearby walls
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def floor_rects_around(self, pos): #returns location of nearby floor tiles
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in FLOOR_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def save(self, path): #saves a map that has been created
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()

    def load(self, path): #function that loads a file/whatever file we give it
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors_circ = set()
            neighbors_wall = set()
            for shift in [(1,0), (-1,0), (0,-1), (0,1), (1,1), (1,-1), (-1,1), (-1,-1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == 'circuit' or self.tilemap[check_loc]['type'] == 'start' or self.tilemap[check_loc]['type'] == 'end':
                        neighbors_wall.add(shift)
            for shift in [(1,0), (-1,0), (0,-1), (0,1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == 'circuit' or self.tilemap[check_loc]['type'] == 'start' or self.tilemap[check_loc]['type'] == 'end':
                        neighbors_circ.add(shift)
            neighbors_circ = tuple(sorted(neighbors_circ))
            neighbors_wall = tuple(sorted(neighbors_wall))
            if tile['type'] == 'circuit' and (neighbors_circ in AUTOTILE_CIRC_MAP):
                tile['variant'] = AUTOTILE_CIRC_MAP[neighbors_circ]
            if tile['type'] == 'wall' and (neighbors_wall in AUTOTILE_WALL_MAP):
                tile['variant'] = AUTOTILE_WALL_MAP[neighbors_wall]