import pygame as pg

from config import FONT_PATH, WHITE, BLACK, RED, GREEN, GREY


class MenuComponent(pg.sprite.Sprite):
    def __init__(self, surface, text, pos, size, font_size, colour=BLACK):
        pg.sprite.Sprite.__init__(self)
        self.surface = surface
        self.x, self.y = pos
        self.width, self.height = size
        self.colour = colour
        self.font = pg.font.Font(FONT_PATH["Bungee"], font_size)
        self.text = self.font.render(text, False, self.colour)

    def add_text(self):
        self.pos = self.text.get_rect()
        self.pos.center = (self.x + self.width / 2, self.y + self.height / 2)

    def updateText(self, text):
        self.text = self.font.render(text, False, self.colour)


class Label(MenuComponent):
    def __init__(
        self,
        surface,
        text,
        pos=(512, 100),
        size=(256, 50),
        font_size=50,
        colour=WHITE,
    ):
        super().__init__(surface, text, pos, size, font_size, colour)

    def draw(self):
        if hasattr(self, "text"):
            self.add_text()
            self.surface.blit(self.text, self.pos)


class Button(MenuComponent):
    def __init__(
        self,
        surface,
        text,
        pos=(496, 60),
        size=(288, 50),
        font_size=28,
        locked=None,
        action=None,
    ):
        super().__init__(surface, text, pos, size, font_size)
        self.hover_colour = RED
        self.colour = GREEN
        self.locked = locked
        self.action = action
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def isHovered(self):
        mouse_pos = pg.mouse.get_pos()
        if (self.x < mouse_pos[0] < self.x + self.width) and (
            self.y < mouse_pos[1] < self.y + self.height
        ):
            return True
        return False

    def draw(self, y):
        self.y = self.rect.y = y

        if self.locked == True != None:
            pg.draw.rect(self.surface, GREY, self.rect, border_radius=10)
        else:
            if self.isHovered():
                pg.draw.rect(
                    self.surface, self.hover_colour, self.rect, border_radius=10
                )
            else:
                pg.draw.rect(self.surface, self.colour, self.rect, border_radius=10)
        if hasattr(self, "text"):
            self.add_text()
            self.surface.blit(self.text, self.pos)