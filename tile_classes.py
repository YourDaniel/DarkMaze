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

# TODO: Add tiles variety
class TileObject:
    def __init__(self, x_position, y_position):
        self.objects_hidden = False
        self.x_pos = x_position
        self.y_pos = y_position
        self.objects_on = []

    def add_object(self, item_object):
        self.objects_on.append(item_object)

    def delete_object(self, item_object):
        self.objects_on.remove(item_object)


class Wall(TileObject):
    name = 'Wall'
    tile_char = tile_set['wall']['custom_tile']
    bottom_tile_char = tile_set['floor']['custom_tile']

    def __init__(self, x, y):
        self.destroyable = True
        self.can_walk_on = False
        self.obtainable = False
        self.description = 'A rough stone wall. It is dark and cold.'
        super(Wall, self).__init__(x, y)


class Floor(TileObject):
    name = 'Floor'
    tile_char = tile_set['floor']['custom_tile']
    bottom_tile_char = tile_set['floor']['custom_tile']

    def __init__(self, x, y):
        self.destroyable = False
        self.can_walk_on = True
        self.obtainable = False
        self.description = 'a rough stone floor. It is dark and cold.'
        super(Floor, self).__init__(x, y)


class Door(TileObject):
    name = 'Door'
    bottom_tile_char = "'"

    def __init__(self, x, y, align):
        # TODO: Rework aligning. Automatically choose tile or use the same tile for all doors?
        if align == 0:  # horizontal
            self.tile_char = tile_set['door_h']['custom_tile']
        else:  # vertical
            self.tile_char = tile_set['door_v']['custom_tile']
        self.closed_tile_char = self.tile_char
        self.is_closed = True
        self.destroyable = True
        self.can_walk_on = False
        self.obtainable = False
        self.description = 'an old wooden door with rusty handle and a keyhole.'
        super(Door, self).__init__(x, y)

    def open(self):
        self.is_closed = False
        self.can_walk_on = True
        self.tile_char = self.bottom_tile_char

    def close(self):
        self.is_closed = True
        self.can_walk_on = False
        self.tile_char = self.closed_tile_char


class StairsDown(TileObject):
    name = 'Downward Staircase'
    tile_char = tile_set['stairs_down']['custom_tile']
    bottom_tile_char = tile_set['floor']['custom_tile']

    def __init__(self, x, y):
        self.destroyable = False
        self.can_walk_on = True
        self.obtainable = False
        self.description = 'Steps leading down to the darkness. You feel a cold air blowing from there.'
        super(StairsDown, self).__init__(x, y)


class Chest(TileObject):
    name = 'Chest'
    tile_char = '■'
    bottom_tile_char = '∟'

    def __init__(self, x, y):
        self.destroyable = True
        self.can_walk_on = False
        self.obtainable = False
        self.is_closed = True
        self.description = 'a crude chest with iron frame. It has a keyhole.'
        self.closed_tile_char = self.tile_char
        super(Chest, self).__init__(x, y)
        self.objects_hidden = True

    def open(self):
        self.is_closed = False
        self.can_walk_on = True
        self.tile_char = self.bottom_tile_char
        self.objects_hidden = False

    def close(self):
        self.is_closed = True
        self.can_walk_on = False
        self.tile_char = self.closed_tile_char
        self.objects_hidden = True

