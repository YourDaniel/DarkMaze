from readchar import readkey
import colorama
from colorama import Fore, Back, Style
from datetime import datetime
import ctypes
import json

from gamestate import GameState
from log import Log
from item_classes import *
from tile_classes import *
from ansi_wraps import *

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

G_STATE = GameState()
G_STATE.load_level('levels/test_big_level.txt')
drop_keys = ('q', 'w', 'e', 'r', 't', 'y', 'a', 's', 'd', 'f', 'g', 'h')

def place_object(obj, x, y):
    G_STATE.level[x][y].add_object(obj)


def remove_object(obj, x, y):
    G_STATE.level[x][y].delete_object(obj)


def lower_letter(obj):
        return obj.name[:1].lower() + obj.name[1:]


class Inventory:
    content = []
    inv_line = 0                         # Inventory starts from top of the window
    inv_row = len(G_STATE.level[0]) + 1  # Inventory as far to the right as width of the map + border


    def add_item(self, obj):
        self.content.append(obj)
        self.draw()

    def remove_item(self, obj_id):
        for i in range(len(self.content)):
            if self.content[i].id == obj_id:
                del self.content[i]
                break
        self.draw()

    def drop_item(self, obj_n):
        place_object(self.content[obj_n], HERO.x_pos, HERO. y_pos)
        LOG.add_msg(f'You dropped {self.content[obj_n].name_a}.')
        del self.content[obj_n]
        self.draw()

    # TODO: Move inventory screen on the right side
    def draw(self):
        print(Fore.LIGHTYELLOW_EX, end='')
        move_cursor_to(self.inv_line, self.inv_row)
        print('Inventory:')
        self.clear_lines()
        move_cursor_to(self.inv_line + 1, self.inv_row)
        if len(self.content) == 0:
            print('Your backpack is empty')
        else:
            for i in range(len(self.content)):
                move_cursor_to(self.inv_line + 1 + i, self.inv_row)
                clear_line()
                print(f'[{drop_keys[i]}]', end=' ')
                print(self.content[i].name, end='')
        print(Style.RESET_ALL, end='')

    def clear_lines(self):
        for i in range(len(drop_keys)):
            move_cursor_to(self.inv_line + 1 + i, self.inv_row)
            clear_line()

    def item_inside(self, obj):
        if any(isinstance(i, obj) for i in self.content):
            return True
        else:
            return False


class Hero:
    id = 0
    tile_char = '☻'

    def __init__(self, x_position, y_position, name):
        self.x_pos = x_position
        self.y_pos = y_position
        self.name = name

    def open(self, x, y):
        obj_name = G_STATE.level[x][y].name_a
        if G_STATE.level[x][y].is_closed:
            if INVENTORY.item_inside(Key):
                G_STATE.upd_chars.append((x, y))
                G_STATE.upd_chars.append((self.x_pos, self.y_pos))
                G_STATE.level[x][y].open()
                INVENTORY.remove_item(Key.id)
                LOG.add_msg(f'You opened {obj_name}.')
            else:
                LOG.add_msg(f'You need to find a key to open {obj_name}.')
        else:
            LOG.add_msg(f"You can't open {obj_name}.")

    def move(self, x, y):
        try:
            if G_STATE.level[x][y].can_walk_on:
                G_STATE.upd_chars.append((x, y))
                G_STATE.upd_chars.append((self.x_pos, self.y_pos))
                place_object(self, x, y)
                remove_object(self, self.x_pos, self.y_pos)
                self.x_pos = x
                self.y_pos = y
                return True
            else:
                try:
                    self.open(x, y)
                except AttributeError:
                    LOG.add_msg("You can't move here.")
        except IndexError:
            LOG.add_msg("You can't move here.")

    def grab(self):
        objects_below = G_STATE.level[self.x_pos][self.y_pos].objects_on
        tile_name = G_STATE.level[self.x_pos][self.y_pos].name_a
        for i in range(len(objects_below)-1, -1, -1):
            # Check if picked item is not a Hero since he has id = 0
            # TODO: Fix this dirty hack
            if objects_below[i].id != 0:
                INVENTORY.add_item(objects_below[i])
                obj_name = objects_below[i].name_a
                remove_object(objects_below[i], self.x_pos, self.y_pos)
                G_STATE.upd_chars.append((self.x_pos, self.y_pos))
                LOG.add_msg(f'You grabbed {obj_name} from {tile_name}.')
                break
        else:
            LOG.add_msg('There are no items here.')

    def drop(self):
        if len(INVENTORY.content) == 0:
            LOG.add_msg('You have no items in your backpack.')
            return False
        LOG.add_msg('Select an item to drop. Press C to cancel')
        while True:
            key_pressed = readkey()
            for i, key in enumerate(drop_keys):
                if key_pressed == key:
                    INVENTORY.drop_item(i)
                    return True
                elif key_pressed == 'c':
                    LOG.add_msg('You changed your mind on dropping something.')
                    return False
                else:
                    LOG.add_msg('Select a proper item in your backpack.')
                    break


