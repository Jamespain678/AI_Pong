import pygame

from config import WHITE, PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_VEL, WIDTH, HEIGHT, MAX_BALL_VEL
from .ball import Ball

pygame.init()
SCORE_FONT = pygame.font.SysFont('calibri', 50)


class Paddle:
    """Class for handle paddles"""
    COLOR = WHITE

    def __init__(self,
                 x: int,
                 y: int,
                 side: int) -> None:
        """Init paddle
        Args:
            x (int): x position
            y (int): y position
            side (int): side of the paddle (-1 left, 1 right)
        """
        self.x = x
        self.y = y
        self.side = side
        self.score = 0

    def draw(self, win: pygame.Surface) -> None:
        """Draw the paddle on the window
        Args:
            win (pygame.Surface): window
        """
        pygame.draw.rect(win,
                         self.COLOR,
                         (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))
        score_text = SCORE_FONT.render(f'{self.score}', 1, WHITE)
        score_pos = (WIDTH//2) + self.side * (WIDTH//4) - (score_text.get_width()//2)
        win.blit(score_text, (score_pos, 20))

    def move(self, direction: int = 0) -> None:
        """Move the paddle
        Args:
            direction (int, optional): direction of movement (-1 down, 0 don't move, 1 up).
                                       Defaults to 0.
        """
        new_pos = self.y - PADDLE_VEL * direction
        if new_pos <= 0:
            direction = 0
        elif new_pos >= HEIGHT - PADDLE_HEIGHT:
            direction = 0
        self.y -= PADDLE_VEL*direction

    def ball_colide(self, ball: Ball) -> None:
        """Check colisions with the ball. If true, change the ball vel
        Args:
            ball (Ball): Ball
        """
        y_col = x_col = False
        y_col = self.y < ball.y < self.y + PADDLE_HEIGHT
        if self.side == -1:
            x_col = ball.x - ball.radius < self.x + PADDLE_WIDTH
        else:
            x_col = ball.x + ball.radius > self.x
        if y_col and x_col:
            middle_y = self.y + PADDLE_HEIGHT//2
            diff_y = middle_y - ball.y
            y_vel = - (diff_y * MAX_BALL_VEL) // (PADDLE_HEIGHT//2)
            ball.y_vel = y_vel
            ball.x_vel *= -1
