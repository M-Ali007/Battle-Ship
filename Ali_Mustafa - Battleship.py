# Mustafa Ali
# Battleship - Assignment 2
# Block 5
# 1st June

# This program is my own work - MA

# Consider any possible problems or limitations pertaining to this program.
# What are they? Make the necessary modifications.
#
# Problems found and fixed:
# 1. Ships could overlap — fixed by checking that all 3 target cells are still integers
#    before placing a ship, so no ship can overwrite another.
# 2. Clicking the same cell twice would count the move twice — fixed by checking
#    (row, col) not in clicked_cells before registering a click.
# 3. makeRects() was called every frame, creating 49 new objects 240 times a second —
#    fixed by moving it outside the loop so the list is built once and reused.
# 4. Ship placement could go out of bounds — fixed by constraining the random ranges
#    per direction (e.g. rows 3-7 only when going up, so row-2 is always valid).
#
# -------------------------------------------------------------------
# PSEUDOCODE
# -------------------------------------------------------------------
# SET UP grid as 7x7 dictionary, all cells = empty water
# PLACE 3 ships:
#     FOR each ship:
#         PICK a random direction (up / right / down / left)
#         LOOP until valid spot found (no overlap, within bounds):
#             PICK random starting cell
#             IF all 3 cells are empty -> mark them as ship, BREAK
#
# BUILD list of cell Rects (drawn once, reused every frame)
#
# LOOP forever:
#     IF user closes window -> QUIT
#     IF R key pressed -> reset all state and place new ships
#     IF left click AND game not won:
#         FIND which cell was clicked
#         IF cell not already clicked:
#             IF cell contains a ship -> record HIT, increment hits
#             ELSE -> record MISS
#             INCREMENT move counter
#             IF hits == 9 -> SET game_won, record win time
#     DRAW background, title, grid lines
#     IF game_won:
#         CALCULATE how many rows to colour green (based on time elapsed)
#         DRAW green rows top to bottom
#         SHOW "PRESS R TO RESTART" prompt
#     ELSE:
#         DRAW hit/miss markers on clicked cells
#         DRAW hover ring on cell under mouse
#     DRAW moves counter box (top right)
#     UPDATE display

import pygame, sys, random
import os
import platform

# Linux needs an explicit video driver before pygame.init()
if platform.system() == "Linux":
    os.environ["SDL_VIDEODRIVER"] = "x11"
    os.environ["SDL_VIDEO_HIGHDPI_ENABLED"] = "0"

pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

game_font = pygame.font.Font('Impacted.ttf', 40)
small_font = pygame.font.Font('Impacted.ttf', 28)
title_surface = game_font.render("BATTLESHIP", True, (255, 255, 255))
title_rect = title_surface.get_rect(center=(450, 25))


def makeLines():
    # vertical and horizontal grid lines inside the play area
    for i in range(100, 900, 100):
        pygame.draw.line(screen, [0, 0, 0], (i, 100), (i, 800), 2)
    for i in range(100, 900, 100):
        pygame.draw.line(screen, [0, 0, 0], (100, i), (800, i), 2)


def makeRects():
    # one Rect per cell — outer loop is x (col), inner is y (row)
    gridRects = []
    for x in range(100, 800, 100):
        for y in range(100, 800, 100):
            cellRect = pygame.Rect(x, y, 100, 100)
            gridRects.append(cellRect)
    return gridRects


def makeGrid():
    # fresh 7x7 grid — integers are empty water, strings like "X1" mark ship cells
    return {r: [1, 2, 3, 4, 5, 6, 7] for r in range(1, 8)}


