from datetime import datetime
from ansi_wraps import *
from colorama import Fore, Style
import os


class Log:
    messages = []
      # Log starts from this row in a terminal window

    def __init__(self, log_len, timestamps, log_to_file, filename, log_line):
        self.log_len = log_len
        self.timestamps_on = timestamps
        self.log_to_file = log_to_file
        self.filename = filename
        if self.log_to_file:
            with open(self.filename, 'a', encoding='UTF-8') as f:
                f.write('--------------------------------------\n')
                f.write(datetime.today().strftime("Game session at %H:%M:%S on %d.%m.%Y\n"))

        self.log_line = log_line

    def add_msg(self, msg):
        timestamp = datetime.today().strftime("[%H:%M:%S] ")
        if self.log_to_file:
            with open(self.filename, 'a', encoding='UTF-8') as f:
                f.write(timestamp + msg + '\n')

        if len(self.messages) > 0 and self.messages[0][0] == msg:
            self.messages[0][1] += 1
        else:
            if self.timestamps_on:
                block = [timestamp + msg, 1]  # 2nd value - number of same msg
            else:
                block = [msg, 1]
            self.messages.insert(0, block)
        if len(self.messages) > self.log_len:  # Cutting log to max size
            self.messages = self.messages[:self.log_len]
        self.draw()

    # TODO: Make messages of different colors (warnings, battle, common etc.) and highlight items
    def draw(self):
        print(Fore.LIGHTBLUE_EX, end='')
        # First, set cursor to a start of line where Log should be drawn with ESC sequence
        move_cursor_to(self.log_line, 0)
        for i in range(len(self.messages)):
            msg_text = self.messages[i][0]
            msg_count = self.messages[i][1]
            # Then clear old message to print out a new one
            clear_line()
            if msg_count > 1:
                print(f'{msg_text} x {msg_count}')
            else:
                print(msg_text)
        print(Style.RESET_ALL, end='')
