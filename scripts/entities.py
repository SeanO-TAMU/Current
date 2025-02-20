import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) #makes sure each object/entity has its own position list instead of using a reference
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.move = True #change the behavior behind this

    def rect(self):  # need to not use rect for player since player is round
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) #dynamically make a rect for a player

    def mask(self):
         mask = pygame.mask.from_surface(self.game.assets[self.type])
         return mask

    def render(self, surf, offset=(0,0)): #draws player on screen
        surf.blit(self.game.assets[self.type], (self.pos[0] - offset[0], self.pos[1] - offset[1]))

        #makes mask of the image
        # mask = pygame.mask.from_surface(self.game.assets[self.type])
        # mask_surface = mask.to_surface()
        # surf.blit(mask_surface, (self.pos[0] - offset[0], self.pos[1] - offset[1]))



    #can use rect collisions for floor tiles since we don't have to worry about the diagonals, or not?
    #set direction of initial contact as the direction we are currently moving so I guess we just need to figure that out
    #when exiting use framemovement to detect when a tile has been exited in the proper direction if so change the tile type

    def alter_floor_blue(self, tilemap, movement=(0,0)): #function that changes floor tiles

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) #movement function
        entity_mask = self.mask()

        for rect in tilemap.floor_rects_around(self.pos): #function that changes floor tiles

            tile_surface = pygame.Surface(rect.size)
            tile_surface.fill((255, 255, 255))
            wall_mask = pygame.mask.from_surface(tile_surface) # makes a mask of the wall
            tileSize = tilemap.tile_size

            offset = (rect.x - self.pos[0], rect.y - self.pos[1])
            overlap_point = entity_mask.overlap(wall_mask, offset)
            if(overlap_point):
                # print("overlap: ", overlap_point)
                tile_loc = (int((self.pos[0] + overlap_point[0]) // tileSize), int((self.pos[1] + overlap_point[1]) // tileSize))
                check_loc = str(tile_loc[0]) + ';' + str(tile_loc[1]) #location string of tile
                # print("location: ", check_loc)
                tile = tilemap.get_tile(check_loc)
                if tile['style'] == 0 and tile['type'] == 'end':
                    tile['type'] = 'endb'
                    tile['style'] = 1
                elif tile['style'] == 0 and tile['type'] != 'start':
                    if frame_movement[0] > 0:             
                        tile['type'] = 'circuitb'
                        tile['style'] = 1
                        tile['side'] = 'right' 
                    if frame_movement[0] < 0:
                        tile['type'] = 'circuitb'
                        tile['style'] = 1
                        tile['side'] = 'left'                  
                    if frame_movement[1] > 0:
                        tile['type'] = 'circuitb'
                        tile['style'] = 1
                        tile['side'] = 'down'                   
                    if frame_movement[1] < 0:
                        tile['type'] = 'circuitb'
                        tile['style'] = 1
                        tile['side'] = 'up'


    def update(self, tilemap, movement=(0,0)): #function for calculating the movement of the player
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) #movement function

        if (self.move):
            self.pos[0] += frame_movement[0]
            entity_mask = self.mask() #gets mask for player
            entity_rect = self.rect()
            for rect in tilemap.physics_rects_around(self.pos):

                tile_surface = pygame.Surface(rect.size)
                tile_surface.fill((255, 255, 255))
                wall_mask = pygame.mask.from_surface(tile_surface) # makes a mask of the wall

                offset = (rect.x - self.pos[0], rect.y - self.pos[1])
                overlap_point = entity_mask.overlap(wall_mask, offset)
                if(overlap_point):#do some modulus check to move by 1 pixel, also add back determining direction
                    if frame_movement[0] > 0: #right
                        self.pos[0] -= frame_movement[0]
                    if frame_movement[0] < 0: #left
                        self.pos[0] -= frame_movement[0]

            self.pos[1] += frame_movement[1] #moving the y pos
            entity_rect = self.rect()
            for rect in tilemap.physics_rects_around(self.pos):

                tile_surface = pygame.Surface(rect.size)
                tile_surface.fill((255, 255, 255))
                wall_mask = pygame.mask.from_surface(tile_surface) # makes a mask of the wall

                offset = (rect.x - self.pos[0], rect.y - self.pos[1])
                overlap_point = entity_mask.overlap(wall_mask, offset)

                if(overlap_point): #do some modulus check to move by 1 pixel, also add back determining direction
                    self.pos[1] -= frame_movement[1]

            self.alter_floor_blue(tilemap, movement)

            # would need to remove lower portion of this function if we add enemy entities since the following is just for the player
            for rect in tilemap.at_end(self.pos):
                if entity_rect.colliderect(rect):
                    self.ending(rect)


    #need to have this work for every direction as well since it is not always +/positive direction
    def ending(self, rect):
        self.move = False
        self.pos[0] += (-1 * self.pos[0] + rect.centerx - 16)
        self.pos[1] += (-1 * self.pos[1] + rect.centery - 16)
        self.game.movement = [False, False, False, False]
        self.velocity[0] = 0
        
        
