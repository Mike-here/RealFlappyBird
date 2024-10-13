import pygame

pygame.init()

#screen sizes
screen_width = 384
screen_height = 583

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Real Flappy Bird")

#load images
background = pygame.image.load("background-day.png")

# loop
run = True
while run:

    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()        


pygame.quit()            