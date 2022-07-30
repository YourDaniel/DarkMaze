from abc import ABC, abstractmethod
import random

from inventory import Inventory, InventoryIsFullException
from items import Key
from log import Log
from readchar import readkey
from globals import DROP_KEYS
from debug_log import debug
from utils import lower_first_letter


LOG = Log(log_line=12)
# TODO: make base class for items, creatures and tiles
# TODO: move hero functions to base creature class


class Creature(ABC):
    def __init__(self, name, x_pos, y_pos, level):
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.level = level
        self.can_walk_on = False
        self.is_actor = True
        self.color = 'white'
        self.name_a = 'a creature'

    def move(self, x, y):
        try:
            if self.level.check_for_move(x, y):
                self.level.upd_chars.append((x, y))
                self.level.upd_chars.append((self.x_pos, self.y_pos))
                self.level.move_object(self, x, y)
                self.x_pos = x
                self.y_pos = y
        except IndexError:
            pass


class NPC(Creature):
    def __init__(self, x_position, y_position, name, level):
        super().__init__(name, x_position, y_position, level)
        self.inventory = Inventory(inv_col=self.level.get_size('width') + 1, height=self.level.get_size('height'))
        self.tile_char = 'z'
        self.id = 4
        self.name_a = 'a zombie'
        self.color = 'l_green'

    def choose_action(self):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        return self.move, (self.x_pos + x, self.y_pos + y)


class Hero(Creature):
    id = 0
    tile_char = '☻'

    def __init__(self, x_position, y_position, name, level):
        super().__init__(name, x_position, y_position, level)
        self.is_actor = False
        self.inventory = Inventory(
            inv_col=self.level.get_size('width') + 1,
            height=self.level.get_size('height'),
            visible=True)

    def move(self, x, y):
        try:
            if self.level.check_for_move(x, y):
                self.level.upd_chars.append((x, y))
                self.level.upd_chars.append((self.x_pos, self.y_pos))
                self.level.move_object(self, x, y)
                self.x_pos = x
                self.y_pos = y
            else:
                try:
                    self.open(x, y)
                except AttributeError:
                    LOG.add_msg("You can't move here.")
        except IndexError:
            LOG.add_msg("You can't move here.")

    def open(self, x, y):
        obj_to_open = self.level.get_object(x, y)

        if not hasattr(obj_to_open, 'is_closed'):
            LOG.add_msg(f"You can't open {obj_to_open.name_a}.")
            return False

        if not obj_to_open.is_closed:
            LOG.add_msg(f'{obj_to_open.name} is already open.')
            return False

        self.level.upd_chars.append((x, y))
        self.level.upd_chars.append((self.x_pos, self.y_pos))

        if obj_to_open.requires_key:
            if self.inventory.item_inside(Key):
                self.inventory.remove_item(Key.id)
                obj_to_open.open()
                LOG.add_msg(f'You opened {obj_to_open.name_a}.')
                return True
            else:
                LOG.add_msg(f'You need to find a key to open {obj_to_open.name_a}.')
                return False
        else:
            obj_to_open.open()
            LOG.add_msg(f'You opened {obj_to_open.name_a}.')
            return True

    def choose_direction(self, action_verb: str):
        LOG.add_msg(f'Where to {action_verb}? ')
        key_pressed = readkey()
        while True:
            match key_pressed:
                case 'w':
                    x, y = self.x_pos - 1, self.y_pos
                    return x, y
                case 'a':
                    x, y = self.x_pos, self.y_pos - 1
                    return x, y
                case 's':
                    x, y = self.x_pos + 1, self.y_pos
                    return x, y
                case 'd':
                    x, y = self.x_pos, self.y_pos + 1
                    return x, y
                case 'c':
                    LOG.add_msg('You changed your mind.')
                    return None
                case _:
                    LOG.add_msg(f'Use WASD keys to choose a direction to {action_verb}. Press C to cancel.')

    def close(self, x, y):
        self.level.upd_chars.append((x, y))
        obj_to_close = self.level.get_object(x, y)
        if hasattr(obj_to_close, 'is_closed'):
            if not obj_to_close.is_closed:
                obj_to_close.close()
                LOG.add_msg(f'You closed {obj_to_close.name_a}.')
            else:
                LOG.add_msg(f'{obj_to_close.name} is already closed.')
        else:
            LOG.add_msg('Nothing to close here.')

    def grab(self):
        objects_below = self.level.get_object(self.x_pos, self.y_pos).objects_on
        tile_name = self.level.get_object(self.x_pos, self.y_pos).name_a
        for i in range(len(objects_below)-1, -1, -1):
            # Check if picked item is not a Hero since he has id = 0
            # TODO: Fix this dirty hack
            if objects_below[i].id != 0:
                try:
                    self.inventory.add_item(objects_below[i])
                except InventoryIsFullException:
                    LOG.add_msg("Can't take any more items. Inventory is full.")
                    return False
                obj_name = objects_below[i].name_a
                self.level.remove_object(objects_below[i], self.x_pos, self.y_pos)
                self.level.upd_chars.append((self.x_pos, self.y_pos))
                LOG.add_msg(f'You grabbed {obj_name} from {tile_name}.')
                return True
        else:
            LOG.add_msg('There are no items here.')

    def drop(self):
        if len(self.inventory.content) == 0:
            LOG.add_msg('You have no items in your backpack.')
            return False
        LOG.add_msg('Select an item to drop. Press C to cancel.')
        while True:
            try:
                key_pressed = readkey()
                if key_pressed == 'c':
                    LOG.add_msg('You changed your mind on dropping something.')
                    return False
                if key_pressed not in DROP_KEYS:
                    LOG.add_msg('Select a proper item in your backpack.')
                else:
                    item_index = DROP_KEYS.index(key_pressed)
                    if item_index >= len(self.inventory.content):
                        LOG.add_msg('Select a proper item in your backpack.')
                    else:
                        self.level.place_object(self.inventory.content[item_index], self.x_pos, self.y_pos)
                        LOG.add_msg(f'You dropped {self.inventory.content[item_index].name_a}.')
                        del self.inventory.content[item_index]
                        self.inventory.draw()
                        return True
            except UnicodeDecodeError:
                LOG.add_msg('Try switching to ENG layout')

    def look(self):
        objects_below = [obj for obj in self.level.get_object(self.x_pos, self.y_pos).objects_on if obj != self]
        if len(objects_below) > 0:
            top_object = objects_below[-1]
            LOG.add_msg(f'You see {lower_first_letter(top_object.description)}')
        else:
            tile_below = self.level.get_object(self.x_pos, self.y_pos)
            LOG.add_msg(f'You see {lower_first_letter(tile_below.description)}')
