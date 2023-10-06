import sys
import pygame as pg
from helper import *


class InterfaceComponenet(pg.sprite.Sprite):
    def __init__(self, screen, pos, dim, text, font, size, colour=(0, 0, 0)):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x, self.y = pos
        self.width, self.height = dim
        self.colour = colour
        self.font = pg.font.Font(font, size)
        self.text = self.font.render(text, False, self.colour)

    def add_text(self):
        self.pos = self.text.get_rect()
        self.pos.center = (self.x + self.width / 2, self.y + self.height / 2)


class Label(InterfaceComponenet):
    def __init__(
        self,
        screen,
        text,
        font,
        pos=(512, 100),
        dim=(256, 50),
        size=50,
        colour=(255, 255, 255),
    ):
        super().__init__(screen, pos, dim, text, font, size, colour)

    def draw(self):
        if hasattr(self, "text"):
            self.add_text()
            self.screen.blit(self.text, self.pos)

    def updateText(self, text):
        self.text = self.font.render(text, False, self.colour)


class Button(InterfaceComponenet):
    def __init__(
        self, screen, text, font, pos=(496, 60), dim=(288, 50), size=28, locked=None
    ):
        super().__init__(screen, pos, dim, text, font, size)

        self.active_colour = (255, 0, 0)
        self.non_active_colour = (0, 255, 0)
        self.locked = locked
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def isSelected(self):
        mouse_pos = pg.mouse.get_pos()
        if (self.x < mouse_pos[0] < self.x + self.width) and (
            self.y < mouse_pos[1] < self.y + self.height
        ):
            return True
        return False

    def draw(self, y):
        self.y = self.rect.y = y

        if self.locked == True != None:
            pg.draw.rect(self.screen, (50, 50, 50), self.rect, border_radius=10)
        else:
            if self.isSelected():
                pg.draw.rect(
                    self.screen, self.active_colour, self.rect, border_radius=10
                )
            else:
                pg.draw.rect(
                    self.screen, self.non_active_colour, self.rect, border_radius=10
                )
        if hasattr(self, "text"):
            self.add_text()
            self.screen.blit(self.text, self.pos)


class Menu:
    def __init__(self, screen, cfg, clock):
        self.state = True
        self.menu = "main"
        self.levelNumber = 0
        self.screen = screen
        self.clock = clock
        self.cfg = cfg
        font = self.cfg.FONT_PATH["Bungee"]
        self.mainLabel = Label(self.screen, "MAIN MENU", font)
        self.howtoplayLabel = Label(self.screen, "HOW TO PLAY", font)
        self.settingsLabel = Label(self.screen, "SETTINGS MENU", font)
        self.levelsLabel = Label(self.screen, "LEVEL SELECTOR", font)
        self.playButton = Button(self.screen, "PLAY", font)
        self.howtoplayButton = Button(self.screen, "HOW TO PLAY", font)
        self.quitButton = Button(self.screen, "QUIT GAME", font)
        self.level1Button = Button(self.screen, "LEVEL 1", font)
        self.level2Button = Button(self.screen, "LEVEL 2", font, locked=True)
        self.settingsButton = Button(self.screen, "SETTINGS", font)
        self.backButton = Button(self.screen, "BACK", font)
        self.components = pg.sprite.Group()

    def drawComponenets(self):
        i = 0
        for component in self.components:
            if isinstance(component, Label):
                component.draw()
            elif isinstance(component, Button):
                y = 200 + (i - 1) * 80
                component.draw(y)
            i += 1

    def mainMenu(self):
        self.components.empty()
        self.components.add(
            self.mainLabel,
            self.playButton,
            self.howtoplayButton,
            self.settingsButton,
            self.quitButton,
        )
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.playButton.isSelected():
                        self.menu = "levels"
                        return
                    elif self.settingsButton.isSelected():
                        self.menu = "options"
                        return
                    elif self.howtoplayButton.isSelected():
                        self.menu = "howtoplay"
                        return
                    elif self.quitButton.isSelected():
                        QuitGame()

            self.screen.fill(self.cfg.BG_COLOUR)
            self.drawComponenets()
            pg.display.update()
            self.clock.tick(self.cfg.FPS)

    def optionsMenu(self):
        self.components.empty()
        self.components.add(self.settingsLabel, self.backButton)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.backButton.isSelected():
                        self.menu = "main"
                        return

            self.screen.fill(self.cfg.BG_COLOUR)
            self.drawComponenets()
            pg.display.update()
            self.clock.tick(self.cfg.FPS)

    def howtoplayMenu(self):
        self.components.empty()
        self.components.add(self.howtoplayLabel, self.backButton)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.backButton.isSelected():
                        self.menu = "main"
                        return

            self.screen.fill(self.cfg.BG_COLOUR)
            self.drawComponenets()
            pg.display.update()
            self.clock.tick(self.cfg.FPS)

    def levelSelectorMenu(self):
        self.components.empty()
        self.components.add(
            self.levelsLabel, self.level1Button, self.level2Button, self.backButton
        )
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.backButton.isSelected():
                        self.menu = "main"
                        return
                    elif self.level1Button.isSelected():
                        self.level2Button.locked = False
                        return
                    elif self.level2Button.isSelected():
                        self.levelNumber = 2
                        self.state = False
                        return

            self.screen.fill(self.cfg.BG_COLOUR)
            self.drawComponenets()
            pg.display.update()
            self.clock.tick(self.cfg.FPS)

    def controller(self):
        if self.menu == "main":
            self.mainMenu()
        elif self.menu == "options":
            self.optionsMenu()
        elif self.menu == "howtoplay":
            self.howtoplayMenu()
        elif self.menu == "levels":
            self.levelSelectorMenu()
