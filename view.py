import time
from curses import wrapper
import curses
import os


class View:

    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._pad = curses.newpad(100, 100)

    def display_directory(self, accessible_artifacts):
        """
        Displays all files from the accessible artifact layers.

        Args:
            accessible_artifacts (list): List of accessible artifact layer names.
        """
        self._stdscr.clear()
        row = 0
        for layer in accessible_artifacts:
            layer_path = os.path.join("artifacts", layer)
            if os.path.isdir(layer_path):
                files = [
                    f
                    for f in os.listdir(layer_path)
                    if os.path.isfile(os.path.join(layer_path, f))
                ]
                self._stdscr.addstr(row, 0, f"{layer}/")
                row += 1
                for i, file in enumerate(files):
                    self._stdscr.addstr(row, 1, str(i + 1))
                    self._stdscr.addstr(row, 3, file)
                    row += 1
            else:
                self._stdscr.addstr(row, 0, f"{layer}/ (Not Found)")
                row += 1
        self._stdscr.refresh()
        self._stdscr.getch()  # Wait for user input

    def display_file(self, file):
        file.display()

    def display_bookmarks(self):
        pass