# TODO: Rework positioning in the file and remove classes from it

LOG = Log(log_len=10, timestamps=False, log_to_file=False, filename='logs.txt', log_line=len(G_STATE.level))
HERO = Hero(2, 53, 'Daniel')  # Test coordinates for 1 lvl
INVENTORY = Inventory()


# TODO: Remove all logic from input_handler, use it only for appropriate calls
def input_handler():
    key_pressed = readkey()
    if key_pressed == 'w':
        HERO.move(HERO.x_pos - 1, HERO.y_pos)
    elif key_pressed == 'a':
        HERO.move(HERO.x_pos, HERO.y_pos - 1)
    elif key_pressed == 's':
        HERO.move(HERO.x_pos + 1, HERO.y_pos)
    elif key_pressed == 'd':
        HERO.move(HERO.x_pos, HERO.y_pos + 1)
    elif key_pressed == 'p':
        LOG.add_msg(f'Hero position: ({HERO.x_pos},{HERO.y_pos})')
    elif key_pressed == 'g':
        HERO.grab()
    elif key_pressed == 't':
        HERO.drop()
    elif key_pressed == '\x1b':
        LOG.add_msg('Exiting the game...')
        return True
    elif key_pressed == 'l':  # Look
        objects_below = G_STATE.level[HERO.x_pos][HERO.y_pos].objects_on
        tile_below = G_STATE.level[HERO.x_pos][HERO.y_pos]
        if len(objects_below) > 1:
            LOG.add_msg(f'You see {objects_below[-2].description[:1].lower()}{objects_below[-2].description[1:]}')
        else:
            LOG.add_msg(f'You see {tile_below.description[:1].lower()}{tile_below.description[1:]}')
    else:
        input_handler()


def main():
    # TODO: Move this functionality to Log class
    if LOG.log_to_file:
        now = datetime.today()
        log_file = open('logs.txt', 'a')
        log_file.write('-------------------------------------\n')
        log_file.write(now.strftime("Game session at %H:%M:%S on %d.%m.%Y\n"))
    # TODO: Do not use colorama, remove all calls to it
    colorama.init()
    #data = open('data', 'w')
    #json.dump(G_STATE.level, data)
    '''
    place_object(Key(), 2, 2)
    place_object(Diamond(), 1, 4)
    place_object(Key(), 5, 14)
    place_object(Ace(), 5, 14)
    place_object(Ace(), 5, 15)
    place_object(Diamond(), 5, 16)
    place_object(Diamond(), 5, 16)
    place_object(Diamond(), 5, 16)
    place_object(Diamond(), 5, 16)
    place_object(Diamond(), 5, 16)
    place_object(Diamond(), 5, 16)
    place_object(Diamond(), 5, 16)
    place_object(Diamond(), 5, 16)
    place_object(Key(), 4, 14)
    '''
    place_object(Diamond(), 2, 6)
    place_object(Diamond(), 2, 6)
    place_object(Diamond(), 2, 6)
    place_object(Key(), 9, 47)
    place_object(Key(), 9, 48)
    place_object(Ace(), 16, 40)
    place_object(Key(), 16, 40)
    place_object(Key(), 15, 47)
    place_object(Key(), 16, 53)
    place_object(HERO, HERO.x_pos, HERO.y_pos)
    LOG.add_msg('WASD for movement, L - look, G - grab, T - drop, ESC - exit')
    #LOG.add_msg('Find a diamond!')
    LOG.add_msg('Welcome to Dark Maze!')
    hide_cursor()
    G_STATE.draw_level()
    INVENTORY.draw()
    LOG.draw()
    while True:
        if input_handler():
            break
        G_STATE.update_scr()
    colorama.deinit()


if __name__ == '__main__':
    main()
