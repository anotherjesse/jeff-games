import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode([640, 480])

class Shot(pygame.sprite.Sprite):
    def __init__(self, who, x, y):
        self.x = x
        self.y = y
        self.who = who
        self.age = 30

    def render(self, screen):
        pygame.draw.rect(screen,
                         [255, 0, 0],
                         [8 + self.x*64, 8 + self.y*48,
                          48, 32])
        self.age -= 1

    def alive(self):
        return self.age > 0

class Board():
    def __init__(self):
        self.bkg = pygame.image.load("body.png")
        self.head = pygame.image.load("head.png")
        font = pygame.font.SysFont(pygame.font.get_default_font(), 36)
        self.digits = [font.render(str(digit), True, [255,255,255]) for digit in xrange(10)]

        self.boxes = []

    def draw(self, screen):
        screen.fill([0, 0, 0]) # blank the screen.
        screen.blit(self.bkg, [0,0])

        for digit in xrange(10):
            screen.blit(self.digits[digit], [12,12+48*digit])
            pygame.draw.line(screen,
                             [255,255,0],
                             [0,48*digit],
                             [640,48*digit])

            screen.blit(self.digits[digit], [12+64*digit, 12])
            pygame.draw.line(screen,
                             [255,255,0],
                             [64*digit, 0],
                             [64*digit, 480])

        for b in self.boxes:
            b.render(screen)

        self.boxes = [b for b in self.boxes if b.alive()]

    def shoot(self, who, x, y):
        self.boxes.append(Shot(who,x,y))

    def run(self):
        self.shoot('1324',3,3)
        while pygame.event.poll().type != KEYDOWN:
            self.draw(screen)
            pygame.display.update()

board = Board()
board.run()
