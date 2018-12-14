#! /usr/bin/env python3

import time
import random
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN


class Monster():
    def __init__(self, face):
        self.face = face
        self.found = False


class Game():
    def __init__(self, screen):
        self.blank = pygame.image.load("img/blank.png")
        self.bgimg = pygame.image.load("img/background.jpg")
        self.screen = screen
        self.monsters = []
        self.m2check = set()
        self.running = True
        self.over = False
        self.warmup = True
        self.hold = time.time()
        self.populate()

    def draw_background(self):
        self.screen.blit(self.bgimg, (0, 0))

    def update_monsters(self):
        for m in self.monsters:
            if self.over or m in self.m2check:
                rx = random.randint(-1, 1)
                ry = random.randint(-1, 1)
                self.screen.blit(m.face, (m.x + rx, m.y + ry))
            elif self.warmup or m.found:
                self.screen.blit(m.face, (m.x, m.y))
            else:
                self.screen.blit(self.blank, (m.x, m.y))

    def populate(self):
        for n in range(6 * 6 // 2):
            face = pygame.image.load(f"img/{n}.png")
            self.monsters.append(Monster(face))
            self.monsters.append(Monster(face))

        random.shuffle(self.monsters)
        for n, m in enumerate(self.monsters):
            m.x = (n % 6) * 98 + 6
            m.y = (n // 6) * 98 + 6
            m.r = pygame.Rect(m.x + 18, m.y + 18, 60, 60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.warmup and len(self.m2check) < 2:
                        x, y = pygame.mouse.get_pos()
                        for m in self.monsters:
                            if not m.found or m not in self.m2check:
                                if m.r.collidepoint(x, y):
                                    self.m2check.add(m)
                                    self.hold = time.time()

    def handle_state(self):
        if self.warmup:
            if time.time() - self.hold > 9:
                self.warmup = False
        if len(self.m2check) > 1 and time.time() - self.hold > 0.7:
            m1, m2 = self.m2check.pop(), self.m2check.pop()
            if m1.face == m2.face:
                m1.found = m2.found = True
                if all([m.found for m in self.monsters]):
                    self.over = True


pygame.init()
clock = pygame.time.Clock()
game = Game(pygame.display.set_mode((600, 600)))

while game.running:
    clock.tick(50)
    pygame.display.flip()
    game.draw_background()
    game.update_monsters()
    game.handle_events()
    game.handle_state()
