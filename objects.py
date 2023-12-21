import pygame, math
from castles_war_constants import *
from settings import *

class Barracks:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

        self.training = {}
        self.troops = []

    def move_out(self):
        for troop in list(self.training):
            self.training[troop] -= 1
            if self.training[troop] <= 0:
                del self.training[troop]
                self.troops.append(troop)

    def add_troop(self, troop):
        troop.x = self.x + self.img.get_width() / 2 - troop.img.get_width() / 2
        troop.y = HEIGHT - troop.img.get_height()
        self.training[troop] = troop.training_time

    def get_troop(self, typ):
        for troop in self.troops[:]:
            if troop.type == typ:
                self.troops.remove(troop)
                return troop
        return None

    def get_all_troops(self, typ):
        u = []
        for troop in self.troops[:]:
            if troop.type == typ:
                self.troops.remove(troop)
                u.append(troop)

        return u

    def display(self, surf):
        surf.blit(self.img, (self.x, self.y))

    def decrease_troop_time(self, pos):
        l = list(self.training)
        k = l[pos]
        self.training[pos] -= 1

class Mine:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.workers = []

    def mine_gold(self, current):
        current += len(self.workers) * W_PROD
        return current

    def add_worker(self, worker):
        self.workers.append(worker)

    def display(self, surf):
        surf.blit(self.img, (self.x, self.y))

class Wall:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

        self.health = WALL_HEALTH
        self._font = _font = pygame.font.SysFont('cambria', 30)
        self.health_dis = self._font.render(str(self.health), True, BLACK)
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

        self.workers = []

    def add_worker(self, worker):
        self.workers.append(worker)

    def repair_wall(self):
        self.health += len(self.workers) * W_REPAIR
        if self.health > WALL_HEALTH:
            self.health = WALL_HEALTH

        self._font = _font = pygame.font.SysFont('cambria',30)
        self.health_dis = self._font.render(str(self.health), True, BLACK)

    def display(self, surf):
        surf.blit(self.img, (self.x, self.y))

        for worker in self.workers:
            worker.display(surf)

        surf.blit(self.health_dis, (self.x + self.img.get_width() / 2 - self.health_dis.get_width() / 2, self.y - self.health_dis.get_height()))

    def alive(self):
        if self.health <= 0:
            return False
        return True

