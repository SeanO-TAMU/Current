import pygame
import sys
import os

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Current')
        self.screen = pygame.display.set_mode((800, 600))
        # self.display = pygame.Surface((320, 240)) #generates an empty surface/image that is all black, render on this smaller display resolution and scale it up to the screen resolution
        
        self.clock = pygame.time.Clock()
        self.movement = [False, False, False, False] #index 0 is left, index 1 is right, index 2 is up, index 3 is down

        self.assets = {
            'player' : load_image('entities/player/00_orb1.png'),
            'circuit' : load_images('tiles/circuits'),
            'wall' : load_images('tiles/walls'),
            'background' : load_image('background.png')
        }

        self.player = PhysicsEntity(self, 'player', (120,200), (32,32))

        self.scroll = [0, 0]

        self.tilemap = Tilemap(self, tile_size=64)

        self.scroll = [0, 0] #cameras location
        
        pygame.init()

    def run(self):
        while True:
            # self.screen.fill((0, 0, 0))

            self.screen.blit(self.assets['background'], (0,0))

            self.scroll[0] += (self.player.rect().centerx - self.screen.get_width() / 2 - self.scroll[0]) / 8
            self.scroll[1] += (self.player.rect().centery - self.screen.get_height() / 2 - self.scroll[1]) / 8
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) #converts self.scroll to integers

            self.tilemap.render(self.screen, offset = render_scroll) 

            self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]) * 2, (self.movement[3] - self.movement[2]) * 2))

            self.player.render(self.screen, offset = render_scroll)

            # print(self.tilemap.physics_rects_around(self.player.pos)) # prints out nearby tiles

            for event in pygame.event.get(): #event manager
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

            # self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0)) #renders display onto screen, also uses that function to scale


            pygame.display.update()
            self.clock.tick(60)


Game().run()


