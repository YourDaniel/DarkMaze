from readchar import readkey

from ansi_wraps import TerminalManager
from level import Level
from log import Log
from turns import TurnManager
from items import Key, Diamond, Ace
from creature import Hero, Zombie


class GameState:
    def __init__(self, level_file):
        self.tm = TerminalManager()
        self.level = Level()
        self.level.load(level_file, 'Test level')
        self.log = Log(log_line=self.level.get_size('height') + 1)  # TODO: make it property
        self.turn = TurnManager(self.level)
        self.hero = Hero('Daniel', 2, 2, self.level)

    def spawn_character(self, character):
        self.level.place_object(character, character.x_pos, character.y_pos)

    def test_simple_box(self):
        self.spawn_character(self.hero)
        self.spawn_character(Zombie('Enemy', 1, 10, self.level))
        self.spawn_character(Zombie('Enemy', 2, 11, self.level))
        self.spawn_character(Zombie('Enemy', 1, 12, self.level))
        self.spawn_character(Zombie('Enemy', 2, 13, self.level))
        self.spawn_character(Zombie('Enemy', 1, 14, self.level))
        self.spawn_character(Zombie('Enemy', 2, 15, self.level))
        self.spawn_character(Zombie('Enemy', 1, 16, self.level))
        # for _ in range(10):
        #     self.level.place_object(Key(), 2, 3)
        self.level.place_object(Key(), 2, 4)
        self.level.place_object(Key(), 8, 6)
        self.level.place_object(Key(), 9, 5)
        self.level.place_object(Diamond(), 2, 17)
        self.level.place_object(Diamond(), 2, 17)
        # self.level.place_object(Ace(), 2, 12)
        self.level.draw()
        self.hero.inventory.draw()
        self.log.draw()
        self.draw_ui()

    def draw_ui(self):
        self.tm.move_cursor_to(self.level.get_size('height'), 0)
        self.tm.print_colored(f'HP: {self.hero.hp}/{self.hero.max_hp}', 'red', end=' ')
        self.tm.print_colored('COINS: ☼☼☼', 'yellow', end=' ')
        self.tm.print_colored(f'LEVEL: {self.level.name}', 'l_black')

    def show_controls(self):
        self.log.add_msg('Misc: ESC - exit, (q) - show controls')
        self.log.add_msg('Actions: (l)ook, (g)rab, dro(p), (c)lose, (o)pen')
        self.log.add_msg('Movement: (w)(a)(s)(d)')
        self.log.add_msg('-- Controls --')

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
                direction = self.hero.choose_direction('close')
                if direction:
                    self.hero.close(*direction)
            case 'o':
                direction = self.hero.choose_direction('open')
                if direction:
                    self.hero.open(*direction)
            # Misc
            case 'z':
                self.log.add_msg(f'Hero position: ({self.hero.x_pos},{self.hero.y_pos})')
            case 'q':
                self.show_controls()
            # Exit
            case '\x1b':
                self.log.add_msg('Exiting the game...')
                return True
            # Loop input
            case _:
                self.input_handler()


# TODO: combine items placement and loading level to one logic
