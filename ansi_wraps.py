import functools
print = functools.partial(print, flush=True)


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

    def print_colored(self, string: str, color: str, end=''):
        match color:
            case 'black':
                print(self.ESC_CHAR + '30m' + string, end='')
            case 'red':
                print(self.ESC_CHAR + '31m' + string, end='')
            case 'green':
                print(self.ESC_CHAR + '32m' + string, end='')
            case 'yellow':
                print(self.ESC_CHAR + '33m' + string, end='')
            case 'blue':
                print(self.ESC_CHAR + '34m' + string, end='')
            case 'magenta':
                print(self.ESC_CHAR + '35m' + string, end='')
            case 'cyan':
                print(self.ESC_CHAR + '36m' + string, end='')
            case 'white':
                print(self.ESC_CHAR + '37m' + string, end='')
            case 'l_black':
                print(self.ESC_CHAR + '30;1m' + string, end='')
            case 'l_red':
                print(self.ESC_CHAR + '31;1m' + string, end='')
            case 'l_green':
                print(self.ESC_CHAR + '32;1m' + string, end='')
            case 'l_yellow':
                print(self.ESC_CHAR + '33;1m' + string, end='')
            case 'l_blue':
                print(self.ESC_CHAR + '34;1m' + string, end='')
            case 'l_magenta':
                print(self.ESC_CHAR + '35;1m' + string, end='')
            case 'l_cyan':
                print(self.ESC_CHAR + '36;1m' + string, end='')
            case 'l_white':
                print(self.ESC_CHAR + '37;1m' + string, end='')
            case  _:
                raise Exception(f'No such color in the palette: {color}')
        print(self.ESC_CHAR + '0m', end=end)


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
