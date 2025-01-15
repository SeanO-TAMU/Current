#map editor file

import pygame
import sys


from scripts.utils import load_images #imports image loading function

from scripts.tilemap import Tilemap #imports tilemap class which helps to load tiles onto screen

RENDER_SCALE = 1.0 #constant used to scale down pixel values since we scale them up from display to screen

# pygame.init()

#game object
class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((800, 600))
        # self.display = pygame.Surface((320, 240)) #generates an empty surface/image that is all black, render on this smaller display resolution and scale it up to the screen resolution

        self.clock = pygame.time.Clock()
        self.movement = [False, False, False, False] #in order to move the camera anywhere

        self.assets = { #creates an assets dictionary
            'circuit': load_images('tiles/circuits'),
            'wall': load_images('tiles/walls'),
            'start' : load_images('tiles/start'),
            'end' : load_images('tiles/end'),
        }

        self.tilemap = Tilemap(self, tile_size=64) #initilize instance of Tilemap with tile size of 16 pixels

        self.start = 0

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        
        

        self.scroll = [0, 0] #camera starting position

        self.tile_list = list (self.assets) #transfrom the assets dictionary into a list of the keys

        #use different buttons to change between these
        self.tile_group = 0 #determines which tile we are using (grass, stone, etc...)
        self.tile_variant = 0 #determines which type of tile we are using (stone1, stone2, etc...)

        self.left_clicking = False
        self.right_clicking = False
        
        self.shift = False #used for moving between variants

        self.ongrid = True #used for controlling when to place things offgrid





    def run(self):
        # game loop
        while True:
            self.screen.fill((0,0,0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 7
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 7
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) #rounds up to stop the jittering that happens when using floats instead of ints

            self.tilemap.render(self.screen, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy() #makes a copy of the selected tile
            current_tile_img.set_alpha(100) #makes image partially transparent

            mpos = pygame.mouse.get_pos() #gives pixel coordinates of mouse with respect to the window, use this to figure out where tile should go
            mpos = (mpos[0]/RENDER_SCALE, mpos[1]/RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size)) #gives the coordinates of mouse in terms of the tile system

            if self.ongrid:
                self.screen.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1])) #extra math done here to align with grid, so we are essentially scaling it back up here to fit with grid
            else:
                self.screen.blit(current_tile_img, mpos) #if offgrid show image based on mouse position

            if self.left_clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc] #deletes tile at that location
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)


            self.screen.blit(current_tile_img, (5,5)) #displays chosen block in top left of screen

            for event in pygame.event.get(): #event manager
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  #event.button == 1 is basically saying when it is the left mouse button/left click
                        self.left_clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])}) #this adds the it to offgrid just once, self.scroll gets added in order to make sure it is added correctly to the world no matter where youo have the camera moved
                    if event.button == 3: #right clicking is 3
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.left_clicking = False
                    if event.button == 3:
                        self.right_clicking = False


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g: #whether or not tiles should be placed ongrid
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_t: #press t to autotile everything in map/grid
                        self.tilemap.autotile()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False


            pygame.display.update()
            self.clock.tick(60)


Editor().run()