def setShips(grid):
    # place 3 ships of length 3, no overlapping, random direction each
    for i in range(1, 4):
        direction = random.randint(0, 3)
        match direction:
            case 0: # going up — start row >= 3 so row-2 stays in bounds
                while True:
                    Rx = random.choice(range(1, 8))
                    Ry = random.choice(range(3, 8))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry - 1][Rx - 1], int) and isinstance(grid[Ry - 2][Rx - 1], int):
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry - 1][Rx - 1] = f"X{i}"
                        grid[Ry - 2][Rx - 1] = f"X{i}"
                        break

            case 1: # going right — start col <= 5 so col+2 stays in bounds
                while True:
                    Rx = random.choice(range(1, 6))
                    Ry = random.choice(range(1, 8))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry][Rx], int) and isinstance(grid[Ry][Rx + 1], int):
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry][Rx] = f"X{i}"
                        grid[Ry][Rx + 1] = f"X{i}"
                        break

            case 2: # going left — start col >= 3 so col-2 stays in bounds
                while True:
                    Rx = random.choice(range(3, 8))
                    Ry = random.choice(range(1, 8))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry][Rx - 2], int) and isinstance(grid[Ry][Rx - 3], int):
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry][Rx - 2] = f"X{i}"
                        grid[Ry][Rx - 3] = f"X{i}"
                        break

            case 3: # going down — start row <= 5 so row+2 stays in bounds
                while True:
                    Rx = random.choice(range(1, 8))
                    Ry = random.choice(range(1, 6))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry + 1][Rx - 1], int) and isinstance(grid[Ry + 2][Rx - 1], int):
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry + 1][Rx - 1] = f"X{i}"
                        grid[Ry + 2][Rx - 1] = f"X{i}"
                        break
    for row in grid:
        print(row, grid[row])
    return grid


def resetGame():
    # wipe all state and place fresh ships
    g = makeGrid()
    setShips(g)
    return g, 0, 0, {}, False, 0


# --- INITIAL SETUP ---
grid = makeGrid()
setShips(grid)
hits = 0
moves = 0
clicked_cells = {}
game_won = False
win_start_time = 0

rects = makeRects()  # built once — positions never change

restart_surface = small_font.render("PRESS R TO RESTART", True, (255, 255, 255))
restart_rect = restart_surface.get_rect(center=(450, 840))

# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            grid, hits, moves, clicked_cells, game_won, win_start_time = resetGame()

        # left click — only register new cells, stop accepting clicks after win
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_won:
            for cell in rects:
                if cell.collidepoint(event.pos):
                    col = cell.x // 100  # rect x=100 -> col 1, x=200 -> col 2, etc.
                    row = cell.y // 100  # same mapping for rows
                    if (row, col) not in clicked_cells:
                        if isinstance(grid[row][col - 1], str):
                            clicked_cells[(row, col)] = "hit"
                            hits += 1
                        else:
                            clicked_cells[(row, col)] = "miss"
                        moves += 1
                        if hits == 9:  # all 3 ships (3 cells each) found
                            game_won = True
                            win_start_time = pygame.time.get_ticks()
                    break

    mouseP = pygame.mouse.get_pos()

    # --- DRAW ---
    screen.fill([0, 0, 0])
    pygame.draw.rect(screen, [100, 100, 255], (50, 50, 800, 800))  # blue play area
    screen.blit(title_surface, title_rect)

    # win animation: sweep green across the grid top-to-bottom, one row every 200ms
    if game_won:
        elapsed = pygame.time.get_ticks() - win_start_time
        green_rows = min(7, elapsed // 200)
        for row in range(1, green_rows + 1):
            for col in range(1, 8):
                pygame.draw.rect(screen, (50, 200, 50), pygame.Rect(col * 100, row * 100, 100, 100))
        # show restart prompt once animation finishes
        if green_rows == 7:
            box = restart_rect.inflate(16, 8)
            pygame.draw.rect(screen, (30, 30, 80), box, border_radius=6)
            screen.blit(restart_surface, restart_rect)

    # draw hit/miss markers (hidden during win animation)
    if not game_won:
        for (row, col), result in clicked_cells.items():
            cx = col * 100 + 50
            cy = row * 100 + 50
            if result == "hit":
                pygame.draw.circle(screen, (255, 50, 50), (cx, cy), 40)
            else:
                pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 40, 3)

        # hover ring — only on unclicked cells
        for cell in rects:
            col = cell.x // 100
            row = cell.y // 100
            if cell.collidepoint(mouseP) and (row, col) not in clicked_cells:
                pygame.draw.circle(screen, (255, 50, 0), (cell.x + 50, cell.y + 50), 40, 2)

    makeLines()

    # moves counter with a dark box behind it
    moves_surface = game_font.render(f"MOVES: {moves}", True, (255, 255, 255))
    moves_display_rect = moves_surface.get_rect(topright=(875, 10))
    box_rect = moves_display_rect.inflate(16, 8)  # 8px padding each side
    pygame.draw.rect(screen, (30, 30, 80), box_rect, border_radius=6)
    screen.blit(moves_surface, moves_display_rect)

    pygame.display.update()
    clock.tick(240)
    pygame.display.set_caption(f"FPS: {int(clock.get_fps())}")
