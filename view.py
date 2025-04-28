import os
import curses
from model import Model, Directory


class View:
    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._pad = curses.newpad(100, 100)
        self._model = Model()

    def display_directory(self, directory):
        """
        Display immediate contents of the current directory:
        - Show folder names (with /)
        - Show file names
        - Do not expand inside folders
        """
        self._stdscr.clear()
        row = 0

        if isinstance(directory, list):
            for folder_name in directory:
                self._stdscr.addstr(row, 0, f"{folder_name}/")
                row += 1
        else:
            for i, item in enumerate(directory.contents):
                if hasattr(item, "contents"):
                    self._stdscr.addstr(row, 2, f"{item.name}/")
                else:
                    self._stdscr.addstr(row, 2, f"{i + 1}. {item.name}")
                row += 1

        self._stdscr.refresh()
        key = self._stdscr.getch()
        return key

    def display_file(self, file):
        """
        Display a file's contents.
        """
        file.display()

    def display_bookmarks(self):
        pass
