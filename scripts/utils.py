import pygame
import os

BASE_IMAGE_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert() #.convert converts internal composition of picture and makes it easier to render VERY IMPORTANT TO INCLUDE
    img.set_colorkey((0, 0, 0))

    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMAGE_PATH + path)): #os.listdir will take a path and give all files in that path, THIS ONE MIGHT NOT WORK IN LINUX so add sorted to it
        images.append(load_image(path + '/' + img_name))

    return images

def load_player(path):
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert_alpha() #.convert converts internal composition of picture and makes it easier to render VERY IMPORTANT TO INCLUDE

    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color = img.get_at((x, y))  # Get the pixel color (R, G, B, A)
            if color.r == 0 and color.g == 0 and color.b == 0:  # Check if the color is black
                img.set_at((x, y), (0, 0, 0, 0))  # Set the pixel to transparent (alpha = 0)

    # img.fill((0, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Make all black pixels transparent
    # # img.set_colorkey((0, 0, 0))

    return img

