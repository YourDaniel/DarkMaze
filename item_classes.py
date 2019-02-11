# from tile_classes import TileObject
from tileset import tile_set
# TODO: implement IDs. To distiguish different items


class ItemObject:

    #def __init__(self, x_position, y_position):
    #   self.x_pos = x_position
    #    self.y_pos = y_position
    pass


class Key(ItemObject):
    id = 1
    name = 'Key'
    description = 'A small rusted key. Used for opening doors.'
    tile_char = tile_set['key']['custom_tile']

    '''def __init__(self, x, y):
        super(Key, self).__init__(x, y)'''

class Diamond(ItemObject):
    id = 2
    name = 'Diamond'
    description = 'A beautiful diamond. It shines brightly in the dark.'
    tile_char = tile_set["diamond"]["custom_tile"]

class Ace(ItemObject):
    id = 3
    name = 'Ace of Spades'
    description = 'A worn ace of spades card. It has a ripped corner.'
    tile_char = '♠'