from readchar import readkey
import colorama
from colorama import Fore, Back, Style
import tile_classes
from item_classes import Key, Diamond, Ace
from gamestate import GameState
from ansi_wraps import *
from datetime import datetime
import ctypes
import json

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
log_file = open('logs.txt', 'a')


class Log:
    messages = []
    log_line = 13  # Log starts from this row in a terminal window

    def __init__(self, log_len, timestamps):
        self.log_len = log_len
        self.timestamps_on = timestamps

    def add_msg(self, msg):
        timestamp = datetime.today().strftime("[%H:%M:%S] ")
        log_file.write(timestamp + msg + '\n')
        if len(self.messages) > 0 and self.messages[0][0] == msg:
            self.messages[0][1] += 1
        else:
            if self.timestamps_on:
                block = [timestamp + msg, 1]  # 2nd value - number of same msg
            else:
                block = [msg, 1]
            self.messages.insert(0, block)
        if len(self.messages) > self.log_len:  # Cutting log to max size
            self.messages = self.messages[:self.log_len]
        self.draw()

    def draw(self):
        print(Fore.LIGHTBLUE_EX, end='')
        # First, set cursor to a start of line where Log should be drawn with ESC sequence
        move_cursor_to(self.log_line, 0)
        for i in range(len(self.messages)):
            msg_text = self.messages[i][0]
            msg_count = self.messages[i][1]
            # Then clear old message to print out a new one
            clear_line()
            if msg_count > 1:
                print(f'{msg_text} x {msg_count}')
            else:
                print(msg_text)
        print(Style.RESET_ALL, end='')


class Inventory:
    content = []
    inv_line = 10  # Inventory starts from this row in console
    drop_keys = ('q', 'w', 'e', 'r', 't', 'y', 'a', 's', 'd', 'f', 'g', 'h')

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

    def draw(self):
        move_cursor_to(self.inv_line, 0)
        print(Fore.LIGHTYELLOW_EX, end='')
        print('Inventory:')
        clear_line()
        if len(self.content) == 0:
            print('Your backpack is empty')
        else:
            for i in range(len(self.content)):
                print(f'[{self.drop_keys[i]}]', end=' ')
                if i+1 != len(self.content):
                    print(self.content[i].name, end=', ')
                else:
                    print(self.content[i].name + '.')
        print('-' * 20)
        print(Style.RESET_ALL, end='')

    def item_inside(self, obj):
        if any(isinstance(i, obj) for i in self.content):
            return True
        else:
            return False


def place_object(obj, x, y):
    G_STATE.level[x][y].add_object(obj)


def remove_object(obj, x, y):
    G_STATE.level[x][y].delete_object(obj)


def lower_letter(obj):
        return obj.name[:1].lower() + obj.name[1:]


class Hero:
    tile_char = '☻'

    def __init__(self, x_position, y_position, name):
        self.x_pos = x_position
        self.y_pos = y_position
        self.name = name

    def open(self, x, y):
        obj_name = G_STATE.level[x][y].name_a  # lowercase 1st letter for log
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
        if len(objects_below) > 1:                 # One object on the ground is always a hero
            INVENTORY.add_item(objects_below[-2])  # Since hero is always standing at -1 we grab -2
            obj_name = objects_below[-2].name_a
            remove_object(objects_below[-2], self.x_pos, self.y_pos)
            G_STATE.upd_chars.append((self.x_pos, self.y_pos))
            LOG.add_msg(f'You grabbed {obj_name} from {tile_name}.')
        else:
            LOG.add_msg('There are no items here.')

    def drop(self):
        key_pressed = readkey()
        try:
            if key_pressed == 'q':
                INVENTORY.drop_item(0)
            elif key_pressed == 'w':
                INVENTORY.drop_item(1)
            elif key_pressed == 'e':
                INVENTORY.drop_item(2)
            elif key_pressed == 'c':
                return False
            else:
                LOG.add_msg('Select proper item from your inventory.')
                self.drop()
        except IndexError:
            LOG.add_msg('Select proper item from your inventory.')
            self.drop()


# TODO: rework positioning in the file and remove classes from it
G_STATE = GameState()
LOG = Log(log_len=10, timestamps=False)
HERO = Hero(2, 16, 'Daniel')  # Test coordinates for 1 lvl
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
        LOG.add_msg('Select an item to drop. Press C to cancel')
        HERO.drop()
    elif key_pressed == '\x1b':
        LOG.add_msg('File closed succesfully!')
        log_file.close()
        close_terminal()
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
    now = datetime.today()
    log_file.write('-------------------------------------\n')
    log_file.write(now.strftime("Game session at %H:%M:%S on %d.%m.%Y\n"))
    # TODO: Do not use colorama, remove all calls to it
    colorama.init()
    G_STATE.load_level('levels/test_level.txt')
    #data = open('data', 'w')
    #json.dump(G_STATE.level, data)
    place_object(Key(), 2, 2)
    place_object(Diamond(), 1, 4)
    place_object(Diamond(), 1, 5)
    place_object(Diamond(), 1, 6)
    place_object(Ace(), 5, 14)
    place_object(Key(), 2, 13)
    place_object(Key(), 4, 14)
    place_object(HERO, HERO.x_pos, HERO.y_pos)
    LOG.add_msg('WASD for movement, L - look, G - grab, T - drop, ESC - exit')
    LOG.add_msg('Find a diamond!')
    LOG.add_msg('Welcome to Dark Maze!')
    hide_cursor()
    G_STATE.draw_level()
    INVENTORY.draw()
    LOG.draw()
    while True:
        input_handler()
        G_STATE.update_scr()
    LOG.add_msg('You can rest now, hero...')
    colorama.deinit()


if __name__ == '__main__':
    main()
