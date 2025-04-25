import curses
from time import sleep

class Controller:


    def __init__(self,pad):
        self._pad = pad

# pad.getkey #string representing file that was pressed
    #store and print pad.get_key

    def get_key_press(self):
        while True:
            if self._pad.getkey() is not None:
                return self.pad.getkey()
            if self.pad.getkey() == "+":
                self.model.bookmark()



    def store_inventory(self):
        pass


    def bookmark(self):
        while True:
                return self.pad.getkey()

    def enter_password(self):
        entered_password = ""
        while self._pad_getkey != "e":
            entered_password = self._pad.getkey()
