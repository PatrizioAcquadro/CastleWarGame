import pygame

# gui
WIDTH = 1400
HEIGHT = 600
WALL_POS = 320
WALL_WIDTH = 150
WALL_HEIGHT = 150
MINE_POS = 40
MINE_WIDTH = 116
MINE_HEIGHT = 74
BARRACKS_POS = 165
BARRACKS_WIDTH = 150
BARRACKS_HEIGHT = 90
TOWER_HEIGHT = 160

# Units
# worker
W_COST = 1
W_TRAIN = 2
W_SPEED = 250
W_PROD = 1
W_REPAIR = 1

# swordsman
S_COST = 5
S_TRAIN = 3
S_SPEED = 220
S_RANGE = 15
S_HIT = 10
S_REST = 1
S_HEALTH = 40

# archer
A_COST = 5
A_TRAIN = 3
A_SPEED = 190
A_RANGE = 100
A_REST = 2
A_HEALTH = 25
A_HIT = 7

# Buildings
INIT_RESOURCES = 15
WALL_HEALTH = 50

TOWER_RANGE = 250
TOWER_HIT = 8
TOWER_REST = 2
ARROW_SPEED = 15
ARROW_HIT = 7

# Command
P1_MINE = pygame.K_a
P1_WALL = pygame.K_s
P1_S_ATTACK = pygame.K_d
P1_A = pygame.K_f
P1_W_TRAIN = pygame.K_q
P1_S_TRAIN = pygame.K_w
P1_A_TRAIN = pygame.K_e
P1_UNLEASH = pygame.K_z

P2_MINE = pygame.K_l
P2_WALL = pygame.K_k
P2_S_ATTACK = pygame.K_j
P2_A = pygame.K_h
P2_W_TRAIN = pygame.K_p
P2_S_TRAIN = pygame.K_o
P2_A_TRAIN = pygame.K_i
P2_UNLEASH = pygame.K_m

PAUSE = pygame.K_SPACE
SAVE = pygame.K_v
LOAD = pygame.K_b