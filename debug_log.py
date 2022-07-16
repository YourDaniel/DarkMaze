def debug(msg):
    with open('debug_file.txt', 'a') as f:
        f.write(msg + '\n')
