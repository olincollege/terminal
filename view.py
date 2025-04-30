from time import sleep
import curses
import pygame
from model import Model, TextFile, ImageFile, Directory
from controller import Controller


class View:
    """
    View class for game.
    """

    def __init__(self, stdscr, controller):
        self._stdscr = stdscr
        self._pad = curses.newpad(100, 100)
        self._model = Model()
        self._controller = controller

    def current_path_to_string(self, dir_path):
        """
        Converts a list of directories into a string.

        Args:
            dir_path: List of File objects representing the path of the
                current file

        Returns:
            String: String of file names, seperated by "/"s.
        """
        path = ""
        for element in dir_path:
            path += "/" + element.name
        return path

    def display_text_file(self, file, path):
        """
        Displays contents of text file on the current window.

        Args:
            file: TextFile object representing the file to be displayed.
            path: List of File objects representing the path of the file.
        """
        self._stdscr.clear()

        # Display path at top of screen
        self._stdscr.addstr(0, 0, self.current_path_to_string(path))
        self._stdscr.refresh()

        # Find dimensions of window
        rows, cols = self._stdscr.getmaxyx()
        rows -= 1
        cols -= 1

        # Create pad to store text
        text_pad = curses.newpad(1000, cols)
        mypad_pos = 0

        # Split file contents by line
        text_lines = file.contents.split("\n")
        # Add each line to the pad, splitting when end of window width is reached
        current_row = 0
        for line in text_lines:
            for i in range(int(len(line) / cols)):
                text_pad.addstr(
                    current_row, 0, line[cols * i : cols * (i + 1) + 1]
                )
                current_row += 1
            text_pad.addstr(current_row, 0, line[-(len(line) % cols) :])
            current_row += 1

        # Display initial text
        text_pad.refresh(0, 0, 2, 0, rows, cols)

        # Use keyboard arrow key input to scroll up or down
        while True:
            input_key = self._stdscr.getch()
            if input_key == curses.KEY_DOWN:
                mypad_pos += 1
            elif input_key == curses.KEY_UP:
                mypad_pos -= 1
            elif input_key == 113:
                break

            text_pad.refresh(mypad_pos, 0, 2, 0, rows, cols)
            sleep(0.002)

    def display_image_file(self, file, path):
        """
        Displays contents of image file in a new window.

        Args:
            file: ImageFile object representing the file to be displayed.
            path: List of File objects representing the path of the file.
        """
        scrn = pygame.display.set_mode(
            (file.contents.get_width(), file.contents.get_height())
        )
        pygame.display.set_caption(self.current_path_to_string(path))
        imp = file.contents.convert()
        scrn.blit(imp, (0, 0))
        pygame.display.flip()

        status = True
        while status:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    status = False

        pygame.quit()

    def display_directory(self, directory, path):
        """
        Display immediate contents of a directory in the current window
        - Show folder names (with /)
        - Show file names
        - Do not expand inside folders
        - Each file is numbered, starting from 1

        Args:
            file: Directory object representing the directory to be displayed.
            path: List of File objects representing the path of the directory.

        """
        self._stdscr.clear()

        self._stdscr.addstr(0, 0, self.current_path_to_string(path))

        row = 2

        for i, item in enumerate(directory.contents):
            if isinstance(item, Directory):
                self._stdscr.addstr(row, 0, f"{i+1}. {item.name}/")
            else:
                self._stdscr.addstr(row, 0, f"{i + 1}. {item.name}")
            row += 1

        self._stdscr.refresh()

    def display_bookmarks(self):
        """
        Display currently bookmarked files in the current window
        - Show file names
        - Each file is numbered, starting from 1
        """
        pass
        # TODO

    def display_file(self, file, path):
        """
        Display a file's contents.

        Args:
            file: File object representing the file or directory to be displayed.
            path: List of File objects representing the path of the directory.

        """
        if isinstance(file, Directory):
            self.display_directory(file, path)
        elif isinstance(file, TextFile):
            self.display_text_file(file, path)
            return
        elif isinstance(file, ImageFile):
            self.display_image_file(file, path)
