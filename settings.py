import pygame
from castles_war_constants import *

pygame.init()

clock = pygame.time.Clock()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player War")

# display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player War")

#fonts
font = pygame.font.SysFont("sans", 40)
small = pygame.font.SysFont("cambria", 20)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED= (255, 0, 0)
GREEN = (0, 255, 0)

# player 1
BARRACKS1 = pygame.transform.scale(pygame.image.load(f"images/player1/barracks.png"), (BARRACKS_WIDTH, BARRACKS_HEIGHT))
BARRACKS2 = pygame.transform.scale(pygame.image.load(f"images/player2/barracks.png"), (BARRACKS_WIDTH, BARRACKS_HEIGHT))
MINE1 = pygame.transform.scale(pygame.image.load(f"images/player1/mine.png"), (MINE_WIDTH, MINE_HEIGHT))
MINE2 = pygame.transform.scale(pygame.image.load(f"images/player2/mine.png"), (MINE_WIDTH, MINE_HEIGHT))
CASTLE1 = pygame.transform.scale(pygame.image.load(f"images/player1/castle.png"), (WALL_WIDTH, WALL_HEIGHT))
CASTLE2 = pygame.transform.scale(pygame.image.load(f"images/player2/castle.png"), (WALL_WIDTH, WALL_HEIGHT))

BG = pygame.transform.scale(pygame.image.load(f"images/bg.jpg"), (WIDTH, HEIGHT))

ARROW = pygame.image.load("images/arrow.png")

# helper functions
def load_img(img):
    return pygame.image.load(img)

def get_turn():
    with open("game.txt", "r") as f:
        for line in f:
            if line.lower().strip().split(" ")[0] == "turn":
                turn = int(line.strip().split(" ")[1])
                return turn
    return 0