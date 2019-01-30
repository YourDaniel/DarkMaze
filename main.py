import os
from readchar import readkey


class GameState:
    def __init__(self):
        self.keys = 0
        self.letters_picked = []
        self.level = []

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
                line = []

    def create_tile(self, raw_tile, x, y):
        if raw_tile == tile_set['wall']['standard_tile']:
            return TileObject('Wall', tile_set['wall']['custom_tile'], x, y, True, True, False)
        elif raw_tile == tile_set['floor']['standard_tile']:
            return TileObject('Floor', tile_set['floor']['custom_tile'], x, y, False, False, False)
        elif raw_tile == tile_set['door_v']['standard_tile']:
            return TileObject('Vertical Door', tile_set['door_v']['custom_tile'], x, y, True, True, True) #TODO: rework picking up
        elif raw_tile == tile_set['hero']['standard_tile']:
            return TileObject('Hero', tile_set['hero']['custom_tile'], x, y, True, True, False)
        elif raw_tile == tile_set['stairs_down']['standard_tile']:
            return TileObject('Downward Staircase', tile_set['stairs_down']['custom_tile'], x, y, True, True, False)

    def test_load_level(self, file_name):
        self.level = []
        with open(file_name, encoding='UTF-8-sig') as f:
            data = f.read()
        line = []
        x = 0
        y = 0
        for char in data:
            if char != '\n':
                line.append(self.create_tile(char, x, y))
                y += 1
            else:
                self.level.append(line)
                x += 1
                y = 0
                line = []


class TileObject:
    def __init__(self, name, tile_char, x_position, y_position, destroyable, solid, can_be_picked):
        self.name = name
        self.tile_char = tile_char
        self.x_position = x_position
        self.y_position = y_position
        self.destroyable = destroyable
        self.solid = solid
        self.can_be_picked = can_be_picked
        self.bottom_tile = tile_set['wall']['custom_tile']

    def destroy(self):
        pass
        # create_floor(self.x_position, self.y_position)


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
    'hero':
        dict(name='The Character', standard_tile='@', custom_tile='@'),
    'key':
        dict(name='Key', standard_tile='╘', custom_tile='╘')
}

levels = (1, 2, 3) # sets the order of levels
game_state = GameState()
floor_tile = '.'
wall_tile = '█'
stairs_down = '▼'
pressure_plate = '□'
door_v = '║'
hero = '@'
key = '╘'
level_passed = False


def clear():
    os.system('cls')


def test_draw_level():
    clear()
    for i in range(len(game_state.level)):
        for j in range(len(game_state.level[i])):
            print(game_state.level[i][j].tile_char, end='')
        print()
    print(f'Keys: {game_state.keys}')

def draw_level():
    clear()
    for i in range(len(game_state.level)):
        for j in range(len(game_state.level[i])):
            print(game_state.level[i][j], end='')
        print()
    print(f'Keys: {game_state.keys}')


def place_hero(x, y):
    game_state.level[x][y] = hero
    pos = (x, y)
    return pos


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


def input_handler(pos):
    key_pressed = readkey()
    if key_pressed == 'w':
        pos = move(pos[0] - 1, pos[1], pos)
    elif key_pressed == 'a':
        pos = move(pos[0], pos[1] - 1, pos)
    elif key_pressed == 's':
        pos = move(pos[0] + 1, pos[1], pos)
    elif key_pressed == 'd':
        pos = move(pos[0], pos[1] + 1, pos)
    return pos


def main():
    game_state.test_load_level('level_1.txt')
    test_draw_level()
    a = input('Press Exit...')


    for current_level in levels:
        game_state.load_level(f'level_{str(current_level)}.txt')
        hero_pos = find_hero()
        draw_level()
        print('Find a way downstairs! ▼')
        global level_passed
        while not level_passed:
            hero_pos = input_handler(hero_pos)
        level_passed = False
    print('You can rest now, hero...')


if __name__ == '__main__':
    main()
