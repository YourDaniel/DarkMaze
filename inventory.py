from ansi_wraps import Color
from ansi_wraps import TerminalManager

tm = TerminalManager()
drop_keys = ('q', 'w', 'e', 'r', 't', 'y', 'a', 's', 'd', 'f', 'g', 'h')


class Inventory:
    content = []
    inv_line = 0  # Inventory starts from top of the window

    def __init__(self, inv_col):
        self.inv_col = inv_col

    def add_item(self, obj):
        self.content.append(obj)
        self.draw()

    def remove_item(self, obj_id):
        for i in range(len(self.content)):
            if self.content[i].id == obj_id:
                del self.content[i]
                break
        self.draw()

    def draw(self):
        print(Color.l_yellow, end='')
        tm.move_cursor_to(self.inv_line, self.inv_col)
        print('Inventory:')
        self.clear_lines()
        tm.move_cursor_to(self.inv_line + 1, self.inv_col)
        if len(self.content) == 0:
            print('Your backpack is empty')
        else:
            for i in range(len(self.content)):
                tm.move_cursor_to(self.inv_line + 1 + i, self.inv_col)
                tm.clear_line()
                print(f'[{drop_keys[i]}]', end=' ')
                print(self.content[i].name, end='')
        print(Color.reset, end='')

    def clear_lines(self):
        for i in range(len(drop_keys)):
            tm.move_cursor_to(self.inv_line + 1 + i, self.inv_col)
            tm.clear_line()

    def item_inside(self, obj):
        if any(isinstance(i, obj) for i in self.content):
            return True
        else:
            return False
