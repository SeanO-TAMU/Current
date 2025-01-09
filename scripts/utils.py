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



