import pygame as pg
import pymunk as pm

from game import Game
from pymunk import Vec2d
from sprites import Floor, Ball, Block
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
            self.floor = Floor(self.game.display, self.space, (0, 50), (1280, 50))
            self.block = Block(self.game.display, self.space, (1000, 100), 400, 100)
            self.ball = Ball(self.game.display, self.space, (100, 600))
            self.sprites.add(self.floor, self.ball, self.block)

    def draw_level(self):
        for sprite in self.sprites:
            if isinstance(sprite, (Floor, Ball, Block)):
                sprite.draw()

    def reset_space(self):
        for body in self.space.bodies:
            for shape in body:
                self.space.remove(shape)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.inLevel = False
                self.game.playing = False
                self.game.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.inLevel = False
                    self.game.playing = False
                if event.key == pg.K_SPACE:
                    self.ball.shoot(self.power)
                if event.key == pg.K_a and self.power > 0:
                    self.power -= 1000
                if event.key == pg.K_d and self.power < 10000:
                    self.power += 1000

    def start(self):
        self.load_level()
        self.inLevel = True
        self.angle, self.power = 0, 0
        while self.inLevel:
            self.check_events()
            self.game.display.fill(WHITE)
            self.draw_level()
            self.game.screen.blit(self.game.display, (0, 0))
            pg.display.update()
            self.game.clock.tick(FPS)
            self.space.step(1 / FPS)
