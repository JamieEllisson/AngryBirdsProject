import pygame as pg
import pymunk as pm

from game import Game
from pymunk import Vec2d
from sprites import Floor, Ball
from config import FPS, WHITE


class Level:
    def __init__(self, game: Game):
        self.game = game
        self.space = pm.Space()
        self.space.gravity = Vec2d(0, -981)
        self.inLevel = True

    def load_level(self):
        self.sprites = pg.sprite.Group()
        if self.game.level_pointer == 1:
            floor = Floor(self.game.display, self.space, (0, 50), (1280, 50))
            ball = Ball(self.game.display, self.space, (100, 600))
            self.sprites.add(floor, ball)

    def draw_level(self):
        for sprite in self.sprites:
            if isinstance(sprite, (Floor, Ball)):
                sprite.draw()

    def start(self):
        self.load_level()
        self.inLevel = True
        while self.inLevel:
            self.game.check_events()
            self.game.display.fill(WHITE)
            self.draw_level()
            self.game.screen.blit(self.game.display, (0, 0))
            pg.display.update()
            self.game.clock.tick(FPS)
            self.space.step(1 / FPS)
