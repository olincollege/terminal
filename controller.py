import curses
from time import sleep


class Controller:

    def __init__(self, stdscr, model):
        self._stdscr = stdscr
        self._model = model

    def get_key_press(self):
        while True:
            key = self._stdscr.getkey()
            if key is not None:
                return key
            sleep(0.002)

    def enter_password(self):
        entered_password = ""
        while True:
            key = self._stdscr.getkey()
            if key == "\n":
                break
            entered_password += key
        return entered_password
