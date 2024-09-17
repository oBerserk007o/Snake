import random
import pygame
from pygame import gfxdraw
import sys

# initialize it
pygame.init()

# configurations
frequency = 1 # in updates per second
unit = 40
block_width_number = 12
block_height_number = 12
block_number = block_height_number*block_width_number
fps = 15
window_height = block_height_number * unit
window_width = block_width_number * unit

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
pos = pygame.Vector2(0, display.get_height() - unit)
# pos_block = pygame.Vector2(round(pos.x / block_size), round(pos.y / block_size))
pos_block = pygame.Vector2(0, block_height_number - 1)
length = 3
snake = []

direction = 2 # 1 = up, 2 = right, 3 = down, 4 = left
direction_for_tick = direction

def draw_grid():
    for x in range(int(block_width_number)):
        for y in range(int(block_height_number)):
            rect = pygame.Rect(x * unit, y * unit, unit, unit)
            pygame.draw.rect(display, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN, rect)
            """
            # for showing positions of each cell
            text = pygame.font.Font('comfortaa.ttf', 15)
            text_surface = text.render(f"{x}, {y}", True, RED)
            text_rect = text_surface.get_rect(center=((x * block_size) + block_size / 2, (y * block_size) + block_size / 2))
            display.blit(text_surface, text_rect)
            """
            if apples[x][y]:
                gfxdraw.filled_circle(display, x * unit + int(unit / 2),
                                      y * unit + int(unit / 2), int(3 * unit / 8), RED)
                gfxdraw.aacircle(display, x * unit + int(unit / 2),
                                 y * unit + int(unit / 2), int(3 * unit / 8), RED)
    pygame.display.flip()


def guess_ill_die():
    # game over text
    text = pygame.font.Font('comfortaa.ttf', 40)
    text_surface = text.render('GAME OVER', True, RED)
    text_rect = text_surface.get_rect(center=(window_width / 2, window_height / 2))
    display.blit(text_surface, text_rect)
    pygame.display.flip()

    # death sound
    pygame.mixer.Sound("./windows_shutdown.mp3" if random.randint(0, 1) == 1 else "./windows_error.mp3").play()

    # death animations
    for position in snake:
        body = pygame.Rect(position[0], position[1], unit, unit)
        pygame.draw.rect(display, DARK_GREEN if ((position[0] + position[1]) / unit) % 2 == 0 else LIGHT_GREEN, body)
        pygame.display.flip()
        pygame.time.wait(300)
    pygame.quit()
    sys.exit()


def check_if_dead():
    if (pos_block.x > block_width_number - 1
            or pos_block.x < 0
            or pos_block.y > block_height_number - 1
            or pos_block.y < 0
            or (pos.x, pos.y) in snake):
        guess_ill_die()


def check_for_apple():
    if apples[int(pos_block.x)][int(pos_block.y)]:
        grow()
        apples[int(pos_block.x)][int(pos_block.y)] = False

        # choosing a new apple location
        new_x = random.randint(0, block_width_number - 1)
        new_y = random.randint(0, block_height_number - 1)
        apples[new_x][new_y] = True
        gfxdraw.filled_circle(display, new_x * unit + int(unit / 2),
                              new_y * unit + int(unit / 2), int(3 * unit / 8), RED)
        gfxdraw.aacircle(display, new_x * unit + int(unit / 2),
                         new_y * unit + int(unit / 2), int(3 * unit / 8), RED)


def grow():
    global length
    length += 1


def move_body():
    match direction:
        case 1:
            snake.insert(0, (pos.x, pos.y + unit))
        case 2:
            snake.insert(0, (pos.x - unit, pos.y))
        case 3:
            snake.insert(0, (pos.x, pos.y - unit))
        case 4:
            snake.insert(0, (pos.x + unit, pos.y))
    if len(snake) >= length:
        x = snake[len(snake) - 1][0]
        y = snake[len(snake) - 1][1]
        rect = pygame.Rect(x, y, unit, unit)
        pygame.draw.rect(display, DARK_GREEN if ((x + y) / unit) % 2 == 0 else LIGHT_GREEN, rect)
        pygame.display.flip()
        snake.pop()
    for position in snake:
        body = pygame.Rect(position[0], position[1], unit, unit)
        pygame.draw.rect(display, (18, 117, 22), body)


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

draw_grid()

# forever loop
while True:
    # frame clock ticking
    clock.tick(fps)

    # draw stuff once per second
    if frame == fps_per_frequency:
        # updating player's drawn position
        match direction:
            case 1:
                pos.y -= unit
            case 2:
                pos.x += unit
            case 3:
                pos.y += unit
            case 4:
                pos.x -= unit

        # updating pos_block with pos
        pos_block.x = int(pos.x / unit)
        pos_block.y = int(pos.y / unit)

        move_body()

        # draw player
        direction_for_tick = direction
        player = pygame.Rect(pos.x, pos.y, unit, unit)
        pygame.draw.rect(display, "red", player)

        # checking if player has to die or grow
        check_if_dead()
        check_for_apple()

        frame = 0
        ticks = pygame.time.get_ticks()

    frame += 1

    # movement
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and direction_for_tick != 3:
        direction = 1
    elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and direction_for_tick != 1:
        direction = 3
    elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and direction_for_tick != 2:
        direction = 4
    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and direction_for_tick != 4:
        direction = 2

    if keys[pygame.K_LSHIFT]:
        frequency = 2
        frame = fps_per_frequency
    else:
        frequency = 1

    pygame.display.flip()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

