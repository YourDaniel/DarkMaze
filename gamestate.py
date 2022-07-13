import tile_classes
from tileset import tile_set
from ansi_wraps import TerminalManager
from item_classes import Key, Diamond, Ace
from readchar import readkey
from log import Log


class GameState:
    def __init__(self, level_file):
        self.tm = TerminalManager()
        self.level = []
        self.load_level(level_file)
        self.log = Log(log_line=self.get_level_size()[1], timestamps=True)  # TODO: make it property
        self.upd_chars = []
        self.hero = None

    def load_level(self, file_name):
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

    def get_level_size(self):
        x = len(self.level[0])
        y = len(self.level)
        return x, y

    def draw_a_tile(self, x, y):
        self.tm.move_cursor_to(x, y)
        # if there are any elements on a tile and they're not hidden we draw them instead of an actual tile
        if len(self.level[x][y].objects_on) > 0 and not self.level[x][y].objects_hidden:
            print(self.level[x][y].objects_on[-1].tile_char, end='')
        else:
            print(self.level[x][y].tile_char, end='')

    def draw_level(self):
        self.tm.clear()
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                self.draw_a_tile(i, j)
            print()
        #self.draw_ui()

    def update_scr(self):
        for char in self.upd_chars:
            x = char[0]
            y = char[1]
            #move_cursor_to(x, y)
            with open('debug_file.txt', 'a') as f:
                f.write(f'updated char: {x} {y}\n')
            self.draw_a_tile(x, y)
        self.upd_chars = []

    def place_object(self, obj, x, y):
        self.level[x][y].add_object(obj)

    def remove_object(self, obj, x, y):
        self.level[x][y].delete_object(obj)

    @staticmethod
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

    def spawn_character(self, character):
        self.place_object(character, character.x_pos, character.y_pos)

    def test_simple_box(self, hero):
        self.hero = hero
        self.spawn_character(self.hero)
        self.place_object(Key(), 2, 3)
        self.place_object(Key(), 2, 4)
        self.place_object(Diamond(), 2, 17)
        self.place_object(Diamond(), 2, 17)
        self.place_object(Ace(), 2, 12)
        self.draw_level()

    def test_big_level_setup(self, hero):
        self.hero = hero
        self.spawn_character(self.hero)
        self.place_object(Diamond(), 2, 6)
        self.place_object(Diamond(), 2, 6)
        self.place_object(Diamond(), 2, 6)
        self.place_object(Key(), 9, 47)
        self.place_object(Key(), 9, 48)
        self.place_object(Ace(), 16, 40)
        self.place_object(Key(), 16, 40)
        self.place_object(Key(), 15, 47)
        self.place_object(Key(), 16, 53)
        self.draw_level()

    def move_hero(self, x, y):
        try:
            if self.level[x][y].can_walk_on:
                self.upd_chars.append((x, y))
                self.upd_chars.append((self.hero.x_pos, self.hero.y_pos))
                self.place_object(self.hero, x, y)
                self.remove_object(self.hero, self.hero.x_pos, self.hero.y_pos)
                self.hero.move(x, y)
                #return True
            else:
                try:
                    self.hero.open(x, y)
                except AttributeError:
                    self.log.add_msg("You can't move here.")
        except IndexError:
            self.log.add_msg("You can't move here.")

    def input_handler(self):
        key_pressed = readkey()

        # Moving
        if key_pressed == 'w':
            self.move_hero(self.hero.x_pos - 1, self.hero.y_pos)
        elif key_pressed == 'a':
            self.move_hero(self.hero.x_pos, self.hero.y_pos - 1)
        elif key_pressed == 's':
            self.move_hero(self.hero.x_pos + 1, self.hero.y_pos)
        elif key_pressed == 'd':
            self.move_hero(self.hero.x_pos, self.hero.y_pos + 1)

        # Actions
        elif key_pressed == 'g':
            self.hero.grab()
        elif key_pressed == 't':
            self.hero.drop()
        elif key_pressed == 'l':  # Look
            objects_below = self.level[self.hero.x_pos][self.hero.y_pos].objects_on
            tile_below = self.level[self.hero.x_pos][self.hero.y_pos]
            if len(objects_below) > 1:
                self.log.add_msg(f'You see {objects_below[-2].description[:1].lower()}{objects_below[-2].description[1:]}')
            else:
                self.log.add_msg(f'You see {tile_below.description[:1].lower()}{tile_below.description[1:]}')

        # Misc
        elif key_pressed == 'p':
            self.log.add_msg(f'Hero position: ({self.hero.x_pos},{self.hero.y_pos})')

        # Exit
        elif key_pressed == '\x1b':
            self.log.add_msg('Exiting the game...')
            return True

        # Loop input
        else:
            self.input_handler()

# TODO: remove local coordinates from hero
# TODO: combine items placement and loading level to one logic
