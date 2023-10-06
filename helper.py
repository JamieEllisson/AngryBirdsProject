import sys
import pygame as pg


def QuitGame():
    pg.quit()
    sys.exit()


def PymunkToPygame(point):
    HEIGHT = 720
    return int(point[0]), int(HEIGHT - point[1])
