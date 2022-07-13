from datetime import datetime
from ansi_wraps import TerminalManager, Color

tm = TerminalManager()


class Log:
    messages = []

    def __init__(self, log_line, log_len=10, timestamps=False, log_to_file=False):
        self.log_len = log_len
        self.timestamps_on = timestamps
        self.log_to_file = log_to_file
        if self.log_to_file:
            self.filename = 'logs/log.txt'
            with open(self.filename, 'a', encoding='UTF-8') as f:
                f.write('--------------------------------------\n')
                f.write(datetime.today().strftime("Game session at %H:%M:%S on %d.%m.%Y\n"))

        self.log_line = log_line

    def add_msg(self, msg):
        timestamp = ''  # TODO: add repeating messages when timestamps are on
        if self.timestamps_on:
            timestamp = datetime.today().strftime("[%H:%M:%S] ")
        if self.log_to_file:
            with open(self.filename, 'a', encoding='UTF-8') as f:
                f.write(timestamp + msg + '\n')

        if len(self.messages) > 0 and self.messages[0][0] == msg:
            self.messages[0][1] += 1
        else:
            block = [timestamp + msg, 1]  # 2nd value - number of same msg
            self.messages.insert(0, block)
        if len(self.messages) > self.log_len:  # Cutting log to max size
            self.messages = self.messages[:self.log_len]
        self.draw()

    # TODO: Make messages of different colors (warnings, battle, common etc.) and highlight items
    def draw(self):
        print(Color.l_blue, end='')
        # First, set cursor to a start of line where Log should be drawn with ESC sequence
        tm.move_cursor_to(self.log_line, 0)
        for i in range(len(self.messages)):
            msg_text = self.messages[i][0]
            msg_count = self.messages[i][1]
            # Then clear old message to print out a new one
            tm.clear_line()
            if msg_count > 1:
                print(f'{msg_text} x {msg_count}')
            else:
                print(msg_text)
        print(Color.reset, end='')
