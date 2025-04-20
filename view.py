import time
from curses import wrapper
import curses


class View:

    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._pad = curses.newpad(100, 100)

    def display_directory(self, directory):
        self._stdscr.clear()
        x = 0
        y = 0
        for file in directory:
            self._pad.addstr(y, x, file.name)
            y += 1

        y += 1
        self._pad.move(y, x)
        self._pad.refresh(0, 0, 0, 0, 20, 75)

        while True:
            self._pad.addstr(self._pad.getkey())

            self._pad.refresh(0, 0, 0, 0, 20, 75)
            time.sleep(0.02)

    def display_file(self, file):
        file.display()

    def display_bookmarks(self):
        pass
