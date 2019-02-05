import os
from readchar import readkey
import tile_classes
import item_classes
# from tile_classes import TileObject
from item_classes import Key

tile_set = {
    'floor':
        dict(name='Floor tile', standard_tile='.', custom_tile='.'),
    'wall':
        dict(name='Wall tile', standard_tile='█', custom_tile='█'),
    'stairs_down':
        dict(name='Downward Staircase Tile', standard_tile='▼', custom_tile='▼'),
    'pressure_plate':
        dict(name='Pressure Plate Tile', standard_tile='□', custom_tile='□'),
    'door_v':
        dict(name='Vertical Door Tile', standard_tile='║', custom_tile='║'),
    'door_h':
        dict(name='Horizontal Door Tile', standard_tile='═', custom_tile='═'),
    'hero':
        dict(name='The Character', standard_tile='@', custom_tile='@'),
    'key':
        dict(name='Key', standard_tile='╘', custom_tile='╘')
}


def clear():
    os.system('cls')


class Log:
    messages = []

    def __init__(self, log_len):
        self.log_len = log_len

    def draw(self):
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

    def draw(self):
        print('Inventory:')
        if len(self.content) == 0:
            print("Your backpack is empty")
        for i in range(len(self.content)):
            if i+1 != len(self.content):
                print(self.content[i].name, end=', ')
            else:
                print(self.content[i].name + '.')


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


class Hero:
    tile_char = '☻'

    def __init__(self, x_position, y_position, name):
        self.x_pos = x_position
        self.y_pos = y_position
        self.name = name

    def move(self, x, y):
        if game_state.level[x][y].can_walk_on:
            place_object(self, x, y)
            remove_object(self, self.x_pos, self.y_pos)
            self.x_pos = x
            self.y_pos = y
        else:
            log.add_msg("Can't move here!")


class GameState:
    def __init__(self):
        self.letters_picked = []
        self.level = []
    '''
    def load_level(self, file_name):
        self.level = []
        with open(file_name, encoding='UTF-8-sig') as f:
            data = f.read()
        line = []
        for char in data:
            if char != '\n':
                line.append(char)
            else:
                self.level.append(line)
                line = []'''

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


game_state = GameState()
log = Log(10)
hero = Hero(2, 16, 'Daniel')  # Test coordinates for 1 lvl
inv = Inventory()
'''
def find_hero():
    for i in range(len(game_state.level)):
        for j in range(len(game_state.level[i])):
            if game_state.level[i][j] == hero:
                pos = (i, j)
                return pos
    else:
        print('Hero is not found on level!')
def move(x, y, old_pos):
    def wall_collision(x, y):
        if game_state.level[x][y] == wall_tile:
            return True
        elif game_state.level[x][y] == door_v:
            if game_state.keys < 1:
                return True
            else:
                game_state.keys -= 1
                return False
        else:
            return False
    if not wall_collision(x, y):
        if game_state.level[x][y] == stairs_down:
            global level_passed
            level_passed = True
        if game_state.level[x][y] == pressure_plate:
            #TODO: Redo this hardcode
            game_state.level[2][4] = floor_tile
        if game_state.level[x][y] == key:
            game_state.keys += 1
        game_state.level[old_pos[0]][old_pos[1]] = floor_tile
        new_pos = place_hero(x, y)
        draw_level()
        return new_pos
    else:
        print("Can't move here")
        return old_pos
'''


def draw_level():
    clear()
    lvl = game_state.level
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            # if there are any elements on a tile we draw them instead of an actual tile
            if len(lvl[i][j].objects_on) > 0:
                print(lvl[i][j].objects_on[-1].tile_char, end='')
            else:
                print(lvl[i][j].tile_char, end='')
        print()
    inv.draw()
    print('-'*20)
    log.draw()


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
            inv.add_item(objects_below[-2])  # -2 to exclude hero itself
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
    game_state.load_level('test_level.txt')
    place_object(Key(), 3, 10)
    place_object(Key(), 3, 13)
    place_object(hero, hero.x_pos, hero.y_pos)
    log.add_msg('Welcome to Dark Maze!')
    log.add_msg('Find a way downstairs! ▼')
    while True:
        draw_level()
        input_handler()
    log.add_msg('You can rest now, hero...')


if __name__ == '__main__':
    main()
