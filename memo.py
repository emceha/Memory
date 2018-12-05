#! /usr/bin/env python3

import sys
import random
import pygame
import time


class Monster():
    def __init__(self, face, found):
        self.face = face
        self.found = found


pygame.init()
clock = pygame.time.Clock()

blank = pygame.image.load("./img/blank_a.png")
bgimg = pygame.image.load("./img/background.jpg")
screen = pygame.display.set_mode((600, 600))

DOT = "\N{MIDDLE DOT}"

monsters = []
for n in range(18):
    face = pygame.image.load(f"./img/{n}.png")
    monsters.append(Monster(face, False))
    monsters.append(Monster(face, False))

random.shuffle(monsters)
for n, m in enumerate(monsters):
    m.x = (n % 6) * 100 + 2
    m.y = (n // 6) * 100 + 2

clicks = 0
running = True
gameover = False
warmup = True

m2check = set()
gameon = hold = time.time()

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

    if not warmup:
        if not gameover:
            tm = int(time.time() - gameon)
            st = "{:02d}:{:02d}".format(tm // 60, tm % 60)
        pygame.display.set_caption(f"Time {st}  {DOT}  Clicks {clicks:03d}")
    else:
        sek = int(9 - (time.time() - gameon))
        pygame.display.set_caption(f"Start In   {sek} s")
        if sek < 1:
            gameon = time.time()
            warmup = False

    if len(m2check) > 1 and time.time() - hold > 0.6:
        m1, m2 = m2check.pop(), m2check.pop()
        if m1.face == m2.face:
            m1.found = m2.found = True
            if all([m.found for m in monsters]):
                gameover = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not gameover and not warmup:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    m = monsters[(y // 100) * 6 + x // 100]
                    if not m.found and m not in m2check:
                        if len(m2check) < 2:
                            m2check.add(m)
                            hold = time.time()
                            clicks += 1
