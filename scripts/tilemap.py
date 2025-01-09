import pygame 
import json

NEIGHBOR_OFFSETS = [(-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (0,0), (-1,1), (0,1), (1,1)]

PHYSICS_TILES = {'wall'}

class Tilemap:
    def __init__(self, game, tile_size=64):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} #pos in the lookup for this will be a string
        self.offgrid_tiles = [] #coordinates need to be in pixels for this one

        for i in range(4):
            self.tilemap[str(2 + i) + ';3'] = {'type': 'circuit', 'variant': 0, 'pos': (2 + i, 3)}
            self.tilemap[str(2 + i) + ';2'] = {'type': 'wall', 'variant': 0, 'pos': (2 + i, 2)}

    def render(self, surf):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects