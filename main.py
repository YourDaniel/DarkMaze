import os
import ctypes

from gamestate import GameState


if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

LOG_FOLDER = 'logs'
G_STATE = GameState(level_file='levels/simple_box.txt')


def main():
    G_STATE.show_controls()
    G_STATE.log.add_msg('Welcome to Dark Maze!')
    G_STATE.tm.hide_cursor()
    G_STATE.test_simple_box()
    while True:
        if G_STATE.input_handler():
            break
        G_STATE.turn.make_turn()
        G_STATE.level.update_scr()
        G_STATE.draw_ui()

    G_STATE.tm.show_cursor()


if __name__ == '__main__':
    main()
