import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) #makes sure each object/entity has its own position list instead of using a reference
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) #dynamically make a rect for a player

    def render(self, surf, offset=(0,0)): #draws player on screen
        surf.blit(self.game.assets[self.type], (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def update(self, tilemap, movement=(0,0)): #function for calculating the movement of the player
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) #movement function

        self.pos[0] += frame_movement[0]
        
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1] #moving the y pos
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y