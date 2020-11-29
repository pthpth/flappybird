import pygame
import random
from pygame.locals import (
    K_SPACE,
    QUIT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP
)


# making the game part first
class blc(pygame.sprite.Sprite):
    def __init__(self, length, pos):
        super(blc, self).__init__()
        self.surf = pygame.Surface((10, length))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=pos)

    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.left < 0:
            self.kill()


class blocker(object):
    def __init__(self):
        self.hgt = random.randint(200, 700)
        self.top = random.randint(200, self.hgt)
        self.bottom = self.hgt - self.top
        self.top_layer = blc(self.top, (SCREEN_WIDTH, SCREEN_HEIGHT - self.top // 2))
        self.bottom_layer = blc(self.bottom, (SCREEN_WIDTH, self.bottom // 2))


# player class
class player(pygame.sprite.Sprite):
    def __init__(self):
        super(player, self).__init__()
        self.surf = pygame.Surface((10, 10), )
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=(100, 450))

    def jump(self):
        self.rect.move_ip(0, -2)

    def fall(self):
        self.rect.move_ip(0, 3)


# starting pygame module
pygame.init()
# initializing the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDBLOCKER = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBLOCKER, 800)
blockers = pygame.sprite.Group()

player = player()
running = True
jump = 0
update_timer = 0
while running:
    if pygame.sprite.spritecollideany(player,blockers):
        running=False
    for event in pygame.event.get():
        if event.type == ADDBLOCKER:
            tem = blocker()
            blockers.add(tem.top_layer)
            blockers.add(tem.bottom_layer)
            tem = None
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                jump = 10
        if event.type == KEYUP:
            if event.key == K_SPACE:
                jump = -10
    # mechanism to show simulate gravity and jumping
    if jump > 0:
        if jump % 5 == 0:
            player.jump()
        jump = jump + 1
    if jump < 0:
        if abs(jump) % 10 == 0:
            player.fall()
        jump = jump - 1

    screen.fill((255, 255, 255))
    screen.blit(player.surf, player.rect)
    update_timer += 1
    for x in blockers:
        screen.blit(x.surf, x.rect)
    if update_timer % 5 == 0:
        blockers.update()
        update_timer = 0
    pygame.display.flip()
