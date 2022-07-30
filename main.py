import os
import ctypes

from gamestate import GameState


if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

LOG_FOLDER = 'logs'
G_STATE = GameState(level_file='levels/simple_box.txt')


def main():
    G_STATE.log.add_msg('~ Misc: ESC - exit, z - get Hero coords')
    G_STATE.log.add_msg('~ Actions: (l)ook, (g)rab, dro(p), (c)lose')
    G_STATE.log.add_msg('~ Movement: wasd')
    G_STATE.log.add_msg('-- Controls --')
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
