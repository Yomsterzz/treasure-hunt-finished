import pygame
pygame.init()
import random
import time
import sys

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Hunt")

clock = pygame.time.Clock()
grid_size = 20
cell_size = WIDTH//grid_size
fps = 30
obstacle_num = 25

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (76, 210, 90)
RED = (186, 45, 11)
BLUE = (5, 142, 217)

treasure_pos = []
obstacle_pos = []
player_pos = [grid_size//2, grid_size//2]
score = 0

def draw_grid():
    for x in range(0,WIDTH, cell_size):
        pygame.draw.line(screen, WHITE, (x,0), (x,HEIGHT))
    
    for y in range(0,HEIGHT, cell_size):
        pygame.draw.line(screen, WHITE, (0,y), (WIDTH,y))
        
def draw_player():
    pygame.draw.rect(screen, BLUE, (player_pos[0]*cell_size, player_pos[1]*cell_size, cell_size, cell_size))
    
def draw_treasures():
    for pos in treasure_pos:
        pygame.draw.rect(screen, GREEN, (pos[0]*cell_size, pos[1]*cell_size, cell_size, cell_size))

def draw_obstacles():
    for pos in obstacle_pos:
        pygame.draw.rect(screen, RED, (pos[0]*cell_size, pos[1]*cell_size, cell_size, cell_size))
        
def check_treasure_col():
    for t_pos in treasure_pos:
        if player_pos == t_pos:
            treasure_pos.remove(t_pos)
            return True
    
    return False

def restart_game():
    global player_pos, obstacle_pos, treasure_pos, score
    player_pos = [grid_size//2, grid_size//2]
    treasure_pos = [[random.randint(0,grid_size-1), random.randint(0,grid_size-1)] for i in range(1,3)]
    obstacle_pos = []
    while len(obstacle_pos) < obstacle_num:
        pos = [random.randint(0,grid_size-1), random.randint(0,grid_size-1)]
        if pos != player_pos and pos not in treasure_pos and pos not in obstacle_pos:
            obstacle_pos.append(pos)
    score = 0

restart_game()

while True:
    screen.fill(BLACK)
    draw_grid()
    draw_player()
    draw_treasures()
    draw_obstacles()
    clock.tick(fps)
    pygame.display.flip()
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= 1
    
    if keys[pygame.K_d] and player_pos[0] < grid_size-1:
        player_pos[0] += 1
    
    if keys[pygame.K_w] and player_pos[1] > 0:
        player_pos[1] -= 1
    
    if keys[pygame.K_s] and player_pos[1] < grid_size-1:
        player_pos[1] += 1
        
    if check_treasure_col():
        score += 1
        if len(treasure_pos) == 0:
            restart_game()
            #message = You win!
    
    if player_pos in obstacle_pos:
        restart_game()
        #message = Game over.
    
    font = pygame.font.Font()
    score_text = font.render("Score: {}".format(score), False, WHITE)
    score_rect = score_text.get_rect(center = (WIDTH//2, 20))
    screen.blit(score_text, score_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()