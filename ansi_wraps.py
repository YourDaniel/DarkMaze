import os


def close_terminal():
    os.system('taskkill /IM cmd.exe')


def clear_line():
    print('\x1b[K', end='')


def move_cursor_to(x, y):
    print('\x1b[' + str(x + 1) + ';' + str(y + 1) + 'H', end='')


def clear():
    print('\x1b[2J', end='')


def hide_cursor():
    print('\x1b[?25l')
