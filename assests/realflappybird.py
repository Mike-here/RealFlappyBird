import pygame 
import random

pygame.init()
clock = pygame.time.Clock()
fps = 60

#screen sizes
screen_width = 400
screen_height = 603


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Real Flappy Bird")

#define font
font = pygame.font.SysFont("freesans 78", 30)

#define text_color
black = (250, 250, 250)

# game variables
base_scroll = 0
scroll_speed = 2
flying = False
game_over = False
pipe_distance = 120
pipe_freg = 1500            #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_freg
score = 0
pass_pipe = False

#load images
background = pygame.image.load("background-day.png")
base = pygame.image.load("base.png")
restart_img = pygame.image.load("restart.jpg")




def reset_game():
    pipe_group.empty()
    flappy.rect.x = 30
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

#draw the scores from text.
def draw_text(text, font, text_color, x, y):
    score_img = font.render(text, True, text_color)
    screen.blit(score_img, (x, y))                        #display the score image on the screen.

#creating the bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        #creating a list of 3 static bird images to make it look like it's flapping fast
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1,4):
            pic = pygame.image.load(f"bluebird{i}.png")
            self.images.append(pic)                     #list
        self.image = self.images[self.index]            #starting with the first bird(midflap)
        self.rect = self.image.get_rect()                           #forms a rectangle around the bird
        self.rect.center = [x,y]                                    #position of the bird
        self.vel = 0

    def update(self):

        #gravity aspect
        if flying == True:
            self.vel += 0.2
            if self.vel > 4:
                self.vel = 4
            
            if self.rect.bottom <= 490:
                self.rect.y += int(self.vel)

        if game_over == False:
            #jumping
            if pygame.mouse.get_pressed()[0] == 1:
                self.vel -= 0.62

            

            #controlling the animation.
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]        

            #bird's rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe-red.png")
        self.rect = self.image.get_rect()
        #position 1 is up and -1 is down
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_distance / 2)]
        if position == -1:    
            self.rect.topleft = [x, y + int(pipe_distance / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class RestartButton():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topright = (x, y)

    # draw the restart button
    def draw(self):
        action = False
        #get the position of the mouse
        pos = pygame.mouse.get_pos()

        #check if mouse is over the restart button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image,  (self.rect.x, self.rect.y))
         
        return action 
        


#objects grouping.
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(30, int(screen_height / 2))

bird_group.add(flappy)

#create the restart button 
restart = RestartButton(screen_width // 2 + 75, screen_height // 2 - 100, restart_img)

# loop
run = True
while run:

    clock.tick(fps)

    #display the static background.
    screen.blit(background, (0,0))

    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)
    
    #display the scrolling base.
    screen.blit(base, (base_scroll,490))

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    draw_text(str(score), font, black, int(screen_width / 2), 20)           

    # check if it collides or move above the top level
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom >= 490:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        #generate new pipes.
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_freg:
            pipe_height = random.randint(-85, 85)
            pipe_btm = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            pipe_top = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(pipe_btm)
            pipe_group.add(pipe_top)
            last_pipe = time_now
            

        #make sure the base scrolls well   
        base_scroll -= scroll_speed
        if abs(base_scroll) > 53.8:
            base_scroll = 0

        pipe_group.update()      

    #check for gameover and restart
    if game_over == True:
        if restart.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)) and flying == False and game_over == False:
            flying = True  
    
                      

    pygame.display.update()        


pygame.quit()            