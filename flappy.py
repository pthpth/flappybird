import random
import time

import numpy as np
import pygame
from pygame.locals import QUIT, K_ESCAPE, KEYDOWN


# val = open("values.txt", "a")
score=0

def sigmoid(z):
    return 1 / (1 + np.exp(z * -1))


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
        self.rect.move_ip(0, -3)
        if self.rect.top < 0:
            self.rect.top = 0

    def fall(self):
        self.rect.move_ip(0, 1)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class PLAYER:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias
        self.emote = player()
        self.aliveTime = time.time()

    def give_answer(self, data):
        sig = sigmoid(np.dot(data, self.weights.T) + self.bias)
        if sig > 0.5:
            self.emote.jump()


# making the game part first
class blc(pygame.sprite.Sprite):
    def __init__(self, length, pos):
        super(blc, self).__init__()
        self.surf = pygame.Surface((10, length))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=pos)

    def update(self):
        self.rect.move_ip(-2, 0)
        if self.rect.left < 100:
            update_data(self)
            self.kill()


INPUT_LAYER = []
WHITE = (0, 0, 0)
font_name = pygame.font.match_font("arial")
blocker_pos = []
pygame.init()
NUMBER_OF_OBS = 1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def update_data(data: blc):
    blocker_pos.remove(data)


class blocker(object):
    def __init__(self):
        self.hgt = random.randint(300, 600)
        self.top = random.randint(300, self.hgt)
        self.bottom = self.hgt - self.top
        self.top_layer = blc(self.top, (SCREEN_WIDTH, SCREEN_HEIGHT - self.top // 2))
        self.bottom_layer = blc(self.bottom, (SCREEN_WIDTH, self.bottom // 2))


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
pygame.time.set_timer(ADDBLOCKER, 400)
blockers = pygame.sprite.Group()
counter_1 = 0
subject = []
# for x in range(32):
# subject.append(PLAYER(np.random.randn(1, NUMBER_OF_OBS * 4), np.random.randn()))
subject.append(PLAYER(np.array([[-1.11259854, -0.17451191, -0.68249956, -1.28828769]]), 0.06528976057173011))
running = True
jump = 0
update_timer = 0
while running:
    #     if pygame.sprite.spritecollideany(player, blockers):
    #         running = False
    if len(subject) == 0:
        running = False
    for event in pygame.event.get():
        if event.type == ADDBLOCKER:
            tem = blocker()
            blocker_pos.append(tem.top_layer)
            blocker_pos.append(tem.bottom_layer)
            blockers.add(tem.top_layer)
            blockers.add(tem.bottom_layer)
            tem = None
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    screen.fill((255, 255, 255))
    update_timer += 1
    for x in blockers:
        screen.blit(x.surf, x.rect)
    if update_timer % 5 == 0:
        blockers.update()
        update_timer = 0
    for z in subject:
        z.emote.fall()
        if pygame.sprite.spritecollideany(z.emote, blockers):
            subject.remove(z)
    if len(blocker_pos) > NUMBER_OF_OBS * 2:
        for z in subject:
            screen.blit(z.emote.surf, z.emote.rect)
            INPUT_LAYER = []
            for x in range(0, NUMBER_OF_OBS):
                INPUT_LAYER.append(blocker_pos[2 * x].rect.left - z.emote.rect.right)
                INPUT_LAYER.append(blocker_pos[2 * x].rect.bottom - z.emote.rect.top)
                INPUT_LAYER.append(blocker_pos[2 * x + 1].rect.left - z.emote.rect.right)
                INPUT_LAYER.append(blocker_pos[2 * x + 1].rect.bottom - z.emote.rect.top)
            INPUT_LAYER = np.array(INPUT_LAYER)
            INPUT_LAYER = np.divide(INPUT_LAYER, 400)
            z.give_answer(INPUT_LAYER)
    if len(subject) == 1:
        best = str(subject[0].weights) + " " + str(subject[0].bias) + " " + str(
            time.time() - subject[0].aliveTime) + "\n"
    # draw_text(screen, str(INPUT_LAYER), 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    pygame.display.flip()
show_go_screen()
print("Game Over")
# val.write(best)
pygame.quit()
