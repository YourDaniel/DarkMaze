import os
from readchar import readkey
import tile_classes
from item_classes import Key
from item_classes import Diamond
from item_classes import Ace
from colorama import init
from colorama import deinit
from colorama import Fore, Back, Style
from tileset import tile_set


def clear():
    os.system('cls')

def set_color():
    os.system('color f4')


class Log:
    messages = []

    def __init__(self, log_len):
        self.log_len = log_len

    def draw(self):
        # TODO: Add fading color to messages
        for i in range(len(self.messages)):
            msg_count = self.messages[i][1]
            msg_text = self.messages[i][0]
            if msg_count > 1:
                print(f'{msg_text} x {msg_count}')
            else:
                print(msg_text)

    def add_msg(self, msg):
        if len(self.messages) > 0:
            if self.messages[0][0] == msg:
                self.messages[0][1] += 1
            else:
                block = [msg, 1]  # 2nd value - number of same msg
                self.messages.insert(0, block)
        else:
            block = [msg, 1]
            self.messages.insert(0, block)
        if len(self.messages) > self.log_len:  # Cutting log to max size
            self.messages = self.messages[:self.log_len]


class Inventory:
    content = []

    def add_item(self, obj):
        self.content.append(obj)

    def remove_item(self, obj_id):
        for i in range(len(self.content)):
            if self.content[i].id == obj_id:
                del self.content[i]
                break

    def draw(self):
        print('Inventory:')
        if len(self.content) == 0:
            print("Your backpack is empty")
        for i in range(len(self.content)):
            if i+1 != len(self.content):
                print(self.content[i].name, end=', ')
            else:
                print(self.content[i].name + '.')

    def item_inside(self, obj):
        if any(isinstance(i, obj) for i in self.content):
            return True
        else:
            return False


def place_object(obj, x, y):
    game_state.level[x][y].add_object(obj)


def remove_object(obj, x, y):
    game_state.level[x][y].delete_object(obj)


def create_tile(raw_tile, x, y):
    if raw_tile == tile_set['wall']['standard_tile']:
        return tile_classes.Wall(x, y)
    elif raw_tile == tile_set['floor']['standard_tile']:
        return tile_classes.Floor(x, y)
    elif raw_tile == tile_set['door_v']['standard_tile']:
        return tile_classes.Door(x, y, 1)
    elif raw_tile == tile_set['door_h']['standard_tile']:
        return tile_classes.Door(x, y, 0)
    elif raw_tile == tile_set['stairs_down']['standard_tile']:
        return tile_classes.StairsDown(x, y)
    elif raw_tile == tile_set['chest']['standard_tile']:
        return tile_classes.Chest(x, y)


class Hero:
    tile_char = '☻'

    def __init__(self, x_position, y_position, name):
        self.x_pos = x_position
        self.y_pos = y_position
        self.name = name

    def open(self, x, y):
        if game_state.level[x][y].is_closed:
            if inv.item_inside(Key):
                game_state.level[x][y].open()
                inv.remove_item(Key.id)
                # TODO: rework this naming problem
                log.add_msg(f'You opened a {game_state.level[x][y].name[:1].lower()}{game_state.level[x][y].name[1:]}.')
            else:
                log.add_msg(f'You need to find a key to open a {game_state.level[x][y].name[:1].lower()}{game_state.level[x][y].name[1:]}.')
        else:
            log.add_msg("You can't move here.")

    def move(self, x, y):
        if game_state.level[x][y].can_walk_on:
            place_object(self, x, y)
            remove_object(self, self.x_pos, self.y_pos)
            self.x_pos = x
            self.y_pos = y
            return True
        else:
            try:
                self.open(x, y)
            except AttributeError:
                log.add_msg("You can't move here.")


class GameState:
    def __init__(self):
        self.letters_picked = []
        self.level = []

    def load_level(self, file_name):
        self.level = []
        with open(file_name, encoding='UTF-8-sig') as f:
            data = f.read()
        line = []
        x = 0
        y = 0
        for char in data:
            if char != '\n':
                line.append(create_tile(char, x, y))
                y += 1
            else:
                self.level.append(line)
                x += 1
                y = 0
                line = []


# TODO: rework positioning in the file and remove classes from it
game_state = GameState()
log = Log(10)
hero = Hero(2, 16, 'Daniel')  # Test coordinates for 1 lvl
inv = Inventory()


# TODO: rework drawing so just only changed tiles get reprinted in process
def draw_level():
    clear()
    lvl = game_state.level
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            # if there are any elements on a tile and they're not hidden we draw them instead of an actual tile
            if len(lvl[i][j].objects_on) > 0 and not lvl[i][j].objects_hidden:
                    print(lvl[i][j].objects_on[-1].tile_char, end='')
            else:
                if lvl[i][j].tile_char == '.':
                    print(Fore.BLUE, end='')
                if lvl[i][j].tile_char == '█':
                    print(Fore.LIGHTBLUE_EX, end='')
                print(lvl[i][j].tile_char, end='')
                #print(Style.RESET_ALL, end='')
        print()
    draw_ui()


def draw_ui():
    print(Fore.LIGHTYELLOW_EX, end='')
    print(Style.DIM, end='')
    inv.draw()
    print('-' * 20)
    print(Fore.LIGHTBLUE_EX, end='')
    print(Style.BRIGHT, end='')
    log.draw()
    print(Style.RESET_ALL)



def input_handler():
    key_pressed = readkey()
    if key_pressed == 'w':
        hero.move(hero.x_pos - 1, hero.y_pos)
    elif key_pressed == 'a':
        hero.move(hero.x_pos, hero.y_pos - 1)
    elif key_pressed == 's':
        hero.move(hero.x_pos + 1, hero.y_pos)
    elif key_pressed == 'd':
        hero.move(hero.x_pos, hero.y_pos + 1)
    elif key_pressed == 't':
        log.add_msg(f'Hero position: ({hero.x_pos},{hero.y_pos})')
    elif key_pressed == 'g':
        objects_below = game_state.level[hero.x_pos][hero.y_pos].objects_on
        if len(objects_below) > 1:
            inv.add_item(objects_below[-2])  # -2 to exclude hero itself because he's always standing at -1
            remove_object(objects_below[-2], hero.x_pos, hero.y_pos)
        else:
            log.add_msg('There are no items here.')
    elif key_pressed == 'l':  # Look
        objects_below = game_state.level[hero.x_pos][hero.y_pos].objects_on
        tile_below = game_state.level[hero.x_pos][hero.y_pos]
        if len(objects_below) > 1:
            log.add_msg(f'You see {objects_below[-2].description[:1].lower()}{objects_below[-2].description[1:]}')
        else:
            log.add_msg(f'You see {tile_below.description[:1].lower()}{tile_below.description[1:]}')
    else:
        input_handler()


def main():
    init()
    game_state.load_level('test_level.txt')
    place_object(Key(), 2, 2)
    place_object(Diamond(), 1, 4)
    place_object(Ace(), 5, 14)
    place_object(Key(), 2, 13)
    place_object(Key(), 4, 14)
    place_object(hero, hero.x_pos, hero.y_pos)
    log.add_msg('Welcome to Dark Maze!')
    log.add_msg('Find a diamond! ◊')
    while True:
        draw_level()
        input_handler()
    log.add_msg('You can rest now, hero...')
    deinit()


if __name__ == '__main__':
    main()
