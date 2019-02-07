from tile_classes import TileObject
# TODO: remove copies of tile_set and import it
tile_set = {
    'floor':
        dict(name='Floor tile', standard_tile='.', custom_tile='.'),
    'wall':
        dict(name='Wall tile', standard_tile='█', custom_tile='█'),
    'stairs_down':
        dict(name='Downward Staircase Tile', standard_tile='▼', custom_tile='▼'),
    'pressure_plate':
        dict(name='Pressure Plate Tile', standard_tile='□', custom_tile='□'),
    'door_v':
        dict(name='Vertical Door Tile', standard_tile='║', custom_tile='║'),
    'door_h':
        dict(name='Horizontal Door Tile', standard_tile='═', custom_tile='═'),
    'hero':
        dict(name='The Character', standard_tile='@', custom_tile='@'),
    'key':
        dict(name='Key', standard_tile='╘', custom_tile='╘')
}

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
    tile_char = '◊'

class Ace(ItemObject):
    id = 3
    name = 'Ace of Spades'
    description = 'A worn ace of spades card. It has a ripped corner.'
    tile_char = '♠'