class Tower:
    def __init__(self, x, y, img, player):
        self.x = x
        self.y = y
        self.img = img

        self.arrow = None
        self.player = player
        self.cooldown = 0

    def shoot(self, targets):
        if self.cooldown == 0:
            if targets:
                target = min(targets, key=lambda x: (abs(x.x - self.x)))

                if self.in_range(target):
                    ank = (target.x + target.img.get_width() / 2) - (self.x + (self.img.get_width() if self.x < WIDTH / 2 else 0)) 
                    geg = (target.y + target.img.get_height() / 2) - (self.y + self.img.get_height() / 5)
                    hyp = math.hypot(ank, geg)

                    t = hyp // ARROW_SPEED
                    self.arrow = Arrow(self.x + (self.img.get_width() if self.x < WIDTH / 2 else 0), self.y + self.img.get_height() / 5, 1, ank/t, geg/t)
                    self.cooldown = TOWER_REST

        if not self.arrow:
            return True
        self.move_arrow(targets)
        return False

    def move_arrow(self, targets):
        if self.arrow.move(targets):
            self.arrow = None

    def cooldown_time(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def in_range(self, target):
        if self.player == "player1":
            if abs(target.x - (self.x + self.img.get_width())) <= TOWER_RANGE:
                return True
        else:
            if abs((target.x + target.img.get_width()) - self.x) <= TOWER_RANGE:
                return True
        return False

    def display(self, surf):
        if self.arrow:
            self.arrow.display(surf)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mine = Mine(MINE_POS, self.y - MINE1.get_height(), MINE1)
        self.barracks = Barracks(BARRACKS_POS, self.y - BARRACKS1.get_height(), BARRACKS1)
        self.tower = Tower(WALL_POS + WALL_WIDTH / 2 - CASTLE1.get_width() / 2, self.y - CASTLE1.get_height(), CASTLE1, "player1")
        self.wall = Wall(WALL_POS, self.y - CASTLE1.get_height(), CASTLE1)
        self.attackers = []

        self.gold = INIT_RESOURCES
        self._font = pygame.font.SysFont('cambria', 45)
        self.goldSurf = self._font.render(f"Gold: {self.gold}", True, BLACK)

        self.player = "player1"

    def display(self, surf):
        self.display_buildings(surf)
        self.display_troops(surf)
        self.display_recources(surf)

    def deanimate(self):
        for worker in self.wall.workers:
            worker.animated = False
        for troop in self.attackers:
            troop.animated = False

    def animate(self):
        finished = True
        for worker in self.wall.workers:
            if not worker.animate_once():
                finished = False
        for troop in self.attackers:
            if not troop.animate_once():
                finished = False
        return finished

    def display_recources(self, surf):
        surf.blit(self.goldSurf, (0,0))

    def display_buildings(self, surf):
        self.mine.display(surf)
        self.barracks.display(surf)
        self.tower.display(surf)
        self.wall.display(surf)

    def display_troops(self, surf):
        for troop in self.attackers[:]:
            troop.display(surf)

    def run_buildings(self):
        self.barracks.move_out()
        self.gold = self.mine.mine_gold(self.gold)
        self.goldSurf = self._font.render(f"Gold: {self.gold}", 1, BLACK)
        self.wall.repair_wall()

    def add_troops(self, troops):
        self.attackers += troops
    
    def move_troops(self, targets):
        moved = True
        for troop in self.attackers[:]:
            troop.current_state = 0
            if not troop.move(targets):
                moved = False
            elif troop.type == "worker":
                if troop.targetType == "mine":
                    self.mine.add_worker(troop)
                    self.attackers.remove(troop)
                elif troop.targetType == "wall":
                    self.wall.add_worker(troop)
                    self.attackers.remove(troop)
        return moved

    def remove_dead(self):
        for troop in self.attackers[:]:
            troop.dist_moved = 0
            if troop.type != "worker":
                if troop.death():
                    self.attackers.remove(troop)

    def troop_attack(self, targets):
        finished = True
        for troop in self.attackers[:]:
            if troop.type != "worker":
                if not troop.move_attack(targets):
                    finished = False

        if not self.tower.shoot(targets):
            finished = False

        return finished

    def redirect_troop(self, dest):
        if dest == "mine":
            if self.wall.workers:
                worker = self.wall.workers.pop(0)
                worker.reached = False
                worker.dir *= -1
                worker.flip = not worker.flip
                worker.targetType = "mine"
                worker.target = self.mine
                self.attackers.append(worker)
        elif dest == "wall":
            if self.mine.workers:
                worker = self.mine.workers.pop(0)
                worker.reached = False
                worker.dir *= -1
                worker.targetType = "wall"
                worker.target = self.wall
                worker.flip = not worker.flip
                self.attackers.append(worker)

    def buy(self, troopType):
        if troopType == "worker":
            if self.gold >= W_COST:
                self.barracks.add_troop(Worker(0, 0, self.player, None, None))
                self.gold -= W_COST
        elif troopType == "swordsman":
            if self.gold >= S_COST:
                self.barracks.add_troop(Swordsman(0, 0, self.player))
                self.gold -= S_COST
        else:
            if self.gold >= A_COST:
                self.barracks.add_troop(Archer(0, 0, self.player))
                self.gold -= A_COST

        self.goldSurf = self._font.render(f"Gold: {self.gold}", True, BLACK)

    def decrease_cooldown(self):
        for troop in self.attackers:
            if troop.type != "worker":
                troop.cooldown_time()
        self.tower.cooldown_time()

    def to_mine(self):
        troop = self.barracks.get_troop("worker")
        if troop:
            troop.target = self.mine
            troop.targetType = "mine"
            troop.lock()
            self.add_troops([troop])
            return True
        return False

    def to_wall(self):
        troop = self.barracks.get_troop("worker")
        if troop:
            troop.target = self.wall
            troop.targetType = "wall"
            troop.lock()
            self.add_troops([troop])
            return True
        return False

    def load(self, file):
        start = False
        add = True
        with open(file, "r") as f:
            for line in f:
                add = False
                if start:
                    if line.strip().lower() == f"end {self.player}":
                        start = False
                        break
                    f = line.strip().split(" ")[0].lower()
                    fs = line.strip().split(" ")[1].lower()
                    if f == "resources":
                        self.gold = int(fs)
                        self.goldSurf = self._font.render(f"Gold: {self.gold}", True, BLACK)
                    elif f == "wall":
                        self.wall.health = self.health = int(fs)
                    elif f == "worker":
                        self.barracks.add_troop(Worker(0, 0, self.player, None, None))
                        last = list(self.barracks.training)[-1]
                        while self.barracks.training[list(self.barracks.training)[-1]] == last:
                            self.barracks.decrease_troop_time(-1)
                            if not self.barracks.training:
                                break
                        
                        if fs == "mine":
                            self.barracks.troops.insert(0, list(self.barracks.training)[-1])
                            self.barracks.training.pop(list(self.barracks.training)[-1])
                            self.barracks.troops[0].target = self.mine
                            self.barracks.troops[0].targetType = "mine"
                            self.add_troops([self.barracks.troops[0]])
                            self.barracks.troops.pop(0)
                            self.attackers[-1].lock()
                            while not self.attackers[-1].reached:
                                self.attackers[-1].move([])
                                self.attackers[-1].dist_moved = 0
                            self.mine.add_worker(self.attackers[-1])
                            self.attackers.pop()
                        elif fs == "wall":
                            self.barracks.troops.insert(0, list(self.barracks.training)[-1])
                            self.barracks.training.pop(list(self.barracks.training)[-1])
                            self.barracks.troops[0].target = self.wall
                            self.barracks.troops[0].targetType = "wall"
                            self.add_troops([self.barracks.troops[0]])
                            self.barracks.troops.pop(0)
                            self.attackers[-1].lock()
                            while not self.attackers[-1].reached:
                                self.attackers[-1].move([])
                                self.attackers[-1].dist_moved = 0
                            self.wall.add_worker(self.attackers[-1])
                            self.attackers.pop()
                    elif f == "swordsman":
                        if fs == "barracks" or fs == "training":
                            self.barracks.add_troop(Swordsman(0,0,self.player))
                            last = list(self.barracks.training)[-1]
                            if fs == "barracks":
                               while self.barracks.training[list(self.barracks.training)[-1]] == last:
                                    self.barracks.decrease_troop_time(-1)
                                    if not self.barracks.training:
                                        break
                        else:
                            x, y, health = fs.split(",")
                            sword = Swordsman(int(x), int(y), self.player)
                            sword.health = int(health)
                            self.attackers.append(sword)
                    elif f == "archer":
                        if fs == "barracks" or fs == "training":
                            self.barracks.add_troop(Archer(0,0,self.player))
                            last = list(self.barracks.training)[-1]
                            if fs == "barracks":
                               while self.barracks.training[list(self.barracks.training)[-1]] == last:
                                    self.barracks.decrease_troop_time(-1)
                                    if not self.barracks.training:
                                        break
                        else:
                            x, y, health = fs.split(",")
                            archer = Archer(int(x), int(y), self.player)
                            archer.health = int(health)
                            self.attackers.append(archer)
                else:
                    if line.strip().lower() == f"start {self.player}":
                        start = True

        if add:
            self.add_beginning_troops()

    def add_beginning_troops(self):
        self.barracks.add_troop(Worker(0, 0, self.player, None, None))
        self.barracks.add_troop(Swordsman(0, 0, self.player))
        self.barracks.add_troop(Archer(0, 0, self.player))

        while self.barracks.training:
            self.barracks.move_out()

    def save(self, file):
        with open(file, "a") as f:
            f.write(f"START {self.player}\n")
            f.write(f"resources {self.gold}\n")
            f.write(f"wall {self.wall.health}\n")
            for troop in self.barracks.training:
                f.write(f"{troop.type} training\n")
            for troop in list(self.barracks.training) + self.barracks.troops:
                f.write(f"{troop.type} barracks\n")
            for worker in self.mine.workers + self.wall.workers:
                f.write(f"worker {worker.targetType}\n")
            for troop in self.attackers:
                f.write(f"{troop.type} {int(troop.x)},{int(troop.y)},{int(troop.health)}\n")
            f.write(f"END {self.player}\n")
            
        
class Player2(Player):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.wall = Wall(WIDTH - 140 - WALL_POS, self.y - CASTLE2.get_height(), CASTLE2)
        self.tower = Tower(WIDTH - 140 - WALL_POS, self.y - CASTLE2.get_height(), CASTLE2, "player2")
        self.barracks = Barracks(WIDTH - 140 - BARRACKS_POS, self.y - BARRACKS2.get_height(), BARRACKS2)
        self.mine = Mine(WIDTH -110 - MINE_POS, self.y - MINE2.get_height(), MINE2)

        self.player = "player2"

    def display_recources(self, surf):
        surf.blit(self.goldSurf, (WIDTH - self.goldSurf.get_width(), 0))

class Arrow:
    def __init__(self, x, y, direction, velx=ARROW_SPEED, vely=0):
        self.x = x
        self.y = y
        self.dir = direction
        self.damage = ARROW_HIT

        self.velx = velx * self.dir
        self.vely = vely

        self.flip = True if self.dir == -1 else False
        self.img = ARROW

        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x, self.y)

    def move(self, targets):
        self.x += self.velx
        self.y += self.vely

        for target in targets:
            if pygame.Rect(self.x, self.y, self.rect.width, self.rect.height).colliderect(target.rect):
                target.health -= self.damage
                return True
        if self.off_screen():
            return True
        return False

    def display(self, surf):
        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.x, self.y))

    def off_screen(self):
        if self.x < 0 or self.x > WIDTH or self.y > HEIGHT:
            return True
        return False

