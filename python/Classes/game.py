import pygame

from config import PADDLE_HEIGHT, PADDLE_WIDTH, WIDTH, HEIGHT
from config import FPS, BLACK, WHITE, WINNING_SCORE
from .paddle import Paddle
from .ball import Ball


class Game():
    def __init__(self) -> None:
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Pong')
        self.run = True
        self.clock = pygame.time.Clock()
        self.left_paddle = Paddle(10,
                                  HEIGHT//2 - PADDLE_HEIGHT // 2,
                                  -1)
        self.right_paddle = Paddle(WIDTH - PADDLE_WIDTH - 10,
                                   HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                   1)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2)
        self.start()

    def start(self) -> None:
        while self.run:
            # FPS control
            self.clock.tick(FPS)
            # Draw window
            self.draw()
            # Events
            self.ball.move()
            self.handle_collisions()
            self.handle_score()
            # Close
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
            # Keys
            self.handle_key_inputs()
        pygame.quit()

    def draw(self) -> None:
        self.win.fill(BLACK)
        self.left_paddle.draw(self.win)
        self.right_paddle.draw(self.win)
        self.ball.draw(self.win)
        pygame.draw.rect(self.win,
                         WHITE,
                         (WIDTH // 2 - 1,
                          0,
                          2,
                          HEIGHT))
        pygame.display.update()

    def handle_key_inputs(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.left_paddle.y - self.left_paddle.VEL >= 0:
            self.left_paddle.move(up=True)
        if keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.VEL <= HEIGHT - PADDLE_HEIGHT:
            self.left_paddle.move(up=False)
        if keys[pygame.K_i] and self.right_paddle.y - self.right_paddle.VEL >= 0:
            self.right_paddle.move(up=True)
        if keys[pygame.K_k] and self.right_paddle.y + self.right_paddle.VEL <= HEIGHT - PADDLE_HEIGHT:
            self.right_paddle.move(up=False)

    def handle_collisions(self):
        # Borders
        if self.ball.y + self.ball.radius >= HEIGHT or self.ball.y - self.ball.radius <= 0:
            self.ball.y_vel *= -1
        # Paddles
        if self.ball.x_vel < 0:
            self.ball.x_vel, self.ball.y_vel = self.left_paddle.ball_colide(self.ball)
        else:
            self.ball.x_vel, self.ball.y_vel = self.right_paddle.ball_colide(self.ball)

    def handle_score(self):
        if self.ball.x < 0:
            self.right_paddle.score += 1
            self.reset()
        elif self.ball.x > WIDTH:
            self.left_paddle.score += 1
            self.reset()
        if self.right_paddle.score >= WINNING_SCORE or self.left_paddle.score >= WINNING_SCORE:
            self.run = False

    def reset(self):
        self.ball.reset()
        self.left_paddle.y = HEIGHT//2 - PADDLE_HEIGHT // 2
        self.right_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
