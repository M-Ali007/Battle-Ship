# Mustafa Ali
# Battleship - Assignment 2
# Block 5
# 1st June

# This program is my own work - MA

# Consider any possible problems or limitations pertaining to this program.
# What are they? Make the necessary modifications.
#
# A problem that I came across was

import pygame, sys, random
import os
import platform

# GAME VARS
hits = 0
tries = 0
grid = {
    1:[1,2,3,4,5,6,7],
    2:[1,2,3,4,5,6,7],
    3:[1,2,3,4,5,6,7],
    4:[1,2,3,4,5,6,7],
    5:[1,2,3,4,5,6,7],
    6:[1,2,3,4,5,6,7],
    7:[1,2,3,4,5,6,7]
}

if platform.system() == "Linux":
    os.environ["SDL_VIDEODRIVER"] = "x11"
    os.environ["SDL_VIDEO_HIGHDPI_ENABLED"] = "0"

pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

game_font = pygame.font.Font('Impacted.ttf',40)
title_surface = game_font.render("BATTLESHIP", True, (255,255,255))
title_rect = title_surface.get_rect(center = (450, 25))

def makeLines():
    for i in range(100, 900, 100):
        pygame.draw.line(screen, [0,0,0], (i, 100), (i, 800), 2)
    for i in range(100, 900, 100):
        pygame.draw.line(screen, [0,0,0], (100, i), (800, i), 2)

def makeRects():
    gridRects = []
    for x in range(100, 800, 100):
        for y in range(100, 800, 100):
            cellRect = pygame.Rect(x, y, 100, 100)
            gridRects.append(cellRect)
    return gridRects

def setShips():
    for i in range(1,4):
        direction = random.randint(0,3)
        match direction:
            case 0: # going up
                while True:
                    Rx = random.choice(range(1,8))
                    Ry = random.choice(range(3,8))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry - 1][Rx - 1], int) and isinstance(grid[Ry - 2][Rx - 1], int):
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry - 1][Rx - 1] = f"X{i}"
                        grid[Ry - 2][Rx - 1] = f"X{i}" 
                        break


            case 1: # going right
                while True:
                    Rx = random.choice(range(1,6))
                    Ry = random.choice(range(1,8))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry][Rx], int) and isinstance(grid[Ry][Rx + 1], int):
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry][Rx] = f"X{i}"
                        grid[Ry][Rx + 1] = f"X{i}" 
                        break

            case 2: # going left
                while True:
                    Rx = random.choice(range(3,8))
                    Ry = random.choice(range(1,8))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry][Rx - 2], int) and isinstance(grid[Ry][Rx - 3], int):
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry][Rx - 2] = f"X{i}"
                        grid[Ry][Rx - 3] = f"X{i}" 
                        break

            case 3: # going down
                while True:
                    Rx = random.choice(range(1,8))
                    Ry = random.choice(range(1,6))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry + 1][Rx - 1], int) and isinstance(grid[Ry + 2][Rx - 1], int):                    
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry + 1][Rx - 1] = f"X{i}"
                        grid[Ry + 2][Rx - 1] = f"X{i}" 
                        break
    for row in grid:
        print(row, grid[row])

setShips()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouseP = pygame.mouse.get_pos()

    screen.fill([0,0,0])
    pygame.draw.rect(screen, [100, 100, 255], (50, 50, 800, 800))
    screen.blit(title_surface, title_rect)
    makeLines()
    rects = makeRects()
    for cell in rects:
        if cell.collidepoint(mouseP):
            pygame.draw.circle(screen, (255, 50, 0), (cell.x + 50, cell.y + 50), 40, 2)

    pygame.display.update()
    clock.tick(240)
    pygame.display.set_caption(f"FPS: {int(clock.get_fps())}")
