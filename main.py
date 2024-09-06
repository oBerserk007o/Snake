import math
import random

import pygame
import sys

import pygame_menu

# initialize it
pygame.init()

# configurations
frequency = 1 # in updates per second
block_size = 40
block_width_number = 12
block_height_number = 12
fps = 15
window_height = block_height_number * block_size
window_width = block_width_number * block_size

# title and logo
pygame.display.set_caption("Snake")
logo = pygame.image.load('./snake.png') # thank you to Snake Game Nokia (https://play.google.com/store/apps/details?id=com.giftintech.android.snake.game&hl=en_US&pli=1) by Giftin Technologies
pygame.display.set_icon(logo)

# colours (yes, I'm canadian, I put u's in words)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (40, 173, 49)
LIGHT_GREEN = (79, 238, 90)

# creating window
display = pygame.display.set_mode((window_width, window_height))

# creating our frame regulator
clock = pygame.time.Clock()

# position of the player
pos = pygame.Vector2(-40, display.get_height() - block_size)

fps_per_frequency = int(fps / frequency)
frame = fps_per_frequency
ticks = 0
direction = 2 # 1 = up, 2 = right, 3 = down, 4 = left


# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame (but modified)
def draw_grid():
    for x in range(int(block_width_number)):
        for y in range(int(block_height_number)):
            rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            pygame.draw.rect(display, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN, rect)


def guess_ill_die():
    pygame.mixer.Sound("./windows_shutdown.mp3" if random.randint(0, 1) == 1 else "./windows_error.mp3").play()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


def check_if_dead():
    if pos.x > window_width - block_size or pos.x < 0:
        guess_ill_die()
    if pos.y > window_height - block_size or pos.y < 0:
        guess_ill_die()


# forever loop
while True:
    # frame clock ticking
    clock.tick(fps)

    # draw stuff once per second
    if frame == fps_per_frequency:
        draw_grid()
        pos.x += block_size if direction == 2 else 0
        pos.x -= block_size if direction == 4 else 0
        pos.y += block_size if direction == 3 else 0
        pos.y -= block_size if direction == 1 else 0
        player = pygame.Rect(pos.x, pos.y, block_size, block_size)
        pygame.draw.rect(display, "red", player)
        check_if_dead()
        print(frame)
        print(pygame.time.get_ticks() - ticks)
        frame = 0
        ticks = pygame.time.get_ticks()
    frame += 1

    # movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        direction = 1
    if keys[pygame.K_s]:
        direction = 3
    if keys[pygame.K_a]:
        direction = 4
    if keys[pygame.K_d]:
        direction = 2
    if keys[pygame.K_LSHIFT]:
        frequency = 4
        frame = fps_per_frequency
    else:
        frequency = 1

    pygame.display.flip()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

