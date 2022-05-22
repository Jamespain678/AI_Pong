import pickle

import pygame
import neat

from config import PADDLE_HEIGHT, PADDLE_WIDTH, WIDTH, HEIGHT
from config import FPS, BLACK, WHITE, WINNING_SCORE, CONFIG_NEAT_PATH
from .paddle import Paddle
from .ball import Ball


class Game():
    """Class for handle the game"""

    def __init__(self) -> None:
        """Init the game"""
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Pong')
        self.run = True
        self.clock = pygame.time.Clock()
        self.left_paddle = Paddle(10,
                                  HEIGHT//2 - PADDLE_HEIGHT//2,
                                  -1)
        self.right_paddle = Paddle(WIDTH - PADDLE_WIDTH - 10,
                                   HEIGHT//2 - PADDLE_HEIGHT//2,
                                   1)
        self.ball = Ball(WIDTH//2, HEIGHT//2)

    def play(self, mode: int) -> None:
        """Starts the game
        Args:
            mode (int): Mode (0 PvP, 1 PvAI, 2 AIvAI)
        """
        if mode == 0:
            self.play_PvP()
        elif mode == 1:
            self.play_PvAI()
        elif mode == 2:
            self.play_AIvAI()

    def play_PvP(self) -> None:
        """Loop fro PvP game"""
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
            self.handle_key_inputs_PvP()
        pygame.quit()

    def play_PvAI(self):
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             CONFIG_NEAT_PATH)
        with open('best.pickle', 'rb') as f:
            genome = pickle.load(f)
        self.net2 = neat.nn.FeedForwardNetwork.create(genome, config)
        """Loop fro PvAI game"""
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
            self.handle_key_inputs_PvAI()
            out2 = self.net2.activate(self.right_paddle.get_inputs(self.ball))
            self.right_paddle.move(out2.index(max(out2)) - 1)
        pygame.quit()

    def play_AIvAI(self):
        """Loop for AIvAI game"""
        pass

    def draw(self) -> None:
        """Refresh window"""
        self.win.fill(BLACK)
        self.left_paddle.draw(self.win)
        self.right_paddle.draw(self.win)
        self.ball.draw(self.win)
        pygame.draw.rect(self.win,
                         WHITE,
                         (WIDTH//2 - 1,
                          0,
                          2,
                          HEIGHT))
        pygame.display.update()

    def handle_key_inputs_PvP(self) -> None:
        """Key movements for PvP"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move(direction=1)
        if keys[pygame.K_s]:
            self.left_paddle.move(direction=-1)
        if keys[pygame.K_i]:
            self.right_paddle.move(direction=1)
        if keys[pygame.K_k]:
            self.right_paddle.move(direction=-1)

    def handle_key_inputs_PvAI(self) -> None:
        """Key movements for PvAI"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move(direction=1)
        if keys[pygame.K_s]:
            self.left_paddle.move(direction=-1)

    def handle_collisions(self):
        """Collisions of the ball"""
        # Borders
        if self.ball.y + self.ball.radius >= HEIGHT or self.ball.y - self.ball.radius <= 0:
            self.ball.y_vel *= -1
        # Paddles
        if self.ball.x_vel < 0:
            self.left_paddle.ball_colide(self.ball)
        else:
            self.right_paddle.ball_colide(self.ball)

    def handle_score(self) -> None:
        """Manage the win and the score"""
        if self.ball.x < 0:
            self.right_paddle.score += 1
            self.reset()
        elif self.ball.x > WIDTH:
            self.left_paddle.score += 1
            self.reset()
        if self.right_paddle.score >= WINNING_SCORE or self.left_paddle.score >= WINNING_SCORE:
            self.run = False

    def reset(self) -> None:
        """Restart the game"""
        self.ball.reset()
        self.left_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2
        self.right_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2

    def train_ai(self, genome1, genome2, config) -> None:
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.run_train = True
        while self.run_train:
            # Close
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
            out1 = net1.activate(self.left_paddle.get_inputs(self.ball))
            self.left_paddle.move(out1.index(max(out1)) - 1)
            out2 = net2.activate(self.right_paddle.get_inputs(self.ball))
            self.right_paddle.move(out2.index(max(out2)) - 1)
            # Loop
            self.ball.move()
            self.handle_collisions()
            self.handle_score()
            # End loop
            if self.right_paddle.score >= 1 or self.left_paddle.score >= 1 or self.right_paddle.hits >= 50:
                self.calculate_fitness(genome1, genome2)
                break
            # self.draw()

    def calculate_fitness(self, genome1, genome2) -> None:
        genome1.fitness += self.left_paddle.hits + len(self.left_paddle.movement_score)
        genome2.fitness += self.right_paddle.hits + len(self.right_paddle.movement_score)
