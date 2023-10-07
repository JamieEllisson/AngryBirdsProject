import pygame as pg


from config import TITLE, SCREENSIZE, FPS, BG_COLOUR


class Game:
    def __init__(self):
        from menu import MainMenu, SettingsMenu, LevelMenu
        from levels import Level

        pg.init()
        self.screen = pg.display.set_mode(SCREENSIZE)
        pg.display.set_caption(TITLE)
        self.display = pg.Surface(SCREENSIZE)
        self.clock = pg.time.Clock()
        self.running, self.playing = True, False
        self.main_menu = MainMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.level_menu = LevelMenu(self)
        self.current_menu = self.main_menu

        self.level = Level(self)
        self.level_pointer = 0

    def game_loop(self):
        while self.playing:
            self.check_events()
            self.display.fill(BG_COLOUR)
            self.screen.blit(self.display, (0, 0))
            pg.display.update()
            self.clock.tick(FPS)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
            if event.type == pg.MOUSEBUTTONDOWN:
                self.running, self.playing = True, False
