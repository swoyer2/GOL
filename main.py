import pygame
import random

import grid

WIDTH = 720
HEIGHT = 720
FPS = 30
GRID_SIZE = (16, 16)

WHITE = (255, 255, 250)
BLACK = (0, 15, 66)
PINK = (255, 36, 215)
BLUE = (138, 255, 206)

pygame.init()
pygame.mixer.init()  # For sound
pygame.font.init()
font = pygame.font.SysFont('Arial', 60)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GOL")
clock = pygame.time.Clock()

# Grid
game_grid = grid.Grid(GRID_SIZE)
seed = ''.join(str(random.randint(0, 2)) for _ in range(32*32))
game_grid.set_seed("1001001101111010101011001001001101100001100010000110111110100010110010110000110001111000011110110101011101001110110100001111011100000001010000101110100110000101100101001101010000010110101110110001011010101011110000000000010111100101111101110101111111100101")

# group all the sprites together for ease of update
all_sprites = pygame.sprite.Group(*game_grid.get_all_squares())

update_interval = 50  # milliseconds (0.05 seconds)
last_update = pygame.time.get_ticks()

running = True
paused = True
current_iteration = 0
while running:
    clock.tick(FPS)
    text_surface = font.render(f'Iteration: {current_iteration}', False, (0, 0, 0))
    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            clicked_square_x, clicked_square_y = game_grid.get_square_pos_from_mouse(mouse_pos)
            if clicked_square_x != None:
                game_grid.rotate_state(clicked_square_x, clicked_square_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_r:
                game_grid.reload()
                all_sprites = pygame.sprite.Group(*game_grid.get_all_squares())
            if event.key == pygame.K_e:
                game_grid.clear_board()
                current_iteration = 0
            if event.key == pygame.K_RIGHT:
                current_iteration += 1
                if game_grid.is_repeating_seed():
                    print("Repeating!")
                game_grid.set_new_board_state()

    if current_time - last_update >= update_interval and not paused:
        current_iteration += 1
        if game_grid.is_repeating_seed():
            print("Repeating!")
        game_grid.set_new_board_state()
        last_update = current_time

    all_sprites.update()

    screen.fill(WHITE)
    
    all_sprites.draw(screen)
    screen.blit(text_surface, (200, 20))

    pygame.display.flip()       

pygame.quit()