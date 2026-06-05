# Mustafa Ali
# Battleship - Assignment 2
# Block 5
# 24th May

# This program is my own work - MA

# Consider any possible problems or limitations pertaining to this program.
# What are they? Make the necessary modifications.
#
# A problem that I came across was

import pygame, sys, random
import os
import platform

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
