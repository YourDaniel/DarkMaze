from inventory import Inventory
from item_classes import Key
from readchar import readkey

# from log import Log
# logger = Log(11)

drop_keys = ('q', 'w', 'e', 'r', 't', 'y', 'a', 's', 'd', 'f', 'g', 'h')


class Hero:
    id = 0
    tile_char = '☻'

    def __init__(self, x_position, y_position, name, inv_col):
        self.x_pos = x_position
        self.y_pos = y_position
        self.name = name
        self.inventory = Inventory(inv_col=inv_col)

    def move(self, x, y):
        self.x_pos = x
        self.y_pos = y

    '''
    def open(self, x, y):
        obj_name = G_STATE.level[x][y].name_a
        if G_STATE.level[x][y].is_closed:
            if self.inventory.item_inside(Key):
                G_STATE.upd_chars.append((x, y))
                G_STATE.upd_chars.append((self.x_pos, self.y_pos))
                G_STATE.level[x][y].open()
                self.inventory.remove_item(Key.id)
                LOG.add_msg(f'You opened {obj_name}.')
            else:
                LOG.add_msg(f'You need to find a key to open {obj_name}.')
        else:
            LOG.add_msg(f"You can't open {obj_name}.")

    
    def grab(self):
        objects_below = G_STATE.level[self.x_pos][self.y_pos].objects_on
        tile_name = G_STATE.level[self.x_pos][self.y_pos].name_a
        for i in range(len(objects_below)-1, -1, -1):
            # Check if picked item is not a Hero since he has id = 0
            # TODO: Fix this dirty hack
            if objects_below[i].id != 0:
                self.inventory.add_item(objects_below[i])
                obj_name = objects_below[i].name_a
                remove_object(objects_below[i], self.x_pos, self.y_pos)
                G_STATE.upd_chars.append((self.x_pos, self.y_pos))
                LOG.add_msg(f'You grabbed {obj_name} from {tile_name}.')
                break
        else:
            LOG.add_msg('There are no items here.')

    def drop(self):
        if len(self.inventory.content) == 0:
            LOG.add_msg('You have no items in your backpack.')
            return False
        LOG.add_msg('Select an item to drop. Press C to cancel')
        while True:
            key_pressed = readkey()
            for i, key in enumerate(drop_keys):
                if key_pressed == key:
                    place_object(self.inventory.content[i], self.x_pos, self.y_pos)
                    LOG.add_msg(f'You dropped {self.inventory.content[i].name_a}.')
                    del self.inventory.content[i]
                    self.inventory.draw()
                    return True
                elif key_pressed == 'c':
                    LOG.add_msg('You changed your mind on dropping something.')
                    return False
                else:
                    LOG.add_msg('Select a proper item in your backpack.')
                    break
    '''

# TODO: make log work from several instances (bug: new message continues count)
# TODO: initialize Hero from Gamestate
