#UTTINI_LORENZO_502183
#ACQUADRO_PATRIZIO_502311
import pygame, sys
from pygame import K_SPACE, KEYDOWN, MOUSEBUTTONDOWN, QUIT

from settings import *
from objects import *
from castles_war_constants import *

player1 = Player(0, HEIGHT)
player2 = Player2(WIDTH // 1.45, HEIGHT)
player1.load("game.txt")
player2.load("game.txt")

_font = pygame.font.SysFont('cambria', 45)
pause = _font.render("Pause", True, BLACK)
turn = get_turn()
turnfont = pygame.font.SysFont('cambria', 55)
turnSurf = turnfont.render(f"Turn: {turn}", True, BLACK)
player1_input = player2_input = False
p1_moved = p2_moved = False
game_over = finished = False

def display():
    win.fill(WHITE)
    win.blit(BG, (0, 0))
    player1.display(win)
    player2.display(win)
    win.blit(turnSurf, (WIDTH / 2 - turnSurf.get_width() / 2, 0))
    pygame.display.update()

while 1 and not finished:
    clock.tick(60)

    if player1_input and player2_input:
        if not p1_moved:
            targets = [player2.wall] + player2.attackers
            p1_moved = player1.move_troops(targets)
        if not p2_moved:
            targets = [player1.wall] + player1.attackers
            p2_moved = player2.move_troops(targets)
        if p1_moved and p2_moved:
            p1_combat_f = player1.troop_attack(player2.attackers)
            p2_combat_f = player2.troop_attack(player1.attackers)
            if p1_combat_f and p2_combat_f and player1.animate() and player2.animate():
                player1.remove_dead()
                player2.remove_dead()
                player1.run_buildings()
                player2.run_buildings()
                player1.decrease_cooldown()
                player2.decrease_cooldown()
                player1.deanimate()
                player2.deanimate()

                p1_moved = p2_moved = False
                player1_input = player2_input = False
                turn += 1
                turnSurf = turnfont.render(f"Turn: {turn}", True, BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            finished = True
        if event.type == KEYDOWN:
            if not player1_input:
                player1_input = True
                if event.key == P1_W_TRAIN:
                    player1.buy("worker")
                elif event.key == P1_S_TRAIN:
                    player1.buy("swordsman")
                elif event.key == P1_A_TRAIN:
                    player1.buy("archer")
                elif event.key == P1_MINE:
                    if not player1.to_mine():
                        player1.redirect_troop("mine")
                elif event.key == P1_WALL:
                    if not player1.to_wall():
                        player1.redirect_troop("wall")
                elif event.key == P1_S_ATTACK:
                    troop = player1.barracks.get_troop("swordsman")
                    if troop:
                        player1.add_troops([troop])
                elif event.key == P1_A:
                    troop = player1.barracks.get_troop("archer")
                    if troop:
                        player1.add_troops([troop])
                elif event.key == P1_UNLEASH:
                    player1.add_troops(player1.barracks.get_all_troops("swordsman") + player1.barracks.get_all_troops("archer"))
                else:
                    player1_input = False

            if not player2_input:
                player2_input = True
                if event.key == P2_W_TRAIN:
                    player2.buy("worker")
                elif event.key == P2_S_TRAIN:
                    player2.buy("swordsman")
                elif event.key == P2_A_TRAIN:
                    player2.buy("archer")
                elif event.key == P2_MINE:
                    if not player2.to_mine():
                        player2.redirect_troop("mine")
                elif event.key == P2_WALL:
                    if not player2.to_wall():
                        player2.redirect_troop("wall")
                elif event.key == P2_S_ATTACK:
                    troop = player2.barracks.get_troop("swordsman")
                    if troop:
                        player2.add_troops([troop])
                elif event.key == P2_A:
                    troop = player2.barracks.get_troop("archer")
                    if troop:
                        player2.add_troops([troop])
                elif event.key == P2_UNLEASH:
                    player2.add_troops(player2.barracks.get_all_troops("swordsman") + player2.barracks.get_all_troops("archer"))
                else:
                    player2_input = False

            if event.key == K_SPACE:
                while 1:
                    clock.tick(10)
                    break_while = False
                    win.blit(pause, (WIDTH / 2 - pause.get_width() / 2, HEIGHT / 2 - pause.get_height() / 2))
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                        elif event.type == KEYDOWN:
                            if event.key == K_SPACE:
                                break_while = True
                    if break_while:
                        break

    display()
   
    if not player1.wall.alive() or not player2.wall.alive():
        game_over = True
        _font = pygame.font.SysFont('cambria', 50)
        win_message = _font.render("Player 1 has won!" if player1.wall.alive() else "Player 2 has won!", True, BLACK)
        win.blit(win_message, (WIDTH / 2 - win_message.get_width() / 2, HEIGHT / 2 - win_message.get_height() / 2))
        pygame.display.update()
        pygame.time.wait(3000)
        with open("game.txt", "w"):
            pass
        pygame.quit()
        sys.exit()

if not game_over:
    with open("game.txt", "w") as f:
        f.write(f"START game\nturn {turn}\nEND game\n")
    player1.save("game.txt")
    player2.save("game.txt")