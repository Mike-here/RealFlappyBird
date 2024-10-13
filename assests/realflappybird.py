import pygame

pygame.init()
clock = pygame.time.Clock()
fps = 60

#screen sizes
screen_width = 292
screen_height = 603

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Real Flappy Bird")

# game variables
base_scroll = 0
scroll_speed = 2

#load images
background = pygame.image.load("background-day.png")
base = pygame.image.load("base.png")

#creating the bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #creating a list of 3 static bird images to make it look like flipping fast
        self.images = []
        self.index = 0
        self.counter = 0
        for x in range(1,4):
            pic = pygame.image.load(f"bluebird{x}.png")
            self.images.append(pic)                     #list
        self.image = self.images[self.index]            #starting with the first bird(midflap)
        self.rect = self.image.get_rect()                           #forms a rectangle around the bird
        self.rect.center = [x,y]                                    #position of the bird

    def update(self):
        #controlling the animation.
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0

#bird grouping.
bird_group = pygame.sprite.Group()

flappy = Bird(30, int(screen_height / 2))

bird_group.add(flappy)

# loop
run = True
while run:

    clock.tick(fps)

    #display the static background.
    screen.blit(background, (0,0))

    bird_group.draw(screen)

    #display the scrolling base.
    screen.blit(base, (base_scroll,490))
    base_scroll -= scroll_speed
    if abs(base_scroll) > 46:
        base_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()        


pygame.quit()            