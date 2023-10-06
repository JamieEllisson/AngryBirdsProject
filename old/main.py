import os
import sys
import pygame as pg
import pymunk as pm
from helper import *
from old.menu import Menu
from old.game import Game


class Config:
    rootdir = os.path.dirname(os.path.realpath(__file__))
    TITLE = "TTT"
    SCREENSIZE = 1280, 720
    FPS = 120
    BG_COLOUR = (51, 51, 51)
    FONT_PATH = {
        "Bungee": os.path.join(rootdir, "assets", "fonts", "BungeeSpice-Regular.ttf")
    }


class AngryBirds:
    def __init__(self):
        self.cfg = Config
        pg.init()
        self.display = pg.display.set_mode(self.cfg.SCREENSIZE)
        self.clock = pg.time.Clock()
        self.menu = Menu(self.display, self.cfg, self.clock)
        self.game = Game(self.display, self.cfg, self.clock)

    def run(self):
        cfg = self.cfg
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.display.fill(cfg.BG_COLOUR)
            if self.menu.state:
                self.menu.controller()
            elif not self.menu.state:
                self.game.run()
            else:
                pass
            pg.display.update()
            self.clock.tick(cfg.FPS)


def main():
    game = AngryBirds()
    game.run()
    QuitGame()


if __name__ == "__main__":
    main()
