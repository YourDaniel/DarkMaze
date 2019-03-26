import os
from colorama import Fore, Back
import tile_classes
from tileset import tile_set


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


class GameState:
    def __init__(self):
        # self.letters_picked = []
        self.level = []
        self.upd_chars = []

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

    def clear(self):
        os.system('cls')

    def get_cursor_position(self, x, y):
        return '\x1b[' + str(x + 1) + ';' + str(y + 1) + 'H'

    # TODO: rework drawing so just only changed tiles get reprinted in process
    def draw_a_tile(self, x, y):
        # if there are any elements on a tile and they're not hidden we draw them instead of an actual tile
        if len(self.level[x][y].objects_on) > 0 and not self.level[x][y].objects_hidden:
            print(self.level[x][y].objects_on[-1].tile_char, end='')
        else:
            print(self.level[x][y].tile_char, end='')

    def draw_level(self):
        self.clear()
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                self.draw_a_tile(i, j)
            print()
        # self.draw_ui()

    def update_scr(self):
        for i in range(len(self.upd_chars)):
            x = self.upd_chars[i][0]
            y = self.upd_chars[i][1]
            print(self.get_cursor_position(x, y), end='')
            self.draw_a_tile(x, y)
        print(self.get_cursor_position(23, 0), end='')
        self.upd_chars = []
