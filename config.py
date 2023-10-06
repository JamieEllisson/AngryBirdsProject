import os
import pygame

rootdir = os.path.dirname(os.path.realpath(__file__))
TITLE = "Computer Science Project"
SCREENSIZE = 1280, 720
FPS = 120
FONT_PATH = {
    "Bungee": os.path.join(rootdir, "assets", "fonts", "BungeeSpice-Regular.ttf")
}
BG_COLOUR = (51, 51, 51)

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
