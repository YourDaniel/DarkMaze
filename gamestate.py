from readchar import readkey

from ansi_wraps import TerminalManager
from items import Key, Diamond, Ace
from log import Log
from level import Level
from creature import Hero, NPC


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
        self.spawn_character(NPC(4, 4, 'Enemy', self.level))
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
        self.tm.print_colored('HP †: ♥♥♥', 'red', end=' ')
        self.tm.print_colored('COINS: ☼☼☼', 'yellow', end=' ')
        self.tm.print_colored(f'LEVEL: {self.level.name}', 'l_black')

    def input_handler(self):
        try:
            key_pressed = readkey()
        except UnicodeDecodeError:
            self.log.add_msg('Try switching to ENG layout!')
            return False

        match key_pressed:
            # Moving
            case 'w':
                self.hero.move(self.hero.x_pos - 1, self.hero.y_pos)
            case 'a':
                self.hero.move(self.hero.x_pos, self.hero.y_pos - 1)
            case 's':
                self.hero.move(self.hero.x_pos + 1, self.hero.y_pos)
            case 'd':
                self.hero.move(self.hero.x_pos, self.hero.y_pos + 1)
            # Actions
            case 'g':
                self.hero.grab()
            case 'p':
                self.hero.drop()
            case 'l':
                self.hero.look()
            case 'c':
                self.hero.close()
            # Misc
            case 'z':
                self.log.add_msg(f'Hero position: ({self.hero.x_pos},{self.hero.y_pos})')
            # Exit
            case '\x1b':
                self.log.add_msg('Exiting the game...')
                return True
            # Loop input
            case _:
                self.input_handler()


# TODO: combine items placement and loading level to one logic
