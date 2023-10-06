import math
import pygame as pg
import pymunk as pm
from helper import *
from old.game import Ball, Wall
from pymunk import Vec2d


class Level:
    def __init__(self, space, screen):
        self.obstacles = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.space = space
        self.screen = screen

    def load_level(self, levelNumber):
        if levelNumber == 1:
            self.level1()

    def level1(self):
        ball = Ball(self.space, self.screen, 5, (100, 600))
        wall = Wall(self.space, self.screen, Vec2d(1000, 300), 100, 400)
        wall2 = Wall(self.space, self.screen, Vec2d(1000, 550), 400, 100)
        self.balls.add(ball)
        self.obstacles.add(wall, wall2)
