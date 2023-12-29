import math

import pygame

WIDTH, HEIGHT = 1000, 800
FPS = 120


class MovingObjects:
    def __init__(self, x, y, size):
        self.image = pygame.Surface((size, size))
        self.image.fill("white")
        self.size = size
        self.x, self.y = x, y
        self.vx, self.vy = 0., 0.

    def draw(self, sc):
        sc.blit(self.image, (self.x, self.y))

    def update(self, dt_):
        self.x += self.vx * dt_
        self.y += self.vy * dt_


class Player(MovingObjects):

    def __init__(self, acceleration, max_speed, size):
        super().__init__(WIDTH // 2 - size // 2, HEIGHT // 2 - size // 2, size)
        self.direction = [0, 0]
        self.acceleration = acceleration
        self.max_speed = max_speed

    def update(self, dt_):
        self.vx = self.vx + self.acceleration * self.direction[0] * dt_
        self.vy = self.vy + self.acceleration * self.direction[1] * dt_

        if self.vx > 0:
            self.vx = min(self.vx, self.max_speed)
        else:
            self.vx = max(self.vx, -self.max_speed)
        if self.vy > 0:
            self.vy = min(self.vy, self.max_speed)
        else:
            self.vy = max(self.vy, -self.max_speed)

        if self.direction[0] == 0:
            self.vx -= self.acceleration * dt_ * math.copysign(1, self.vx)
            if abs(self.vx) < 40:
                self.vx = 0

        if self.direction[1] == 0:
            self.vy -= self.acceleration * dt_ * math.copysign(1, self.vy)
            if abs(self.vy) < 40:
                self.vy = 0
        super().update(dt_)

    def set_direction(self, side, value):
        self.direction[side] = value


class Enemy(MovingObjects):
    def __init__(self, x, y, size, speed):
        super().__init__(x, y, size)
        self.angle = 0.
        self.speed = speed
        self.image.fill("red")

    def calc_angle(self, pl_x, pl_y):
        self.angle = math.atan2(pl_y - (self.y + self.size // 2), pl_x - (self.x + self.size // 2))

    def update(self, dt_):
        self.vx = self.speed * math.cos(self.angle)
        self.vy = self.speed * math.sin(self.angle)
        super().update(dt_)


class Enemies:

    def __init__(self):
        self.enemies = []

    def add(self, enemy_):
        self.enemies.append(enemy_)

    def del_(self, enemy_):
        if enemy_ in self.enemies:
            self.enemies.remove(enemy_)


def dt():
    return 0.001 * clock.get_time()


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = Player(1500, 500, 50)
enemy = Enemy(100, 100, 20, 300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    player.set_direction(0, 0)
    player.set_direction(1, 0)

    key_pres = pygame.key.get_pressed()
    if key_pres[pygame.K_w]:
        player.set_direction(1, -1)
    if key_pres[pygame.K_s]:
        player.set_direction(1, 1)
    if key_pres[pygame.K_a]:
        player.set_direction(0, -1)
    if key_pres[pygame.K_d]:
        player.set_direction(0, 1)

    player.update(dt())
    enemy.calc_angle(player.x + player.size // 2, player.y + player.size // 2)
    enemy.update(dt())
    screen.fill(0)
    player.draw(screen)
    enemy.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
