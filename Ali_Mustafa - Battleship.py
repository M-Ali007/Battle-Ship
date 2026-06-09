# Mustafa Ali
# Battleship - Assignment 2
# Block 5
# 1st June

# This program is my own work - MA

# Consider any possible problems or limitations pertaining to this program.
# What are they? Make the necessary modifications.
#
# Problems / Limitations:
# 1. No restart — once the game is won the player has to close and reopen the program to play again.
# 2. No partial ship feedback — the player doesn't know how many ships they've found until all 9 cells are hit.
# 3. The random ship placement loop could theoretically spin for a long time on a crowded board,
#    though with only 3 ships on a 7x7 grid this is unlikely in practice.


import pygame, sys, random
import os
import platform

# --- GAME STATE ---
hits = 0          # number of ship cells found
moves = 0         # total clicks made
clicked_cells = {}  # (row, col) -> "hit" or "miss"
game_won = False
win_start_time = 0

# 7x7 grid — integers are empty water, strings like "X1" mark ship cells
grid = {
    1:[1,2,3,4,5,6,7],
    2:[1,2,3,4,5,6,7],
    3:[1,2,3,4,5,6,7],
    4:[1,2,3,4,5,6,7],
    5:[1,2,3,4,5,6,7],
    6:[1,2,3,4,5,6,7],
    7:[1,2,3,4,5,6,7]
}

# Linux needs an explicit video driver before pygame.init()
if platform.system() == "Linux":
    os.environ["SDL_VIDEODRIVER"] = "x11"
    os.environ["SDL_VIDEO_HIGHDPI_ENABLED"] = "0"

pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

game_font = pygame.font.Font('Impacted.ttf', 40)
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


def setShips():
    # place 3 ships of length 3, no overlapping, random direction each
    for i in range(1, 4):
        direction = random.randint(0, 3)
        match direction:
            case 0: # going up
                while True:
                    Rx = random.choice(range(1, 8))
                    Ry = random.choice(range(3, 8))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry - 1][Rx - 1], int) and isinstance(grid[Ry - 2][Rx - 1], int):
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry - 1][Rx - 1] = f"X{i}"
                        grid[Ry - 2][Rx - 1] = f"X{i}"
                        break

            case 1: # going right
                while True:
                    Rx = random.choice(range(1, 6))
                    Ry = random.choice(range(1, 8))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry][Rx], int) and isinstance(grid[Ry][Rx + 1], int):
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry][Rx] = f"X{i}"
                        grid[Ry][Rx + 1] = f"X{i}"
                        break

            case 2: # going left
                while True:
                    Rx = random.choice(range(3, 8))
                    Ry = random.choice(range(1, 8))
                    if isinstance(grid[Ry][Rx - 1], int) and isinstance(grid[Ry][Rx - 2], int) and isinstance(grid[Ry][Rx - 3], int):
                        grid[Ry][Rx - 1] = f"X{i}"
                        grid[Ry][Rx - 2] = f"X{i}"
                        grid[Ry][Rx - 3] = f"X{i}"
                        break

            case 3: # going down
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


setShips()
rects = makeRects()  # built once — positions never change

# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
