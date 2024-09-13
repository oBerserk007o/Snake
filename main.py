import random
import pygame
from pygame import gfxdraw
import sys

# initialize it
pygame.init()

# configurations
frequency = 1 # in updates per second
block_size = 40
block_width_number = 12
block_height_number = 12
block_number = block_height_number*block_width_number
fps = 15
window_height = block_height_number * block_size
window_width = block_width_number * block_size

# title and logo
pygame.display.set_caption("Snake")
# thank you to Snake Game Nokia (https://play.google.com/store/apps/details?id=com.giftintech.android.snake.game&hl=en_US&pli=1)
# by Giftin Technologies
logo = pygame.image.load('./snake.png')
pygame.display.set_icon(logo)

# colours (yes, I'm canadian, I put u's in words)
DARK_GREEN = (40, 173, 49)
LIGHT_GREEN = (79, 238, 90)
RED = (191, 25, 25)

# creating window
display = pygame.display.set_mode((window_width, window_height))

# creating our frame regulator
clock = pygame.time.Clock()

# position of the player
pos = pygame.Vector2(0, display.get_height() - block_size)
# pos_block = pygame.Vector2(round(pos.x / block_size), round(pos.y / block_size))
pos_block = pygame.Vector2(0, block_height_number - 1)


def draw_grid():
    for x in range(int(block_width_number)):
        for y in range(int(block_height_number)):
            rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            pygame.draw.rect(display, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN, rect)

            """
            text = pygame.font.Font('comfortaa.ttf', 15)
            text_surface = text.render(f"{x}, {y}", True, RED)
            text_rect = text_surface.get_rect(center=((x * block_size) + block_size / 2, (y * block_size) + block_size / 2))
            display.blit(text_surface, text_rect)
            """

            if apples[x][y]:
                gfxdraw.filled_circle(display, x*block_size + int(block_size / 2),
                                 y*block_size + int(block_size / 2), int(3 * block_size / 8), RED)
                gfxdraw.aacircle(display, x*block_size + int(block_size / 2),
                                 y*block_size + int(block_size / 2), int(3 * block_size / 8), RED)
    pygame.display.flip()


def guess_ill_die():
    text = pygame.font.Font('comfortaa.ttf', 40)
    text_surface = text.render('GAME OVER', True, RED)
    text_rect = text_surface.get_rect(center=(window_width / 2, window_height / 2))
    display.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.mixer.Sound("./windows_shutdown.mp3" if random.randint(0, 1) == 1 else "./windows_error.mp3").play()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


def check_if_dead():
    if (pos_block.x > block_width_number - 1
            or pos_block.x < 0
            or pos_block.y > block_height_number - 1
            or pos_block.y < 0):
        guess_ill_die()


def check_for_apple():
    print(pos_block.x, pos_block.y)
    #print(apples[int(pos_block.x) - 1][int(pos_block.y) - 1])
    if apples[int(pos_block.x)][int(pos_block.y)]:
        grow()
        apples[int(pos_block.x)][int(pos_block.y)] = False
        apples[random.randint(0, block_width_number - 1)][random.randint(0, block_height_number - 1)] = True


def grow():
    print("Apple eaten! yummy")


fps_per_frequency = int(fps / frequency)
frame = fps_per_frequency
ticks = 0
score = 0

# creating an apples array with apples in random places
apples = [[(random.randint(0, block_number) in range(3)) for i in range(block_width_number)]
          for j in range(block_height_number + 1)]

# there are no apples at the position of the player
apples[0][block_height_number - 1] = False

# there is always an apple in the center of the board
apples[int(block_width_number / 2)][int(block_height_number / 2)] = True

direction = 2 # 1 = up, 2 = right, 3 = down, 4 = left
direction_for_tick = direction
setup = True


# forever loop
while True:
    # frame clock ticking
    clock.tick(fps)

    # draw stuff once per second
    if frame == fps_per_frequency:
        draw_grid()

        # updating player's drawn position
        pos.x += block_size if (direction == 2 and not setup) else 0
        pos.x -= block_size if (direction == 4 and not setup) else 0
        pos.y += block_size if (direction == 3 and not setup) else 0
        pos.y -= block_size if (direction == 1 and not setup) else 0

        # updating pos_block with pos
        pos_block.x = int(pos.x / block_size)
        pos_block.y = int(pos.y / block_size)

        # draw player
        direction_for_tick = direction
        player = pygame.Rect(pos.x, pos.y, block_size, block_size)
        pygame.draw.rect(display, "red", player)

        # checking if player has to die or grow
        check_if_dead()
        check_for_apple()

        print(frame)
        print(pygame.time.get_ticks() - ticks)
        frame = 0
        ticks = pygame.time.get_ticks()
    frame += 1

    # I know, don't judge me
    if setup:
        setup = False

    # movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and direction_for_tick != 3:
        direction = 1
    if keys[pygame.K_s] and direction_for_tick != 1:
        direction = 3
    if keys[pygame.K_a] and direction_for_tick != 2:
        direction = 4
    if keys[pygame.K_d] and direction_for_tick != 4:
        direction = 2
    if keys[pygame.K_LSHIFT]:
        frequency = 3
        frame = fps_per_frequency
    else:
        frequency = 1

    pygame.display.flip()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

