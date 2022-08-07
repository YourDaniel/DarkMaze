import tiles
from tileset import tile_set
from terminal_manager import TerminalManager


tm = TerminalManager()


class Level:
    map = []
    upd_chars = []

    def __init__(self):
        self.name = ''

    def load(self, file_name, name):
        self.name = name
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

    def get_tile(self, x, y):
        return self.map[x][y]

    def get_objects(self):
        objects = []
        for x in range(self.get_size('height')):
            for y in range(self.get_size('width')):
                objects.append(self.get_tile(x, y).objects_on)
        return [obj for sublist in objects for obj in sublist]

    def get_size(self, dimension: str):
        match dimension:
            case 'width':
                lengths = [len(line) for line in self.map]
                return max(lengths)
            case 'height':
                return len(self.map)
            case _:
                raise Exception('Dimension must be "height" or "width"')

    def draw_a_tile(self, x, y):
        tm.move_cursor_to(x, y)
        # if there are any elements on a tile, and they're not hidden we draw them instead of an actual tile
        if len(self.map[x][y].objects_on) > 0 and not self.map[x][y].objects_hidden:
            obj_to_draw = self.map[x][y].objects_on[-1]
        else:
            obj_to_draw = self.map[x][y]
        # Draw background
        if hasattr(obj_to_draw, 'color_back'):
            tm.set_background(obj_to_draw.color_back)

        if isinstance(obj_to_draw.color, list):
            tm.print_colored(obj_to_draw.tile_char, obj_to_draw.color[0])
        else:
            tm.print_colored(obj_to_draw.tile_char, obj_to_draw.color)

    def draw(self):
        tm.clear()
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.draw_a_tile(i, j)
            print(flush=True)

    def blink(self):
        blinks = [obj for obj in self.get_objects() if isinstance(obj.color, list)]
        self.upd_chars.append([(obj.x, obj.y) for obj in blinks])

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

    def check_for_move(self, x, y):
        tile = self.map[x][y]
        if not tile.can_walk_on:
            return False
        for item in tile.objects_on:
            try:
                if not item.can_walk_on:
                    return False
            except AttributeError as e:
                raise Exception(f'No attribute can_walk_on for {item}: {e}')
        return True

    @staticmethod
    def create_tile(raw_tile, x, y):
        if raw_tile == tile_set['wall']['standard_tile']:
            return tiles.Wall(x, y)
        elif raw_tile == tile_set['floor']['standard_tile']:
            return tiles.Floor(x, y)
        elif raw_tile == tile_set['door_v']['standard_tile']:
            return tiles.Door(x, y, 1)
        elif raw_tile == tile_set['door_h']['standard_tile']:
            return tiles.Door(x, y, 0)
        elif raw_tile == tile_set['stairs_down']['standard_tile']:
            return tiles.StairsDown(x, y)
        elif raw_tile == tile_set['chest']['standard_tile']:
            return tiles.Chest(x, y)
        else:
            # Make a floor tile if a tile was not found
            return tiles.Floor(x, y)
