import os
from readchar import readkey

levels = (1, 2) #sets the number of levels
level = []
floor_tile = '.'
wall_tile = '█'
stairs_down = '▼'
pressure_plate = '□'
door_v = '║'
hero = '@'
key = '╘'
keys_count = 0
level_passed = False


def clear():
    os.system('cls')


def load_level(file_name):
    global level
    level = []
    with open(file_name, encoding='UTF-8-sig') as f:
        data = f.read()
    line = []
    for char in data:
        if char != '\n':
            line.append(char)
        else:
            level.append(line)
            line = []
    return True


def draw_level():
    clear()
    print('-------Lvl-1--------')
    for i in range(len(level)):
        for j in range(len(level[i])):
            print(level[i][j], end='')
        print()
    print(f'Keys: {keys_count}')


def place_hero(x, y):
    level[x][y] = hero
    pos = (x, y)
    return pos


def find_hero():
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == hero:
                pos = (i, j)
                return pos
    else:
        print('Hero is not found on level!')


def wall_collision(x, y):
    if level[x][y] == wall_tile:
        return True
    elif level[x][y] == door_v:
        global keys_count
        if keys_count < 1:
            return True
        else:
            keys_count -= 1
            return False
    else:
        return False


def move(x, y, old_pos):
    if not wall_collision(x, y):
        if level[x][y] == stairs_down:
            global level_passed
            level_passed = True
        if level[x][y] == pressure_plate:
            #TODO: Redo this hardcode
            level[2][4] = floor_tile
        if level[x][y] == key:
            global keys_count
            keys_count += 1
        level[old_pos[0]][old_pos[1]] = floor_tile
        new_pos = place_hero(x, y)
        draw_level()
        return new_pos
    else:
        print("Can't move here")
        return old_pos


def input_handler(pos):
    key_pressed = readkey()
    if key_pressed == 'w':
        pos = move(pos[0] - 1, pos[1], pos)
    elif key_pressed == 'a':
        pos = move(pos[0], pos[1] - 1, pos)
    elif key_pressed == 's':
        pos = move(pos[0] + 1, pos[1], pos)
    elif key_pressed == 'd':
        pos = move(pos[0], pos[1] + 1, pos)
    return pos


def main():
    for current_level in levels:
        load_level(f'level_{str(current_level)}.txt')
        hero_pos = find_hero()
        draw_level()
        print('Find a way downstairs! ▼')
        global level_passed
        while not level_passed:
            hero_pos = input_handler(hero_pos)
        level_passed = False
    print('Congratulations! You have won!')


if __name__ == '__main__':
    main()
