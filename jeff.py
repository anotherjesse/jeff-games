#!/usr/bin/env python

from twisted.web import server, resource
from twisted.internet import reactor
import pygame
from pygame.locals import *
from random import uniform

pygame.init()
screen = pygame.display.set_mode([640, 480])

class Shot(pygame.sprite.Sprite):
    def __init__(self, who, x, y):
        self.x = x
        self.y = y
        self.who = who
        self.age = 30
        super(Shot, self).__init__()

    def render(self, screen):
        pygame.draw.rect(screen,
                         [0, 255, 0],
                         [8 + self.y*64, 8 + self.x*48,
                          48, 32])
        self.age -= 1

    def alive(self):
        return self.age > 0

class Missile(pygame.sprite.Sprite):

    WIDTH = 8

    def __init__(self, color=(255,0,0), speed=(1,1), first=(320, 0)):
        self.color = color
        self.speed = speed
        self.first = first
        self.age   = 0
        super(Missile, self).__init__()
        self.rect = (first[0], first[1], self.WIDTH, self.WIDTH)
        self.newpos = first

    def update(self):
        self.age += 1
        self.newpos = list(self.first)
        self.newpos[0] += self.age * self.speed[0]
        self.newpos[1] += self.age * self.speed[1]

        self.rect = (self.newpos[0], self.newpos[1], self.WIDTH, self.WIDTH)

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.first, self.newpos, self.WIDTH)
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(*self.rect))

class Static(pygame.sprite.Sprite):
    def __init__(self, *rect):
        self.rect = pygame.Rect(*rect)
        super(Static, self).__init__()

class Board():
    def __init__(self):
        self.bkg = pygame.image.load("body.png")
        self.head = pygame.image.load("head.png")
        font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
        self.digits = [font.render(str(digit), True, [255,255,255]) for digit in xrange(10)]
        self.missiles = pygame.sprite.Group()

        self.static = pygame.sprite.Group()
        self.static.add(Static(-5,  -5,   0, 490))
        self.static.add(Static(-5,  -5, 650,   0))
        self.static.add(Static(-5, 490, 650,   5))
        self.static.add(Static(640, -5, 650, 490))

        self.boxes = []

        self.frame = 0;

    def draw(self, screen):
        self.frame += 1

        screen.fill([0, 0, 0]) # blank the screen.
        screen.blit(self.bkg, [0,0])

        for digit in xrange(10):
            pygame.draw.line(screen,
                             [255,255,0],
                             [0,48*digit],
                             [640,48*digit])

            pygame.draw.line(screen,
                             [255,255,0],
                             [64*digit, 0],
                             [64*digit, 480])
        for row in xrange(10):
            for col in xrange(10):
                screen.blit(self.digits[col],
                            [2+64*row, 2+48*col])
                screen.blit(self.digits[row],
                            [12+64*row, 2+48*col])


        for b in self.boxes:
            b.render(screen)

        self.boxes = [b for b in self.boxes if b.alive()]

        self.missiles.update()

        if self.frame % 50 == 0:
            side = int(uniform(0, 4))
            if (side == 0):
                start = (uniform(0, 640), 0)
            elif (side == 2):
                start = (uniform(0, 640), 479)
            elif (side == 1):
                start = (0, uniform(0, 480))
            elif (side == 3):
                start = (639, uniform(0, 480))

            self.missiles.add(Missile(first=start))

        for s in self.static:
            pygame.sprite.spritecollide(s, self.missiles, True)

        for b in self.boxes:
            pygame.spride.spritecollide(b, self.missiles, True)

        [m.draw(screen) for m in self.missiles]

    def shoot(self, who, x, y):
        print 'shot!'
        self.boxes.append(Shot(who,x,y))

    def run(self):
        while True:
            key = pygame.event.poll()
            if key.type == KEYDOWN and key.key == K_q:
                break
            self.draw(screen)
            pygame.display.update()
            reactor.runUntilCurrent()
            reactor.doIteration(0)

class CommandCollector(resource.Resource):
    isLeaf = True

    def __init__(self, board):
        self.board = board
    def render(self, req):
        print req
        try :
            uid = req.args.get("uid")[0]
            x = int(req.args.get("x")[0])
            y = int(req.args.get("y")[0])
            self.board.shoot(uid, x, y)
        except:
            pass

        return "orders received, sir"

if __name__ == '__main__':
    board = Board()
    collector = CommandCollector(board)
    reactor.listenTCP(8080, server.Site(collector))
    board.run()
