from enum import Enum
import pygame as pg


class Size(Enum):
    """Class to set a standard for diffenrent size of text"""
    TEXT = 50
    TITLE = 150


class Font(Enum):
    """Class to access the different font"""
    FONT1 = "assets/ByteBounce.ttf"


class Color(Enum):
    """Class to access with ease the different colors"""
    BLACK = (0, 0, 0)
    WHITE = (250, 250, 250)
    RED = pg.Color("deeppink3")


class Box_Button():
    """Class to create button that resize based on the text inside"""
    def __init__(self, x, y, width, height, text, size_text):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.size_text = size_text
        self.font = pg.font.Font(Font.FONT1.value, size_text)
        self.rect = pg.Rect(x, y, width + (size_text / 2 * len(self.text)), height)

    def create_button(self, screen, mouse):
        """Create and display the button"""
        self.rect.center = (self.x, self.y)
        pg.draw.rect(screen, Color.WHITE.value if self.rect.collidepoint(mouse) else Color.RED.value, self.rect)
        display_text = self.font.render(self.text, False, Color.BLACK.value)
        text_rect = display_text.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(display_text, text_rect)
        return self.rect


class Text():
    """A text class to modify the text, it's size and the background color"""
    def __init__(self, text, color, x, y, size_text):
        super().__init__()
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, 100, 100)
        self.font = pg.font.Font(Font.FONT1.value, size_text)

    def show_text(self, screen):
        """Display the text and center it based on the x and y"""
        self.rect.center = (self.x, self.y)
        pg.draw.rect(screen, Color.BLACK.value, self.rect)
        text_render = self.font.render(self.text, False, self.color)
        rect = text_render.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(text_render, rect)
