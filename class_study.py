
class TileObject:
    def __init__(self, x_position, y_position):
        self.x_pos = x_position
        self.y_pos = y_position
        self.items_on = []


class Wall(TileObject):
    name = 'Wall'

    def __init__(self, x, y):
        self.destroyable = True
        self.can_walk_on = True
        self.obtainable = False
        super(Wall, self).__init__(x, y)


class Floor(TileObject):
    name = 'Floor'

    def __init__(self, x, y):
        self.destroyable = False
        self.can_walk_on = False
        self.obtainable = False
        super(Floor, self).__init__(x, y)


tiles = []
tiles.append(Floor(0, 1))
tiles.append(Wall(1, 1))
for tile in tiles:
    print(tile.name)
    print(tile.destroyable)
