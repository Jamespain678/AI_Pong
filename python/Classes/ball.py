import pygame

from config import MAX_VEL, WHITE, BALL_RADIUS


class Ball:
    MAX_VEL = MAX_VEL
    COLOR = WHITE

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win) -> None:
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self) -> None:
        self.x += self.x_vel
        self.y += self.y_vel
