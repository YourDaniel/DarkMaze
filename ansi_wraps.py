class TerminalManager:
    ESC_CHAR = '\x1b['  # \033

    def clear_line(self):
        print(self.ESC_CHAR + 'K', end='')

    def insert_character(self, character):
        print(self.ESC_CHAR + '@', end=character)

    def move_cursor_to(self, x, y):
        print(self.ESC_CHAR + str(x + 1) + ';' + str(y + 1) + 'H', end='')

    def hide_cursor(self):
        print(self.ESC_CHAR + '?25l')

    def show_cursor(self):
        print(self.ESC_CHAR + '?25h')

    def clear(self):
        print(self.ESC_CHAR + '2J')


class Color:
    bold = '\033[1m'
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    l_black = '\033[30;1m'
    l_red = '\033[31;1m'
    l_green = '\033[32;1m'
    l_yellow = '\033[33;1m'
    l_blue = '\033[34;1m'
    l_magenta = '\033[35;1m'
    l_cyan = '\033[36;1m'
    l_white = '\033[37;1m'
    reset = '\033[0m'


def print_colored(string, color, end=''):
    if color == 'black':
        print('\u001b[30m' + string + '\u001b[0m', end=end)
    elif color == 'red':
        print('\u001b[31m' + string + '\u001b[0m', end=end)
    elif color == 'green':
        print('\u001b[32m' + string + '\u001b[0m', end=end)
    elif color == 'yellow':
        print('\u001b[33m' + string + '\u001b[0m', end=end)
    elif color == 'blue':
        print('\u001b[34m' + string + '\u001b[0m', end=end)
    elif color == 'magenta':
        print('\u001b[35m' + string + '\u001b[0m', end=end)
    elif color == 'cyan':
        print('\u001b[36m' + string + '\u001b[0m', end=end)
    elif color == 'white':
        print('\u001b[37m' + string + '\u001b[0m', end=end)
    elif color == 'l_black':
        print('\u001b[30;1m' + string + '\u001b[0m', end=end)
    elif color == 'l_red':
        print('\u001b[31;1m' + string + '\u001b[0m', end=end)
    elif color == 'l_green':
        print('\u001b[32;1m' + string + '\u001b[0m', end=end)
    elif color == 'l_yellow':
        print('\u001b[33;1m' + string + '\u001b[0m', end=end)
    elif color == 'l_blue':
        print('\u001b[34;1m' + string + '\u001b[0m', end=end)
    elif color == 'l_magenta':
        print('\u001b[35;1m' + string + '\u001b[0m', end=end)
    elif color == 'l_cyan':
        print('\u001b[36;1m' + string + '\u001b[0m', end=end)
    elif color == 'l_white':
        print('\u001b[37;1m' + string + '\u001b[0m', end=end)
    else:
        raise Exception(f'No such color in the palette: {color}')
