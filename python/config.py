from os import path


WIDTH, HEIGHT = 600, 500
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_VEL = 4
MAX_BALL_VEL = 5
BALL_RADIUS = 7
WINNING_SCORE = 5
DRAW_HITS = True

APPLICATION_PATH = path.abspath(path.join(path.dirname(__file__), '..'))
CONFIG_NEAT_PATH = path.join(APPLICATION_PATH, 'config.txt')
