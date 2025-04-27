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
                    #View should have bookmark method?
            return key

    def enter_password(self):
        entered_password = ""
        while True:
            key = self._pad.getkey()
            if key == "e":
                break
            entered_password += key
        return entered_password
