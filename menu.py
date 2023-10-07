import pygame as pg

from game import Game
from sprites import Label, Button
from config import BG_COLOUR, BLACK, FPS


class Menu:
    def __init__(self, game: Game):
        self.game = game
        self.show_display = True
        self.components = pg.sprite.Group()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.show_display = False
                self.game.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for element in self.components:
                    if isinstance(element, Button):
                        if element.isHovered():
                            match element.action:
                                case "play":
                                    self.game.current_menu = self.game.level_menu
                                    self.show_display = False
                                case "settings":
                                    self.game.current_menu = self.game.settings_menu
                                    self.show_display = False
                                case "quit":
                                    self.game.running = False
                                    self.show_display = False
                                case "back":
                                    self.game.current_menu = self.game.main_menu
                                    self.show_display = False
                                case "level1":
                                    self.game.level_pointer = 1
                                    self.game.playing = True
                                    self.show_display = False
                                case "level2":
                                    self.game.level_pointer = 2
                                    self.game.playing = True
                                    self.show_display = False

    def draw_menu(self):
        i = 0
        for element in self.components:
            if isinstance(element, Label):
                element.draw()
            if isinstance(element, Button):
                y = 200 + (i - 1) * 80
                element.draw(y)
            i += 1

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
        self.settings = Button(self.game.display, "Settings", action="settings")
        self.quit = Button(self.game.display, "Quit", action="quit")
        self.components.add(self.title, self.play, self.settings, self.quit)


class SettingsMenu(Menu):
    def __init__(self, game: Game):
        Menu.__init__(self, game)
        self.title = Label(self.game.display, "Settings")
        self.back = Button(self.game.display, "BACK", action="back")
        self.components.add(self.title, self.back)


class LevelMenu(Menu):
    def __init__(self, game: Game):
        Menu.__init__(self, game)
        self.title = Label(self.game.display, "Level Selector")
        self.level1 = Button(self.game.display, "Level 1", action="level1")
        self.level2 = Button(self.game.display, "Level 2", action="level2")
        self.back = Button(self.game.display, "BACK", action="back")
        self.components.add(self.title, self.level1, self.level2, self.back)
