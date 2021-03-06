import sys
import pygame
import time
from win32api import GetSystemMetrics
import random
import math


# Initalize modules
pygame.init()
pygame.display.set_caption("Snake_Mańczak")
myfont = pygame.font.SysFont('Arial', 30)

# pygame.display.set_icon(pygame.image.load('Path_to_icon'))


# Set the window size to a rectangle where the lenght of a side is equal to half of the curents screen's height
window_size = window_width, window_height = int(
    GetSystemMetrics(1)/2), int(GetSystemMetrics(1)/2)

# Size of displayed blocks
snake_block_dimensions = 20, 20

# Snake's colour
#     R   G   B
skin_colour = 0, 255, 0

# Create new window
screen = pygame.display.set_mode(window_size)


class snake_block:  # Class that handles single snake element
    def __init__(self, var_pos_x, var_pos_y):
        self.pos_x = var_pos_x
        self.pos_y = var_pos_y
        self.snake_block = pygame.Rect(
            self.pos_x, self.pos_y, snake_block_dimensions[0], snake_block_dimensions[1])

    def draw(self):  # Draw element onto the screen
        pygame.draw.rect(screen, skin_colour, self.snake_block)

    def move(self, speed):  # Move and update blocks position
        self.snake_block = self.snake_block.move(speed[0], speed[1])
        self.pos_x = self.pos_x+speed[0]
        self.pos_y = self.pos_y+speed[1]
        # Teleport on edge
        if self.snake_block.left < 0:  # left to right
            self.snake_block = pygame.Rect(
                window_width-(snake_block_dimensions[0]+1), self.snake_block.top, snake_block_dimensions[0], snake_block_dimensions[1])
            self.pos_x = window_width-(snake_block_dimensions[0]+1)
            self.pos_y = self.snake_block.top
        elif self.snake_block.right > window_width:  # right to left
            self.snake_block = pygame.Rect(
                0, self.snake_block.top, snake_block_dimensions[0], snake_block_dimensions[1])
            self.pos_x = 0
            self.pos_y = self.snake_block.top
        if self.snake_block.top < 0:  # top to bottom
            self.snake_block = pygame.Rect(
                self.snake_block.left, window_height-(snake_block_dimensions[1]+1), snake_block_dimensions[0], snake_block_dimensions[1])
            self.pos_x = self.snake_block.left
            self.pos_y = window_height-(snake_block_dimensions[1]+1)
        elif self.snake_block.bottom > window_height:  # bottom to top
            self.snake_block = pygame.Rect(
                self.snake_block.left, 0, snake_block_dimensions[0], snake_block_dimensions[1])
            self.pos_x = self.snake_block.left
            self.pos_y = 0

    def follow(self, var_pos_x, pos_y):  # Move block to given cords
        self.pos_x = var_pos_x
        self.pos_y = pos_y
        self.snake_block = pygame.Rect(
            self.pos_x, self.pos_y, snake_block_dimensions[0], snake_block_dimensions[1])


wonsz = []


class Apple:  # Class that handles apple
    def __init__(self):
        # Rand apple's position, and make sure, that it is on snake's jump multipy
        self.pos_x = (
            (random.randint(25, window_width-(snake_block_dimensions[0]+10)))//speed_multiplier)*speed_multiplier
        self.pos_y = (random.randint(
            25, window_height-(snake_block_dimensions[1]+10))//speed_multiplier)*speed_multiplier

        self.apple_block = pygame.Rect(
            self.pos_x, self.pos_y, snake_block_dimensions[0], snake_block_dimensions[1])

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.apple_block)


# Game parameters
speed_multiplier = 20  # Has to be positive
speed = [speed_multiplier, 0]

game_over = False
# Create first snake block and fitst apple
wonsz.append(snake_block(20, 20))
apple = Apple()


while not game_over:
    for event in pygame.event.get():  # Arrow's control handler
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and speed[0] == 0:
                #print("K_LEFT")
                speed = [-1*speed_multiplier, 0]

            if event.key == pygame.K_RIGHT and speed[0] == 0:
                #print("K_RIGHT")
                speed = [speed_multiplier, 0]

            if event.key == pygame.K_UP and speed[1] == 0:
                #print("K_UP")
                speed = [0, -1*speed_multiplier]

            if event.key == pygame.K_DOWN and speed[1] == 0:
                #print("K_DOWN")
                speed = [0, speed_multiplier]

            if event.key == pygame.K_SPACE:
                #print("K_SPACE")
                wonsz.append(snake_block(wonsz[0].pos_x, wonsz[0].pos_y))
    # clear the screen
    screen.fill((0, 0, 0))

    apple.draw()

    # Draw and follow elements
    for obj in reversed(range(len(wonsz))):

        wonsz[obj].draw()
        
        if obj != 0:
            wonsz[obj].follow(wonsz[obj-1].pos_x, wonsz[obj-1].pos_y)
            if obj>2 and math.hypot(wonsz[0].pos_x-wonsz[obj].pos_x, wonsz[0].pos_y- wonsz[obj].pos_y) < (snake_block_dimensions[0]-2):
                game_over = True

    
    # Make a move
    wonsz[0].move(speed)

    textsurface = myfont.render(
        'Score: '+str(len(wonsz)-1), False, (255, 255, 255))
    screen.blit(textsurface, (0, 0))

    pygame.display.flip()
    time.sleep(0.1)

    # If the snake is inside the apple, delete the apple, spawn the new one, and append the snake.
    if math.hypot(wonsz[0].pos_x-apple.pos_x, wonsz[0].pos_y-apple.pos_y) < (snake_block_dimensions[0]-2):
        del apple
        while True:
            apple = Apple()
            allgood = True
            for obj in reversed(range(len(wonsz))):
                 if math.hypot(wonsz[obj].pos_x-apple.pos_x, wonsz[obj].pos_y-apple.pos_y) < (snake_block_dimensions[0]-2):
                     del apple
                     apple = Apple()
                     allgood = False
            if allgood:
                break


        wonsz.append(snake_block(wonsz[0].pos_x, wonsz[0].pos_y))


screen.fill((0, 0, 0))
textsurface = myfont.render(
        'GAME OVER', False, (255, 255, 255))
screen.blit(textsurface, ((window_width/2)-60, window_height/2))
pygame.display.flip()
time.sleep(5)
