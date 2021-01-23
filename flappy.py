import pygame
import random
import numpy as np
from pygame.locals import K_SPACE, QUIT, K_ESCAPE, KEYDOWN, KEYUP

score = 0
score_timer = 0


# making the game part first
class blc(pygame.sprite.Sprite):
    def __init__(self, length, pos):
        super(blc, self).__init__()
        self.surf = pygame.Surface((10, length))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=pos)

    def update(self):
        self.rect.move_ip(-3   , 0)
        if self.rect.left < 100:
            self.kill()


WHITE = (0, 0, 0)


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
        self.surf = pygame.Surface(
            (10, 10),
        )
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=(100, 450))

    def jump(self):
        self.rect.move_ip(0, -2)
        if self.rect.top < 0:
            self.rect.top = 0

    def fall(self):
        self.rect.move_ip(0, 4)
        if self.rect.bottom == SCREEN_HEIGHT:
            show_go_screen()
            pygame.quit()


font_name = pygame.font.match_font("arial")

INPUT_LAYER = []
difficulty = 2
blocker_pos = []
# starting pygame module
pygame.init()
NUMBER_OF_OBS = 1
# initializing the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    surf.blit(text_surface, text_rect)


def show_go_screen():
    draw_text(screen, " You Lost", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    pygame.display.flip()


# Create a custom event for adding a new enemy
ADDBLOCKER = pygame.USEREVENT + 1
timer = int(800 // difficulty)
pygame.time.set_timer(ADDBLOCKER, timer)
blockers = pygame.sprite.Group()
counter_1 = 0
player = player()
running = True
jump = 0
update_timer = 0
while running:
    score_timer += 1
    if pygame.sprite.spritecollideany(player, blockers):
        running = False
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
    if score_timer % timer == 0:
        score = score + 1
        score_timer = 0
    # if len(blocker_pos) > NUMBER_OF_OBS and counter_1 % 800 == 0:
    #     counter_1 = 0
    #     INPUT_LAYER = []
    #     for x in range(0, NUMBER_OF_OBS):
    #         INPUT_LAYER.append(blocker_pos[2 * x].rect.left - player.rect.right)
    #         INPUT_LAYER.append(blocker_pos[2 * x].rect.bottom - player.rect.top)
    #         INPUT_LAYER.append(blocker_pos[2 * x + 1].rect.left - player.rect.right)
    #         INPUT_LAYER.append(blocker_pos[2 * x + 1].rect.bottom - player.rect.top)
    # counter_1 += 1
    draw_text(screen, str(score), 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    pygame.display.flip()
show_go_screen()
print("Game Over")
pygame.quit()
