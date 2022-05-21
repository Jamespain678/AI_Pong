import pygame

from config import WHITE, PADDLE_HEIGHT, PADDLE_WIDTH, VEL, WIDTH, HEIGHT
from .ball import Ball

pygame.init()
SCORE_FONT = pygame.font.SysFont('calibri', 50)


class Paddle:
    COLOR = WHITE
    VEL = VEL

    def __init__(self,
                 x: int,
                 y: int,
                 side: int,
                 width: int = PADDLE_WIDTH,
                 height: int = PADDLE_HEIGHT) -> None:
        self.x = x
        self.y = y
        self.side = side  # -1 left, 1 right
        self.width = width
        self.height = height
        self.score = 0

    def draw(self, win) -> None:
        pygame.draw.rect(win,
                         self.COLOR,
                         (self.x, self.y, self.width, self.height))
        score_text = SCORE_FONT.render(f'{self.score}', 1, WHITE)
        score_pos = (WIDTH // 2) + self.side*(WIDTH // 4) - (score_text.get_width()//2)
        win.blit(score_text, (score_pos, 20))

    def move(self, direction: int = 0) -> None:
        new_pos = self.y - self.VEL*direction
        if new_pos <= 0:
            direction = 0
        elif new_pos >= HEIGHT - PADDLE_HEIGHT:
            direction = 0
        self.y -= self.VEL*direction

    def ball_colide(self, ball: Ball) -> tuple[int, int]:
        y_col = x_col = False
        y_col = self.y < ball.y < self.y + self.height
        if self.side == -1:
            x_col = ball.x - ball.radius < self.x + self.width
        else:
            x_col = ball.x + ball.radius > self.x
        if y_col and x_col:
            middle_y = self.y + self.height // 2
            diff_y = middle_y - ball.y
            y_vel = - (diff_y * ball.MAX_VEL) // (self.height // 2)
            return ball.x_vel * -1, y_vel
        return ball.x_vel, ball.y_vel
