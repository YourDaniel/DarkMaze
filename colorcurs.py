import colorama
from colorama import Fore, Back, Style


def pos(x, y):
    return '\x1b[' + str(x + 1) + ';' + str(y + 1) + 'H'


colorama.init()
print(Fore.RED, end='')
print(pos(4, 1), end='')
print('Some cool text!')
print(pos(4, 2), end='')
print('ZZZZ')
print(pos(25, 30), end='')