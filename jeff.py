from twisted.web import server, resource
from twisted.internet import reactor
import pygame
import random
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode([640, 480], pygame.FULLSCREEN|pygame.HWSURFACE)

class Shot(pygame.sprite.Sprite):
    def __init__(self, who, x, y):
        self.x = x
        self.y = y
        self.who = who
        self.age = 30

    def render(self, screen):
        pygame.draw.rect(screen,
                         [255, 0, 0],
                         [8 + self.y*64, 8 + self.x*48,
                          48, 32])
        self.age -= 1

    def alive(self):
        return self.age > 0

class Board():
    def __init__(self):
        self.bkg = pygame.image.load("body.png")
        self.heads = [pygame.image.load(fn) for fn in
                      ['head1.png', 'head2.png', 'head3.png']]
        self.head = random.choice(self.heads)
        font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
        self.digits = [font.render(str(digit),
                                   True,
                                   [0,0,0],
                                   [255,255,255]) for digit in xrange(10)]

        self.boxes = []

    def draw(self, screen):
        screen.fill([0, 0, 0]) # blank the screen.
        screen.blit(self.bkg, [0,0])

        if random.random() < 0.05:
            self.head = random.choice(self.heads)

        screen.blit(self.head, [0,0])

        for digit in xrange(10):
            pygame.draw.line(screen,
                             [255,255,255],
                             [0,48*digit],
                             [640,48*digit])

            pygame.draw.line(screen,
                             [255,255,255],
                             [64*digit, 0],
                             [64*digit, 480])


        for row in xrange(10):
            for col in xrange(10):
                screen.blit(self.digits[col],
                            [1+64*row, 1+48*col])
                screen.blit(self.digits[row],
                            [10+64*row, 1+48*col])


        for b in self.boxes:
            b.render(screen)

        self.boxes = [b for b in self.boxes if b.alive()]


    def shoot(self, who, x, y):
        print 'shot!'
        self.boxes.append(Shot(who,x,y))

    def run(self):
        while pygame.event.poll().type != KEYDOWN:
            self.draw(screen)
            pygame.display.update()
            reactor.runUntilCurrent()
            reactor.doIteration(0)

class CommandCollector(resource.Resource):
    isLeaf = True

    def __init__(self, board):
        self.board = board
    def render(self, req):
        uid = req.args.get("uid",["????"])[0]
        x = int(req.args.get("x",[0])[0])
        y = int(req.args.get("y",[0])[0])
        self.board.shoot(uid, x, y)
        return "orders received, sir"

if __name__ == '__main__':
    board = Board()
    collector = CommandCollector(board)
    reactor.listenTCP(8080, server.Site(collector))
    board.run()
