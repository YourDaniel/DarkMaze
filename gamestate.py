from ansi_wraps import TerminalManager
from item_classes import Key, Diamond, Ace
from readchar import readkey
from log import Log
from level import Level
from creature import Hero


class GameState:
    def __init__(self, level_file):
        self.tm = TerminalManager()
        self.level = Level()
        self.level.load(level_file)
        self.log = Log(log_line=self.level.get_size('height'))  # TODO: make it property
        self.hero = Hero(2, 2, 'Daniel', self.level.get_size('width') + 1, self.level, self.log)

    def spawn_character(self, character):
        self.level.place_object(character, character.x_pos, character.y_pos)

    def test_simple_box(self):
        self.spawn_character(self.hero)
        self.level.place_object(Key(), 2, 3)
        self.level.place_object(Key(), 2, 4)
        self.level.place_object(Diamond(), 2, 17)
        self.level.place_object(Diamond(), 2, 17)
        self.level.place_object(Ace(), 2, 12)
        self.level.draw()
        self.hero.inventory.draw()

    def grab(self):
        objects_below = self.level.get_object(self.hero.x_pos, self.hero.y_pos).objects_on
        tile_name = self.level.get_object(self.hero.x_pos, self.hero.y_pos).name_a
        for i in range(len(objects_below)-1, -1, -1):
            # Check if picked item is not a Hero since he has id = 0
            # TODO: Fix this dirty hack
            if objects_below[i].id != 0:
                self.hero.inventory.add_item(objects_below[i])
                obj_name = objects_below[i].name_a
                self.level.remove_object(objects_below[i], self.hero.x_pos, self.hero.y_pos)
                self.level.upd_chars.append((self.hero.x_pos, self.hero.y_pos))
                self.log.add_msg(f'You grabbed {obj_name} from {tile_name}.')
                break
        else:
            self.log.add_msg('There are no items here.')

    def input_handler(self):
        key_pressed = readkey()

        # Moving
        if key_pressed == 'w':
            self.hero.move(self.hero.x_pos - 1, self.hero.y_pos)
        elif key_pressed == 'a':
            self.hero.move(self.hero.x_pos, self.hero.y_pos - 1)
        elif key_pressed == 's':
            self.hero.move(self.hero.x_pos + 1, self.hero.y_pos)
        elif key_pressed == 'd':
            self.hero.move(self.hero.x_pos, self.hero.y_pos + 1)

        # Actions
        elif key_pressed == 'g':
            self.grab()
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
