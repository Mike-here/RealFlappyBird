import pygame

pygame.init()

#screen sizes
screen_width = 864
screen_height = 536

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Real Flappy Bird")

#load images
base = pygame.image.load('images/base.png')

# loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()            