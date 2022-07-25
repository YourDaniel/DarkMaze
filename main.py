import os
import ctypes

import colorama
from gamestate import GameState


if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

LOG_FOLDER = 'logs'
G_STATE = GameState(level_file='levels/simple_box.txt')


def main():
    G_STATE.log.add_msg('WASD for movement, L - look, G - grab, T - drop, ESC - exit')
    G_STATE.log.add_msg('Welcome to Dark Maze!')
    G_STATE.tm.hide_cursor()
    G_STATE.test_simple_box()
    G_STATE.log.draw()
    while True:
        if G_STATE.input_handler():
            break
        G_STATE.level.update_scr()
    G_STATE.tm.show_cursor()


if __name__ == '__main__':
    main()
