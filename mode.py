import pygame
import random
import copy
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors for different blocks
COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [0, 1, 0]]
]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Function to draw the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, (100, 100, 100), (0, y), (SCREEN_WIDTH, y))

# Function to draw a shape
def draw_shape(shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[row]):
            if shape[row][col]:
                pygame.draw.rect(screen, color, (x + col * BLOCK_SIZE, y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to check if a shape can be placed at a specific position
def is_valid_position(shape, x, y, grid):
    for row in range(len(shape)):
        for col in range(len(shape[row]):
            if shape[row][col]:
                if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT:
                    return False
                if grid[y + row][x + col]:
                    return False
    return True

# Function to remove completed rows
def remove_completed_rows(grid):
    rows_to_remove = []
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            rows_to_remove.append(row)
    for row in rows_to_remove:
        del grid[row]
        grid.insert(0, [0] * GRID_WIDTH)

# Function to rotate a shape by a given angle (in degrees)
def rotate_shape(shape, angle):
    if angle == 0:
        return shape
    elif angle == 90:
        return [[shape[j][i] for j in range(len(shape))] for i in range(len(shape[0]))]
    elif angle == 180:
        return [[shape[i][j] for j in reversed(range(len(shape[0])))] for i in reversed(range(len(shape))]
    elif angle == 270:
        return [[shape[j][i] for j in reversed(range(len(shape)))] for i in range(len(shape[0]))]

# Main game loop
def main():
    clock = pygame.time.Clock()
    game_over = False
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    current_shape = random.choice(SHAPES)
    x, y = GRID_WIDTH // 2 - 1, 0
    shape_color = random.choice(COLORS)
    fall_time = 0
    fall_speed = 1  # Adjust this value to control the fall speed (higher values make it slower)

    rotation_angle = 0
    rotate_cooldown = 0
    rotate_delay = 200  # Delay between rotations (in milliseconds)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if is_valid_position(current_shape, x - 1, y, grid):
                        x -= 1
                elif event.key == pygame.K_RIGHT:
                    if is_valid_position(current_shape, x + 1, y, grid):
                        x += 1
                elif event.key == pygame.K_DOWN:
                    if is_valid_position(current_shape, x, y + 1, grid):
                        y += 1
                elif event.key == pygame.K_UP:
                    # Rotate the shape
                    if rotate_cooldown <= 0:
                        rotation_angle = (rotation_angle + 90) % 360
                        rotated_shape = rotate_shape(current_shape, rotation_angle)
                        if is_valid_position(rotated_shape, x, y, grid):
                            current_shape = rotated_shape
                        rotate_cooldown = rotate_delay

        # Automatic falling
        fall_time += clock.get_rawtime()
        if fall_time > fall_speed:
            if is_valid_position(current_shape, x, y + 1, grid):
                y += 1
            else:
                for row in range(len(current_shape)):
                    for col in range(len(current_shape[row]):
                        if current_shape[row][col]:
                            grid[y + row][x + col] = 1
                remove_completed_rows(grid)
                current_shape = random.choice(SHAPES)
                x, y = GRID_WIDTH // 2 - 1, 0
                shape_color = random.choice(COLORS)
                rotation_angle = 0
            fall_time = 0

        screen.fill((0, 0, 0))
        draw_grid()
        draw_shape(current_shape, x * BLOCK_SIZE, y * BLOCK_SIZE, shape_color)
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if grid[row][col]:
                    pygame.draw.rect(screen, (255, 255, 255), (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.update()
        clock.tick(60)  # Adjust the frame rate as needed

        if rotate_cooldown > 0:
            rotate_cooldown -= clock.get_rawtime()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
