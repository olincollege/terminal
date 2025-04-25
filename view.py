import time
from curses import wrapper
import curses
import os
from model import Model


class View:

    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._pad = curses.newpad(100, 100)
        self._model = Model

    def display_directory(self, model, accessible_artifacts):
        self._stdscr.clear()
        row = 0
        for layer in accessible_artifacts:
            self._stdscr.addstr(row, 0, f"{layer}/")
            row += 1

            files = model.get_accessible_contents(layer)

            if files == ["LOCKED"]:
                self._stdscr.addstr(row, 2, "LOCKED")
                row += 1
            elif files == []:
                self._stdscr.addstr(row, 2, "(No files)")
                row += 1
            else:
                for i, file in enumerate(files):
                    self._stdscr.addstr(row, 2, f"{i + 1}. {file}")
                    row += 1

        self._stdscr.refresh()
        self._stdscr.getch()

    def display_file(self, file):
        file.display()

    def display_bookmarks(self):
        pass
