import os
import ctypes

import colorama
from gamestate import GameState
from creature import Hero

if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

LOG_FOLDER = 'logs'

G_STATE = GameState(level_file='levels/simple_box.txt')
HERO = Hero(2, 2, 'Daniel', inv_col=G_STATE.level.get_size('width') + 1)  # Inventory as far to the right as width of the map + border


def main():
    colorama.init()
    G_STATE.log.add_msg('WASD for movement, L - look, G - grab, T - drop, ESC - exit')
    G_STATE.log.add_msg('Welcome to Dark Maze!')
    G_STATE.tm.hide_cursor()
    G_STATE.test_simple_box(HERO)
    HERO.inventory.draw()
    G_STATE.log.draw()
    while True:
        if G_STATE.input_handler():
            break

        #LOG.add_msg('Screen updated')
        #with open('debug_file.txt', 'a') as f:
        #    f.write(f'{G_STATE.upd_chars}\n')

        G_STATE.level.update_scr()

        #with open('debug_file.txt', 'a') as f:
        #   f.write(f'update_scr was called {G_STATE.upd_chars}\n')

    G_STATE.tm.show_cursor()
    colorama.deinit()


if __name__ == '__main__':
    main()


# TODO: Do not use colorama, remove all calls to it
# TODO: Remove all logic from input_handler, use it only for appropriate calls
