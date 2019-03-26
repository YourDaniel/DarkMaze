from readchar import readkey
import colorama
from colorama import Fore, Back, Style
import tile_classes
from item_classes import Key
from item_classes import Diamond
from item_classes import Ace
from gamestate import GameState


class Log:
    messages = []

    def __init__(self, log_len):
        self.log_len = log_len

    def draw(self):
        print(Fore.LIGHTBLUE_EX, end='')
        for i in range(len(self.messages)):
            msg_count = self.messages[i][1]
            msg_text = self.messages[i][0]
            if msg_count > 1:
                print(f'{msg_text} x {msg_count}')
            else:
                print(msg_text)
        print(Style.RESET_ALL)

    def add_msg(self, msg):
        if len(self.messages) > 0 and self.messages[0][0] == msg:
            self.messages[0][1] += 1
        else:
            block = [msg, 1]  # 2nd value - number of same msg
            self.messages.insert(0, block)
        if len(self.messages) > self.log_len:  # Cutting log to max size
            self.messages = self.messages[:self.log_len]
        # TODO: Rework this shit
        print('\x1b[' + str(13 + 1) + ';' + str(0 + 1) + 'H', end='')
        self.draw()


class Inventory:
    content = []

    def add_item(self, obj):
        self.content.append(obj)
        # TODO: Rework this shit
        print('\x1b[' + str(10 + 1) + ';' + str(0 + 1) + 'H', end='')
        self.draw()

    def remove_item(self, obj_id):
        for i in range(len(self.content)):
            if self.content[i].id == obj_id:
                del self.content[i]
                break

    def draw(self):
        print(Fore.LIGHTYELLOW_EX, end='')
        print('Inventory:')
        if len(self.content) == 0:
            print("Your backpack is empty")
        for i in range(len(self.content)):
            if i+1 != len(self.content):
                print(self.content[i].name, end=', ')
            else:
                print(self.content[i].name + '.')
        print('-' * 20)
        print(Style.RESET_ALL)

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
        obj_name = lower_letter(G_STATE.level[x][y])  # lowercase 1st letter for log
        if G_STATE.level[x][y].is_closed:
            if INVENTORY.item_inside(Key):
                G_STATE.upd_chars.append((x, y))
                G_STATE.upd_chars.append((self.x_pos, self.y_pos))
                G_STATE.level[x][y].open()
                INVENTORY.remove_item(Key.id)
                LOG.add_msg(f'You opened a {obj_name}.')
            else:
                LOG.add_msg(f'You need to find a key to open a {obj_name}.')
        else:
            LOG.add_msg(f"You can't open a {obj_name}.")

    def move(self, x, y):
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


# TODO: rework positioning in the file and remove classes from it
G_STATE = GameState()
LOG = Log(10)
HERO = Hero(2, 16, 'Daniel')  # Test coordinates for 1 lvl
INVENTORY = Inventory()


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
    elif key_pressed == 't':
        LOG.add_msg(f'Hero position: ({HERO.x_pos},{HERO.y_pos})')
    elif key_pressed == 'g':
        objects_below = G_STATE.level[HERO.x_pos][HERO.y_pos].objects_on
        if len(objects_below) > 1:
            INVENTORY.add_item(objects_below[-2])  # -2 to exclude hero itself because he's always standing at -1
            remove_object(objects_below[-2], HERO.x_pos, HERO.y_pos)
            G_STATE.upd_chars.append((HERO.x_pos, HERO.y_pos))
        else:
            LOG.add_msg('There are no items here.')
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
    colorama.init()
    G_STATE.load_level('test_level.txt')
    place_object(Key(), 2, 2)
    place_object(Diamond(), 1, 4)
    place_object(Ace(), 5, 14)
    place_object(Key(), 2, 13)
    place_object(Key(), 4, 14)
    place_object(HERO, HERO.x_pos, HERO.y_pos)
    LOG.add_msg('Welcome to Dark Maze!')
    LOG.add_msg('Find a diamond! ◊')
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
