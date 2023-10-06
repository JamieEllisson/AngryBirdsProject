import pygame as pg

from game import Game
from sprites import Label, Button
from config import BG_COLOUR, BLACK, FPS


class Menu:
    def __init__(self, game: Game):
        self.game = game
        self.show_display = True
        self.components = pg.sprite.Group()

    def draw_menu(self):
        i = 0
        for element in self.components:
            if isinstance(element, Label):
                element.draw()
            if isinstance(element, Button):
                y = 200 + (i - 1) * 80
                element.draw(y)
            i += 1

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.show_display = False
                self.game.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for element in self.components:
                    if isinstance(element, Button):
                        if element.isHovered():
                            if element.action == "switch":
                                self.game.isMainMenu = not self.game.isMainMenu
                                self.show_display = False
                            if element.action == "quit":
                                self.game.running = False
                                self.show_display = False
                            if element.action == "play":
                                self.game.playing = True
                                self.show_display = False

    def show(self):
        self.show_display = True
        while self.show_display:
            self.check_events()
            self.game.display.fill(BG_COLOUR)
            self.draw_menu()
            self.blit_screen()
            self.game.clock.tick(FPS)

    def blit_screen(self):
        self.game.screen.blit(self.game.display, (0, 0))
        pg.display.update()


class MainMenu(Menu):
    def __init__(self, game: Game):
        Menu.__init__(self, game)
        self.title = Label(self.game.display, "Main Menu")
        self.play = Button(self.game.display, "Play", action="play")
        self.settings = Button(self.game.display, "Settings", action="switch")
        self.quit = Button(self.game.display, "Quit", action="quit")
        self.components.add(self.title, self.play, self.settings, self.quit)


class SettingsMenu(Menu):
    def __init__(self, game: Game):
        Menu.__init__(self, game)
        self.title = Label(self.game.display, "Settings")
        self.back = Button(self.game.display, "BACK", action="switch")
        self.components.add(self.title, self.back)
