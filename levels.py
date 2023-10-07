import pygame as pg
import pymunk as pm

from game import Game


class Level:
    def __init__(self, game: Game):
        self.game = game
