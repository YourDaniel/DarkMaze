import tile_classes
from tileset import tile_set
from ansi_wraps import TerminalManager

tm = TerminalManager()


class Level:
    map = []
    upd_chars = []

    def __init__(self):
        pass

    def load(self, file_name):
        self.map = []
        with open(file_name, encoding='UTF-8-sig') as f:
            data = f.read()
        line = []
        x = 0
        y = 0
        for char in data:
            if char != '\n':
                line.append(self.create_tile(char, x, y))
                y += 1
            else:
                self.map.append(line)
                x += 1
                y = 0
                line = []

    def get_object(self, x, y):
        return self.map[x][y]

    def get_size(self, dimension: str):
        if dimension == 'width':
            return len(self.map[0])
        elif dimension == 'height':
            return len(self.map)
        else:
            raise Exception('Dimension must be "height" or "width"')

    def draw_a_tile(self, x, y):
        tm.move_cursor_to(x, y)
        # if there are any elements on a tile and they're not hidden we draw them instead of an actual tile
        if len(self.map[x][y].objects_on) > 0 and not self.map[x][y].objects_hidden:
            print(self.map[x][y].objects_on[-1].tile_char, end='')
        else:
            print(self.map[x][y].tile_char, end='')

    def draw(self):
        tm.clear()
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.draw_a_tile(i, j)
            print()
        #self.draw_ui()

    def update_scr(self):
        for char in self.upd_chars:
            x = char[0]
            y = char[1]
            self.draw_a_tile(x, y)
        self.upd_chars = []

    def place_object(self, obj, x, y):
        self.map[x][y].add_object(obj)

    def remove_object(self, obj, x, y):
        self.map[x][y].delete_object(obj)

    def move_object(self, obj, to_x, to_y):
        self.remove_object(obj, obj.x_pos, obj.y_pos)
        self.place_object(obj, to_x, to_y)

    def get_coords(self):
        pass

    @staticmethod
    def create_tile(raw_tile, x, y):
        if raw_tile == tile_set['wall']['standard_tile']:
            return tile_classes.Wall(x, y)
        elif raw_tile == tile_set['floor']['standard_tile']:
            return tile_classes.Floor(x, y)
        elif raw_tile == tile_set['door_v']['standard_tile']:
            return tile_classes.Door(x, y, 1)
        elif raw_tile == tile_set['door_h']['standard_tile']:
            return tile_classes.Door(x, y, 0)
        elif raw_tile == tile_set['stairs_down']['standard_tile']:
            return tile_classes.StairsDown(x, y)
        elif raw_tile == tile_set['chest']['standard_tile']:
            return tile_classes.Chest(x, y)