import curses
from time import sleep


class Controller:

    def __init__(self, pad, model):
        self._pad = pad
        self._model = model

    def get_key_press(self):
        while True:
            key = self._pad.getkey()
            if key is not None:
                if key == "+":
                    self._model.bookmark()
            return key()

    def store_inventory(self):
        pass

    def bookmark(self):
        while True:
            return self._pad.getkey()

    def enter_password(self):
        entered_password = ""
        while self._pad.getkey() != "e":
            entered_password = self._pad.getkey()
