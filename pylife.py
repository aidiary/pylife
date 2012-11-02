#!/usr/bin/env python
#coding:utf-8
import pygame
from pygame.locals import *
import random
import sys

SCR_RECT = Rect(0, 0, 800, 600)  # screen size
CS = 10                          # cell size
NUM_ROW = SCR_RECT.height / CS   # the num of rows
NUM_COL = SCR_RECT.width / CS    # the num of cols
DEAD, ALIVE = 0, 1               # cell's state
RAND_LIFE = 0.1

class LifeGame:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption(u"Conway's Game of Life")

        self.font = pygame.font.SysFont(None, 16)
        self.field = [[DEAD for x in range(NUM_COL)] for y in range(NUM_ROW)]
        self.generation = 0
        self.run = False
        self.cursor = [NUM_COL/2, NUM_ROW/2]  # position of cursor

        self.clear()

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.eventHandler(event)

    def clear(self):
        """init games"""
        self.generation = 0
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                self.field[y][x] = DEAD

    def rand(self):
        """add living cells randomly"""
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if random.random() < RAND_LIFE:
                    self.field[y][x] = ALIVE

    def update(self):
        if self.run:
            self.step()

    def step(self):
        # Lifegame Rules
        # 1. Any live cell with fewer than two live neighbours dies,
        #    as if caused by under-population.
        # 2. Any live cell with two or three live neighbours lives on to the next generation.
        # 3. Any live cell with more than three live neighbours dies,
        #    as if by overcrowding.
        # 4. Any dead cell with exactly three live neighbours becomes a live cell,
        #    as if by reproduction.
        next_field = [[False for x in range(NUM_COL)] for y in range(NUM_ROW)]
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                num_alive_cells = self.around(x, y)
                if num_alive_cells == 2:
                    next_field[y][x] = self.field[y][x]
                elif num_alive_cells == 3:
                    next_field[y][x] = ALIVE
                else:
                    next_field[y][x] = DEAD
        self.field = next_field
        self.generation += 1

    def draw(self, screen):
        # draw cells
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if self.field[y][x] == ALIVE:
                    pygame.draw.rect(screen, (255,255,0), Rect(x*CS,y*CS,CS,CS))
                elif self.field[y][x] == DEAD:
                    pygame.draw.rect(screen, (0,0,0), Rect(x*CS,y*CS,CS,CS))
                pygame.draw.rect(screen, (50,50,50), Rect(x*CS,y*CS,CS,CS), 1)

        # draw center line
        pygame.draw.line(screen, (255,0,0), (0,SCR_RECT.height/2), (SCR_RECT.width,SCR_RECT.height/2))
        pygame.draw.line(screen, (255,0,0), (SCR_RECT.width/2,0), (SCR_RECT.width/2,SCR_RECT.height))

        # draw cursor
        pygame.draw.rect(screen, (0,0,255), Rect(self.cursor[0]*CS,self.cursor[1]*CS,CS,CS), 1)

        # draw game information
        screen.blit(self.font.render("generation:%d" % self.generation, True, (0,255,0)), (0,0))
        screen.blit(self.font.render("space : birth/kill", True, (0,255,0)), (0,12))
        screen.blit(self.font.render("s : start/stop", True, (0,255,0)), (0,24))
        screen.blit(self.font.render("n : next", True, (0,255,0)), (0,36))
        screen.blit(self.font.render("r : random", True, (0,255,0)), (0,48))

    def around(self, x, y):
        """count live cells around (x y)"""
        # at the edge of the field
        if x == 0 or x == NUM_COL-1 or y == 0 or y == NUM_ROW-1:
            return 0

        sum = 0
        sum += self.field[y-1][x-1]  # upper left
        sum += self.field[y-1][x]    # up
        sum += self.field[y-1][x+1]  # upper right
        sum += self.field[y][x-1]    # left
        sum += self.field[y][x+1]    # right
        sum += self.field[y+1][x-1]  # lower left
        sum += self.field[y+1][x]    # down
        sum += self.field[y+1][x+1]  # lower right
        return sum

    def eventHandler(self, event):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == K_LEFT:
            self.cursor[0] -= 1
            if self.cursor[0] < 0: self.cursor[0] = 0
        elif event.key == K_RIGHT:
            self.cursor[0] += 1
            if self.cursor[0] > NUM_COL-1: self.cursor[0] = NUM_COL-1
        elif event.key == K_UP:
            self.cursor[1] -= 1
            if self.cursor[1] < 0: self.cursor[1] = 0
        elif event.key == K_DOWN:
            self.cursor[1] += 1
            if self.cursor[1] > NUM_ROW-1: self.cursor[1] = NUM_ROW-1
        elif event.key == K_SPACE:
            x, y = self.cursor
            if self.field[y][x] == DEAD:
                self.field[y][x] = ALIVE
            elif self.field[y][x] == ALIVE:
                self.field[y][x] = DEAD
        elif event.key == K_s:
            self.run = not self.run
        elif event.key == K_n:
            self.step()
        elif event.key == K_c:
            self.clear()
        elif event.key == K_r:
            self.rand()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            px, py = event.pos
            x, y = px/CS, py/CS
            self.cursor = [x, y]
            if self.field[y][x] == DEAD:
                self.field[y][x] = ALIVE
            elif self.field[y][x] == ALIVE:
                self.field[y][x] = DEAD

if __name__ == "__main__":
    LifeGame()
