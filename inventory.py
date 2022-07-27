import functools

from ansi_wraps import Color
from ansi_wraps import TerminalManager
from globals import DROP_KEYS

print = functools.partial(print, flush=True)
tm = TerminalManager()


class Inventory:
    content = []
    inv_line = 0  # Inventory starts from top of the window
    column_padding = 15  # chars

    def __init__(self, inv_col, height, visible=False):
        self.inv_col = inv_col
        self.height = height - 1
        self.max_size = len(DROP_KEYS)
        self.visible = visible

    def add_item(self, obj):
        if len(self.content) == self.max_size:
            raise InventoryIsFullException
        self.content.append(obj)
        if self.visible:
            self.draw()

    def remove_item(self, obj_id):
        for i in range(len(self.content)):
            if self.content[i].id == obj_id:
                del self.content[i]
                break
        if self.visible:
            self.draw()

    def draw(self):
        print(Color.l_yellow, end='')
        tm.move_cursor_to(self.inv_line, self.inv_col)
        tm.clear_line()
        print(f'☼ Inventory {len(self.content)}/{self.max_size}')
        self._clear_lines()
        tm.move_cursor_to(self.inv_line + 1, self.inv_col)
        if len(self.content) == 0:
            print('Your backpack is empty')
        else:  
            column_delta = 0
            inventory_row = 0
            for i in range(len(self.content)):
                if (inventory_row + 1) % self.height == 0:
                    column_delta += self.column_padding
                    inventory_row = 0
                tm.move_cursor_to(self.inv_line + 1 + inventory_row, self.inv_col + column_delta)
                inventory_row += 1
                tm.clear_line()
                print(f'[{DROP_KEYS[i]}] {self.content[i].name}', end='')
        print(Color.reset, end='')

    def _clear_lines(self):
        for i in range(self.height - 1):
            tm.move_cursor_to(self.inv_line + 1 + i, self.inv_col)
            tm.clear_line()

    def item_inside(self, obj):
        if any(isinstance(i, obj) for i in self.content):
            return True
        else:
            return False


class InventoryIsFullException(Exception):
    def __init__(self, message='Inventory is full'):
        super().__init__(message)
