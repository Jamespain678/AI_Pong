import pygame

from config import WHITE, PADDLE_HEIGHT, PADDLE_WIDTH, VEL


class Paddle:
    COLOR = WHITE
    VEL = VEL

    def __init__(self,
                 x: int,
                 y: int,
                 width: int = PADDLE_WIDTH,
                 height: int = PADDLE_HEIGHT) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win) -> None:
        pygame.draw.rect(win,
                         self.COLOR,
                         (self.x, self.y, self.width, self.height))

    def move(self, up: bool = True) -> None:
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
