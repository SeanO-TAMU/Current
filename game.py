import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Current')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240)) #generates an empty surface/image that is all black, render on this smaller display resolution and scale it up to the screen resolution
        
        self.clock = pygame.time.Clock()
        self.movement = [False, False] #index 0 is x-axis, index 1 is y-axis

        self.assets = {}

    def run(self):
        while True:
            for event in pygame.event.get(): #event manager
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


Game().run()

