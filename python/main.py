from sys import argv, exit
import pickle

import neat

from Classes import Game
from config import CONFIG_NEAT_PATH


def eval_genomes(genomes, config) -> None:
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            game = Game()
            game.train_ai(genome1, genome2, config)


def run_neat_training() -> None:
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         CONFIG_NEAT_PATH)
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-xx')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 50)
    with open('best.pickle', 'wb') as f:
        pickle.dump(winner, f)


def main() -> None:
    if len(argv) < 2:
        exit('Need some arguments [play, train]')
    elif argv[1] == 'play':
        try:
            modes = {'PvP': 0, 'PvAI': 1, 'AIvAI': 2}
            pong = Game()
            pong.play(modes[argv[2]])
        except KeyError:
            exit(f'{argv[2]} is not valid: [PvP, PvAI, AIvAI]')
        except IndexError:
            exit('Need a mode: [PvP, PvAI, AIvAI]')
    elif argv[1] == 'train':
        run_neat_training()
    else:
        exit(f'{argv[1]} is not valid: [play, train]')


if __name__ == '__main__':
    main()
