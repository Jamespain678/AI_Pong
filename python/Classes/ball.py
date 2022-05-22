from random import randint, choice

import pygame

from config import MAX_BALL_VEL, WHITE, BALL_RADIUS, WIDTH, HEIGHT


class Ball:
    """Class for handdle the ball"""
    COLOR = WHITE

    def __init__(self, x: int, y: int) -> None:
        """Init the ball
        Args:
            x (int): x position
            y (int): y position
        """
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.x_vel = choice((-MAX_BALL_VEL, MAX_BALL_VEL))
        self.y_vel = randint(1, MAX_BALL_VEL)

    def draw(self, win: pygame.Surface) -> None:
        """Draw the ball on the window
        Args:
            win (pygame.Surface): window
        """
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self) -> None:
        """Move the ball"""
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self) -> None:
        """Reset the ball"""
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.x_vel = choice((-MAX_BALL_VEL, MAX_BALL_VEL))
        self.y_vel = randint(1, MAX_BALL_VEL)
