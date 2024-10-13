import pygame
from pygame.locals import *

pygame.init()

#screen sizes
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Real Flappy Bird")


# loop
run = True
while run:
    for event in pygame.get():
        if event.type == pygame.QUIT():
            run = False

            
pygame.quit()            