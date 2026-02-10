import pygame, random
pygame.mixer.init()
point_sound = pygame.mixer.Sound('sound/Point.wav')
pygame.init()
'''
Welcome to PA0 – Flappy Bird! Throughout this code, you are going to find a recreation of a game you have probably
heard of before. This is an introductory assignment designed to help you familiarize yourself with what you can expect 
in future PAs. In this PA, you will barely need to code—mostly just tweaking some variable values and implementing
fewer than five lines of new code. It is recommended that you read through the code and the comments explaining 
some of the game mechanics.
'''
# Setup the screen -->
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird")

# Colors -->
# NOTE: This is in the RGB (Red, Green, Blue) format
WHITE = (255, 255, 255)
GREEN = (30, 159, 24)
BLACK = (0, 0, 0)
PLAYER = (218, 218 , 33)
CELESTE = (207, 122, 233)

# Font Size -->
big_font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 30)

# Text Coordinates -->
title_x = 50
title_y = 150

instruction_x = 80
instruction_y = 550

score_x = 200
score_y = 10

# Player Variables -->
bird_x = 50
bird_y = 300
bird_velocity = 0
# TODO 1: Tweaking the physics
# Looks like the player is falling too quickly not giving a change to flap it's wing, maybe tweak around with the value of this variable
gravity = 0.5
jump = -8
# Pipe Variables -->
pipe_x = 400
pipe_width = 80
pipe_x2 = pipe_x + 250
pipe_width2 = 80

# TODO 2.1: A Little gap Problem
# You probably noticed when running the code that it's impossible the player to go through the gaps
# play around with the pipe_gap variable so that its big enough for the player to pass through
pipe_gap = 150


pipe_height = 200
pipe_height2 = 200

# TODO 2.2: The too fast problem
# The pipes are moving way too fast! Play around with the pipe_speed variable until you find a good
# speed for the player to play in!
pipe_speed = 3.5

score = 0
game_over = False
game_started = False

clock = pygame.time.Clock()

bg = pygame.image.load("img/Fondo.png").convert()
bg = pygame.transform.scale(bg, (400, 690))


GROUND_Y = 520
HITBOX_W = 30
HITBOX_H = 30

pipe_height = random.randint(100, GROUND_Y - pipe_gap - 100)
pipe_height2 = random.randint(100, GROUND_Y - pipe_gap - 100)

scored_pipe1 = False
scored_pipe2 = False

class Bird (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/Bird.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen.get_height()/2))
bird_group.add(flappy)



running = True
while running:
    screen.blit(bg, (0, 0))
    # TODO 6: Changing the name!
    # D'oh! This is not yout name isn't follow the detailed instructions on the PDF to complete this task.
    name = "Mathew"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_started == False:
                    game_started = True
                    bird_velocity = jump
                elif game_over == False:
                    bird_velocity = jump
                else:
                    # TODO 3: Spawning back the Player
                    # After the bird crashes with a pipe the when spawning back the player it doesn't appear.
                    # It is your job to find why this is happening! (Hint: What variable stores the y coordinates
                    # of the bird)
                    bird_y = 300
                    bird_velocity = 0
                    pipe_x = 400
                    pipe_x2 = pipe_x + 250
                    score = 0
                    game_over = False
                    game_started = True

                    pipe_height = random.randint(100, GROUND_Y - pipe_gap - 100)
                    pipe_height2 = random.randint(100, GROUND_Y - pipe_gap - 100)

                    scored_pipe1 = False
                    scored_pipe2 = False

    if game_started == True and game_over == False:
        bird_velocity = bird_velocity + gravity
        bird_y = bird_y + bird_velocity

        flappy.rect.topleft = (bird_x, bird_y)

        pipe_x = pipe_x - pipe_speed
        pipe_x2 = pipe_x2 - pipe_speed

        if pipe_x < -80:
            pipe_x = 400
            pipe_height = random.randint(100, GROUND_Y - pipe_gap - 100)
            scored_pipe1 = False

        if pipe_x2 < -80:
            pipe_x2 = pipe_x + 250
            pipe_height2 = random.randint(100, GROUND_Y - pipe_gap - 100)
            scored_pipe2 = False

        bird_rect = pygame.Rect(0, 0, HITBOX_W, HITBOX_H)
        bird_rect.center = flappy.rect.center

        if bird_rect.bottom >= GROUND_Y or bird_rect.top < 0:
            game_over = True

        if (not scored_pipe1) and (bird_rect.left > pipe_x + pipe_width):
            score += 1
            point_sound.play()
            scored_pipe1 = True

        if (not scored_pipe2) and (bird_rect.left > pipe_x2 + pipe_width2):
            score += 1
            point_sound.play()
            scored_pipe2 = True

        top_pipe_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)

        bottom_pipe_rect = pygame.Rect(
            pipe_x,
            pipe_height + pipe_gap,
            pipe_width,
            GROUND_Y - (pipe_height + pipe_gap)
        )

        top_pipe_rect2 = pygame.Rect(pipe_x2, 0, pipe_width, pipe_height2)

        bottom_pipe_rect2 = pygame.Rect(
            pipe_x2,
            pipe_height2 + pipe_gap,
            pipe_width,
            GROUND_Y - (pipe_height2 + pipe_gap)
        )

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            game_over = True
        if bird_rect.colliderect(top_pipe_rect2) or bird_rect.colliderect(bottom_pipe_rect2):
            game_over = True

    bird_group.draw(screen)
    # TODO 5: A Bird's Color
    # The color of the player is currently white, let's change that a bit! You are free to change the bird's
    # to whatever you wish. You will need to head back to where the PLAYER variable was created and change the values.
    #pygame.draw.rect(screen, PLAYER, (bird_x, bird_y, 30, 30)) # Drawing the bird (You don't need to touch this line!)
    pygame.draw.rect(screen, GREEN, (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(screen, GREEN, (pipe_x, pipe_height + pipe_gap, pipe_width, 600))
    pygame.draw.rect(screen, GREEN, (pipe_x2, 0, pipe_width, pipe_height2))
    pygame.draw.rect(screen, GREEN, (pipe_x2, pipe_height2 + pipe_gap, pipe_width, 600))
    score_text = small_font.render(str(score), True, WHITE)
    screen.blit(score_text, (score_x, score_y))

    if game_started == False: # Start UI -->
        title_text = big_font.render("Flappy Bird", True, WHITE)
        instruction_text = small_font.render("Press space bar to flap!", True, WHITE)
        screen.blit(title_text, (title_x, title_y))
        screen.blit(instruction_text, (instruction_x, instruction_y))

    if game_over: # GameOver UI -->
        loss_text = small_font.render("Press Space to restart...", True, WHITE)
        screen.blit(loss_text, (85, 200))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
