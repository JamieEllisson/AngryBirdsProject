import math
import pygame as pg
import pymunk as pm
from pymunk import Vec2d
from helper import *
from old.menu import Label


class PowerIndicator(pg.sprite.Sprite):
    def __init__(self, screen, pos, dim):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x, self.y = pos
        self.width, self.height = dim
        self.selectedPower = 0
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.rectInner = pg.Rect(self.x, self.y, self.width, self.height)

    def draw(self, power):
        size = (power / 1000) / 10
        new_width = self.width * size
        self.rectInner.width = new_width
        pg.draw.rect(self.screen, (173, 216, 230), self.rectInner, border_radius=5)
        pg.draw.rect(self.screen, "black", self.rect, 5, border_radius=5)


class AngleIndicator(pg.sprite.Sprite):
    def __init__(self, screen, pos, dim):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x, self.y = pos
        self.width, self.height = dim
        self.selectedPower = 0
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.rectInner = pg.Rect(self.x, self.y, self.width, self.height)

    def draw(self, angle):
        center = Vec2d(self.rect.center[0], self.rect.center[1])
        p = [
            (center - Vec2d(0, self.height / 2)),
            (center),
            (center + Vec2d(self.width / 2, 0)),
        ]
        x = self.width / 2 - 3

        for i in range(angle):
            new_x = x * math.cos(math.radians(-i))
            new_y = x * math.sin(math.radians(-i))
            new_line = center + Vec2d(new_x, new_y)
            pg.draw.line(self.screen, (173, 216, 230), center, new_line, 5)

        pg.draw.circle(self.screen, "black", self.rect.center, self.width / 2, 5, True)
        pg.draw.lines(self.screen, "black", False, p, 5)


class Ball(pg.sprite.Sprite):
    def __init__(self, space, screen, mass, pos):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.body = pm.Body()
        self.body.position = pos
        self.shape = pm.Circle(self.body, 10)
        self.shape.mass = mass
        self.shape.elasticity = 0.95
        self.shape.friction = 0.4
        self.body.angle = 0
        space.add(self.body, self.shape)

    def shoot(self, power):
        impulse = power * Vec2d(1, 0)
        self.body.apply_impulse_at_local_point(impulse)

    def draw(self):
        self.pos = PymunkToPygame(self.body.position)
        pg.draw.circle(self.screen, "red", self.pos, 10)


class Static(pg.sprite.Sprite):
    def __init__(self, space, screen, pos):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.pos = pos
        self.thickness = 7
        self.body = pm.Body(body_type=pm.Body.STATIC)
        self.shape = pm.Segment(self.body, pos[0], pos[1], self.thickness)
        self.shape.elasticity = 0.5
        self.shape.friction = 0.4
        space.add(self.body, self.shape)

    def draw(self, screen):
        pg.draw.line(
            screen,
            "black",
            PymunkToPygame(self.pos[0]),
            PymunkToPygame(self.pos[1]),
            self.thickness * 2,
        )


class Wall(pg.sprite.Sprite):
    def __init__(self, space, screen, pos: Vec2d, width, height):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.body = pm.Body()
        self.body.position = pos
        self.shape = pm.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.6
        self.shape.friction = 0.4
        self.shape.mass = 3
        space.add(self.body, self.shape)

    def draw(self, screen):
        p = []
        for v in self.shape.get_vertices():
            q = PymunkToPygame(v.rotated(self.body.angle) + self.body.position)
            p.append(q)

        pg.draw.polygon(screen, ("blue"), p)


class Game:
    def __init__(self, screen, cfg, clock):
        self.screen = screen
        self.cfg = cfg
        self.clock = clock
        font = self.cfg.FONT_PATH["Bungee"]
        self.space = pm.Space()
        self.space.gravity = (0, -981)
        self.floor = Static(self.space, self.screen, [(0, 50), (1280, 50)])
        self.ball = Ball(self.space, self.screen, 5, (100, 600))
        self.wall = Wall(self.space, self.screen, Vec2d(1000, 300), 100, 400)
        self.wall2 = Wall(self.space, self.screen, Vec2d(1000, 550), 400, 100)
        self.leftwall = Static(self.space, self.screen, [(0, 0), (0, 720)])
        self.rightwall = Static(self.space, self.screen, [(1280, 0), (1280, 720)])

        self.powerLabel = Label(
            self.screen,
            "POWER:",
            font,
            colour=(0, 0, 0),
            pos=(37, 85),
            size=25,
        )
        self.angleLabel = Label(
            self.screen,
            "ANGLE:",
            font,
            colour=(0, 0, 0),
            pos=(265, 85),
            size=25,
        )
        self.powerIndicator = PowerIndicator(self.screen, (17, 10), (300, 75))
        self.angleIndicator = AngleIndicator(self.screen, (275, 10), (150, 150))
        self.thingstodraw = pg.sprite.Group()
        self.thingstodraw.add(self.ball, self.wall, self.wall2)
        self.thingstodraw.add(self.floor, self.rightwall, self.leftwall)
        self.thingstodraw.add(
            self.powerIndicator, self.angleIndicator, self.powerLabel, self.angleLabel
        )

    def run(self):
        angle = 0
        power = 0

        pg.key.set_repeat(750, 100)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    QuitGame()
                if event.type == pg.KEYDOWN:
                    if (
                        event.key == pg.K_SPACE
                        and self.ball.body.velocity == Vec2d.zero()
                    ):
                        self.ball.shoot(power)
                    elif event.key == pg.K_a and power > 0:
                        power -= 1000
                    elif event.key == pg.K_d and power < 10000:
                        power += 1000
                    elif event.key == pg.K_w and self.ball.body.angle < math.radians(
                        90
                    ):
                        angle += 1
                        self.ball.body.angle = math.radians(angle)
                    elif event.key == pg.K_s and self.ball.body.angle > 0:
                        angle -= 1
                        self.ball.body.angle = math.radians(angle)

            self.screen.fill("white")
            for sprite in self.thingstodraw:
                if isinstance(sprite, Ball):
                    sprite.draw()
                elif isinstance(sprite, Wall) or isinstance(sprite, Static):
                    sprite.draw(self.screen)
                elif isinstance(sprite, PowerIndicator):
                    sprite.draw(power)
                elif isinstance(sprite, AngleIndicator):
                    sprite.draw(angle)
                elif isinstance(sprite, Label):
                    sprite.draw()
            self.powerLabel.updateText(("POWER:" + " " + str(power)))
            self.angleLabel.updateText(("ANGLE:" + " " + str(angle) + "°"))
            pg.display.update()
            self.clock.tick(self.cfg.FPS)
            self.space.step(1 / self.cfg.FPS)
