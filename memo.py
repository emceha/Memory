#! /usr/bin/env python3

import sys
import random
import pygame
import time
from pygame.locals import *


class Monster():
    def __init__(self, face):
        self.face = face
        self.found = False


pygame.init()

blank = pygame.image.load("./img/blank.png")
bgimg = pygame.image.load("./img/background.jpg")
screen = pygame.display.set_mode((600, 600))

monsters = []
for n in range(18):
    face = pygame.image.load(f"./img/{n}.png")
    monsters.append(Monster(face))
    monsters.append(Monster(face))

random.shuffle(monsters)
for n, m in enumerate(monsters):
    m.x = (n % 6) * 100 + 2
    m.y = (n // 6) * 100 + 2
    m.r = pygame.Rect(m.x + 15, m.y + 15, 70, 70)

running = True
gameover = False
warmup = True

m2check = set()
hold = time.time()
clock = pygame.time.Clock()

while running:
    clock.tick(50)
    pygame.display.flip()
    screen.blit(bgimg, (0, 0))

    for m in monsters:
        if m in m2check or gameover:
            rx = random.randint(-1, 1)
            ry = random.randint(-1, 1)
            screen.blit(m.face, (m.x + rx, m.y + ry))
        elif m.found or warmup:
            screen.blit(m.face, (m.x, m.y))
        else:
            screen.blit(blank, (m.x, m.y))

    if warmup:
        if time.time() - hold > 9:
            warmup = False

    if len(m2check) > 1 and time.time() - hold > 0.6:
        m1, m2 = m2check.pop(), m2check.pop()
        if m1.face == m2.face:
            m1.found = m2.found = True
            if all([m.found for m in monsters]):
                gameover = True

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if not warmup and len(m2check) < 2:
                    x, y = pygame.mouse.get_pos()
                    m = monsters[(y // 100) * 6 + x // 100]
                    if m.found or m in m2check:
                        break
                    if m.r.collidepoint(x, y):
                        m2check.add(m)
                        hold = time.time()
