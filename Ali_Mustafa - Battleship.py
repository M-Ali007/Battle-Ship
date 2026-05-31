# Mustafa Ali
# Battleship - Assignment 2
# Block 5
# 24th May

# This program is my own work - MA

# Consider any possible problems or limitations pertaining to this program.
# What are they? Make the necessary modifications.
#
# A problem that I came across was #TODO

import pygame, sys, random
import os
import platform

if platform.system() == "Linux":
    os.environ["SDL_VIDEODRIVER"] = "x11"
    os.environ["SDL_VIDEO_HIGHDPI_ENABLED"] = "0"

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

bg_surface = pygame.image.load("assets/background-day.png")
bg_surface = pygame.transform.scale2x(bg_surface)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg_surface, (0, 0))

    pygame.display.update()
    clock.tick(240)
    pygame.display.set_caption(f"FPS: {int(clock.get_fps())}")
