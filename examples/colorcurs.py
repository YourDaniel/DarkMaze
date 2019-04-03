#import colorama
#from colorama import Fore, Back, Style
#import ctypes

#kernel32 = ctypes.windll.kernel32
#kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def pos(x, y):
    return '\x1b[' + str(x + 1) + ';' + str(y + 1) + 'H'

print(pos(4, 1), end='')
print('Some cool text!')
print(pos(4, 2), end='')
print('ZZZZ')
print(pos(4, 2), end='')
print('\x1b[K', end='')  # Clear to the end of the line
print('FUCK')
print('\x1b[?25l')
