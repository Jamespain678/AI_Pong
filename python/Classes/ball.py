from random import randint

import pygame

from config import MAX_VEL, WHITE, BALL_RADIUS, WIDTH, HEIGHT


class Ball:
    MAX_VEL = MAX_VEL
    COLOR = WHITE

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.x_vel = self.MAX_VEL
        self.y_vel = randint(0, self.MAX_VEL)

    def draw(self, win) -> None:
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self) -> None:
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self) -> None:
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.y_vel = randint(0, self.MAX_VEL)
