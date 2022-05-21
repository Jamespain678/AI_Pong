from sys import argv, exit

from Classes import Game


def main():
    if len(argv) < 2:
        exit('Need some arguments [play, train]')
    elif argv[1] == 'play':
        try:
            modes = {'PvP': 0, 'PvAI': 1, 'AIvAI': 2}
            print(modes[argv[2]])
            pong = Game()
            pong.start(modes[argv[2]])
        except KeyError:
            exit(f'{argv[2]} is not valid: [PvP, PvAI, AIvAI]')
        except IndexError:
            exit('Need a mode: [PvP, PvAI, AIvAI]')
    elif argv[1] == 'train':
        pass
    else:
        exit(f'{argv[1]} is not valid: [play, train]')


if __name__ == '__main__':
    main()
