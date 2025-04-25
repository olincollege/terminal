import curses
from time import sleep

class Controller:


    def __init__(self,pad):
        self._pad = pad

# pad.getkey #string representing file that was pressed
    #store and print pad.get_key

    def get_key_press(self):
        while True:
            if self._pad.get_key() is not None:
                return self.pad.get_key()
            if self.pad.get_key() == "+":
                self.model.bookmark()



    def store_inventory(self):
        pass


    def bookmark(self):
        while True:
                return self.pad.get_key()

    def enter_password(self):
        entered_password = ""
        while self._pad_get_key != "e":
            #entered_password