# helper class (base-troop)
class Unit:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.time = 0
        self.appeared = False
        self.flip = False
        self.health = 100
        self.dist_moved = 0
        self.dir = 1
        self.animated = False

        self.current_state = 0
        self.current = 0

    def display(self, surf):
        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.x, self.y))
    
    def animate(self):
        self.time += 1
        if self.time % 10 == 0:
            self.current += 1

        self.img = self.imgs[self.current_state][self.current]

        if self.time >= 39:
            self.current = 0
            self.time = 0
        return False

    def animate_once(self):
        if not self.animated:
            self.current_state = 1
            self.time += 1
            if self.time % 10 == 0:
                self.current += 1

            self.img = self.imgs[self.current_state][self.current]

            if self.time >= 39:
                self.current = 0
                self.time = 0
                self.animated = True
                return True
            return False
        return True

    def display_health(self, surf):
        self.health_dis = small.render(str(self.health), 1, BLACK)
        surf.blit(self.health_dis, (self.x + self.img.get_width() / 2 - self.health_dis.get_width() / 2, self.y - self.health_dis.get_height() - 10))

class Worker(Unit):
    def __init__(self, x, y, player, target, targetType):
        super().__init__(x, y, player)
        self.target = target
        self.targetType = targetType
        self.type = "worker"

        self.imgs = []
        for state in ["run", "repair"]:
            imgs = []
            for i in range(4):
                imgs.append(pygame.image.load(f"images/{self.player}/worker-{state}-{i}.png"))
            self.imgs.append(imgs)
        
        self.img = self.imgs[0][0]

        self.training_time = W_TRAIN
        self.vel = W_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

        self.reached = False

    def lock(self):
        if self.target.x < self.x:
            self.dir = -1
            if self.player == "player1":
                self.flip = True
        elif self.player == "player2":
            self.flip = True

    def move(self, targets):
        if not self.reached:
            self.x += self.dir
            self.dist_moved += self.dir
            self.animate()
            if self.target.rect.colliderect(pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)):
                self.reached = True
                return True
            return False
        return True

