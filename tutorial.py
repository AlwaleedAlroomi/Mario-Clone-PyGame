from email.mime import image
import os
import random
import math
import pygame
from os import listdir, name
from os.path import isfile, join



pygame.init()
pygame.display.set_caption('First Game')


WIDTH, HEIGHT = 1366, 768

FPS = 60
PLATER_VEL = 5 # the speed of the player to move on the screen

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    """
        Spawn a player
    """
    COLOR = (255, 0, 0)
    GRAVITY = 1 

    def __init__(self, x, y, width, height):
        # Rect create a rectangle
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = 0
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0

    def move(self, dx, dy):
        # it will take the displacement for x and y so when the player move
        # it adds the new position for the base x and y value from the pygame.Rect()
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        # if i want to move the player to left I change the the x_vel from positive to negative  
        self.x_vel = -vel
        # check the player direction if it != left direction ? then change it to the left : do nothing jsut move 
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        # it calls once every frame to move our char and animation 
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)

def get_background(name):
    image = pygame.image.load(join('assets', 'Background', name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width +1):
        for j in range(HEIGHT // height +1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def draw(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)

    player.draw(window)
    pygame.display.update()

def handle_move(player):
    # to get the pressed key
    keys = pygame.key.get_pressed()

    # to set the x_vel to zero again so the char only move while the key is pressed 
    player.x_vel = 0
    # check what key pressed and take an action
    if keys[pygame.K_a]:
        player.move_left(PLATER_VEL)

    if keys[pygame.K_d]:
        player.move_right(PLATER_VEL)



def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Purple.png")
    player = Player(100, 100, 50, 50)

    run = True
    while run:
        clock.tick(FPS)
        draw(window= window, background= background, bg_image= bg_image, player= player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    
        player.loop(FPS)
        handle_move(player= player)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)