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

FPS = 30
PLATER_VEL = 5 # the speed of the player to move on the screen

window = pygame.display.set_mode((WIDTH, HEIGHT))

# A function to flip the char images 
# ex, when want to move the opposite direction then the char should be flipped to face the other side 
def flip(sprites):
    # firts arg is the source i want to flip, the 2nd and 3rd how to flip it in x or y
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join('assets', dir1, dir2)
    # it will get all the files in path and then the image dic will have the directions for every image
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        # conver_alpha() -> make a png smooth its edges. 
        # convert() method will convert the pixle formats to the same pixle format as the display
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet,(0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace('.png', '') + '_right'] = sprites
            all_sprites[image.replace('.png', '') + '_left'] = flip(sprites)
        else:
            all_sprites[image.replace('.png', '')] = sprites

    return all_sprites


class Player(pygame.sprite.Sprite):
    """
        Spawn a player
    """
    GRAVITY = 1 
    SPRITES = load_sprite_sheets(dir1='MainCharacters', dir2='MaskDude', width=32, height=32, direction=True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        # Rect create a rectangle
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = 0
        self.direction = "right"
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
        # self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        # it calls once every frame to move our char and animation 
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        # the main animation of the char
        sprite_sheet = 'idle'
        # check if the player by check its x_vel
        if self.x_vel != 0:
            sprite_sheet = 'run'
            
        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

    def draw(self, win):
        # self.sprite = self.SPRITES['idle_' + self.direction][0]
        win.blit(self.sprite, (self.rect.x, self.rect.y))

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    
        player.loop(FPS)
        handle_move(player= player)
        draw(window= window, background= background, bg_image= bg_image, player= player)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)