class Swordsman(Unit):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.dir = 1 if player == "player1" else -1
        self.type = "swordsman"

        self.imgs = []
        for state in ["run", "attack"]:
            imgs = []
            for i in range(4):
                imgs.append(pygame.image.load(f"images/{self.player}/sword-{state}-{i}.png"))
            self.imgs.append(imgs)
        
        self.img = self.imgs[0][0]

        self.training_time = S_TRAIN
        self.vel = S_SPEED
        self.range = S_RANGE
        self.damage = S_HIT
        self.cooldown = 0
        self.health = S_HEALTH

        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

        self.reached = False
        self.attacking = False
        self.reached_target = None

    def move(self, targets):
        for target in targets:
            if self.in_range(target):
                self.reached_target = target
                break
            else:
                self.reached_target = None

        if self.reached_target is None and abs(self.dist_moved) < abs(self.vel):
            self.x += self.dir
            self.rect.x = self.x
            self.rect.y = self.y
            self.animate()
            self.dist_moved += self.dir
        else:
            return True
        return False

    def move_attack(self, targets):
        if self.reached_target:
            if self.cooldown <= 0:
                self.reached_target.health -= self.damage
                self.cooldown = S_REST
                return True
        return True
            
    def in_range(self, target):
        if self.player == "player1":
            if abs(self.x + self.img.get_width() - target.x) <= self.range:
                return True
        else:
            if abs(target.x + target.img.get_width() - self.x) <= self.range:
                return True
        return False

    def cooldown_time(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def death(self):
        if self.health <= 0:
            return True
        return False

    def display(self, surf):
        super().display(surf)
        self.display_health(surf)


class Archer(Unit):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.dir = 1 if player == "player1" else -1
        self.type = "archer"

        self.imgs = []
        for state in ["run", "shoot"]:
            imgs = []
            for i in range(4):
                imgs.append(pygame.image.load(f"images/{self.player}/bow-{state}-{i}.png"))
            self.imgs.append(imgs)
        
        self.img = self.imgs[0][0]

        self.training_time = A_TRAIN
        self.vel = A_SPEED
        self.range = A_RANGE
        self.damage = A_HIT
        self.cooldown = 0
        self.health = A_HEALTH

        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

        self.reached = False
        self.alive = True

        self.arrow = None

    def move(self, targets):
        for target in targets:
            if self.in_range(target):
                self.reached_target = target
                break
            else:
                self.reached_target = None

        if self.reached_target is None and abs(self.dist_moved) < abs(self.vel):
            self.x += self.dir
            self.dist_moved += self.dir
            self.rect.x = self.x
            self.rect.y = self.y
            self.animate()
        else:
            self.dist_moved = 0
            return True
        return False
    
    def move_attack(self, targets):
        if not self.arrow:
            if self.cooldown == 0:
                if self.reached_target:
                    self.shoot()
                    self.cooldown = A_REST
        else:
            if self.arrow.move([self.reached_target] + targets):
                self.arrow = None
        if self.arrow is None:
            return True
        return False

    def in_range(self, target):
        if self.player == "player1":
            if abs(self.x + self.img.get_width() - target.x) <= self.range:
                return True
        else:
            if abs(target.x + target.img.get_width() - self.x) <= self.range:
                return True
        return False

    def shoot(self):
        self.arrow = Arrow(self.x + (self.img.get_width() if self.player == "player1" else 0), self.y + 10 * 1, self.dir)

    def cooldown_time(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def display(self, surf):
        super().display(surf)
        self.display_health(surf)

        if self.arrow:
            self.arrow.display(surf)

    def death(self):
        if self.health <= 0:
            return True
        return False