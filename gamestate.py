from readchar import readkey

from ansi_wraps import TerminalManager
from ansi_wraps import print_colored
from items import Key, Diamond, Ace
from log import Log
from level import Level
from creature import Hero, Enemy


class GameState:
    def __init__(self, level_file):
        self.tm = TerminalManager()
        self.level = Level()
        self.level.load(level_file)
        self.log = Log(log_line=self.level.get_size('height') + 1)  # TODO: make it property
        self.hero = Hero(2, 2, 'Daniel', self.level)

    def spawn_character(self, character):
        self.level.place_object(character, character.x_pos, character.y_pos)

    def test_simple_box(self):
        self.spawn_character(self.hero)
        self.spawn_character(Enemy(4, 4, 'Enemy', self.level))
        self.level.name = 'Test level'
        for _ in range(20):
            self.level.place_object(Key(), 2, 3)
        self.level.place_object(Key(), 2, 4)
        self.level.place_object(Diamond(), 2, 17)
        self.level.place_object(Diamond(), 2, 17)
        self.level.place_object(Ace(), 2, 12)
        self.level.draw()
        self.hero.inventory.draw()
        self.draw_ui()

    def draw_ui(self):
        self.tm.move_cursor_to(self.level.get_size('height'), 0)
        print_colored('HP †: ♥♥♥', 'red', end=' ')
        print_colored('COINS: ☼☼☼', 'yellow', end=' ')
        print_colored(f'LEVEL: {self.level.name}', 'l_black')

    def input_handler(self):
        try:
            key_pressed = readkey()
        except UnicodeDecodeError:
            self.log.add_msg('Try switching to ENG layout!')
            return False

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
            self.hero.grab()
        elif key_pressed == 't':
            self.hero.drop()
        elif key_pressed == 'l':  # Look
            self.hero.look()

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

# TODO: combine items placement and loading level to one logic
