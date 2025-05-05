from time import sleep
import curses
import pygame
from model import Directory, TextFile, ImageFile


class View:
    """
    View class for game.
    """

    def __init__(self, stdscr, controller, model):
        self._stdscr = stdscr
        self._model = model
        self._controller = controller

        self._rows, self._cols = self._stdscr.getmaxyx()
        self._rows -= 1
        self._cols -= 1

        self._file_instructions = [
            "Press + to toggle bookmark",
            "Press Q to go back",
        ]
        self._dir_instructions = [
            "Press number keys to open files",
            "Press Q to go back",
        ]

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

        # Display path at top left of screen
        self._stdscr.addstr(0, 0, self.current_path_to_string(path))
        # Display instructions at top right
        for i, line in enumerate(self._file_instructions):
            self._stdscr.addstr(i, self._cols - 30, line)
        self._stdscr.refresh()

        # Create pad to store text
        text_pad = curses.newpad(1000, self._cols)
        mypad_pos = 0

        # Split file contents by line
        text_lines = file.contents.split("\n")
        # Add each line to the pad, splitting when end of window width is reached
        current_row = 0
        for line in text_lines:
            for i in range(int(len(line) / self._cols)):
                text_pad.addstr(
                    current_row,
                    0,
                    line[self._cols * i : self._cols * (i + 1) + 1],
                )
                current_row += 1
            text_pad.addstr(current_row, 0, line[-(len(line) % self._cols) :])
            current_row += 1

        # Display initial text
        text_pad.refresh(0, 0, 2, 0, self._rows, self._cols)

        # Use keyboard arrow key input to scroll up or down
        while True:
            input_key = self._stdscr.getch()
            if input_key == curses.KEY_DOWN:
                mypad_pos += 1
            elif input_key == curses.KEY_UP:
                mypad_pos -= 1
            elif input_key == 113:
                break

            text_pad.refresh(mypad_pos, 0, 2, 0, self._rows, self._cols)
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

    def display_file_list(self, files, header):
        """
        Display a list of files in the current window
        - Show folder names (with /)
        - Show file names
        - Do not expand inside folders
        - Each file is numbered, starting from 1

        Args:
            files: List of File objects to be displayed.
            header: String to be printed at the top of the screen.
        """
        self._stdscr.clear()

        self._stdscr.addstr(0, 0, header)
        # Display instructions at top right
        for i, line in enumerate(self._dir_instructions):
            self._stdscr.addstr(i, self._cols - 30, line)

        row = 2

        for i, item in enumerate(files):
            if isinstance(item, Directory):
                if item.lock_level > self._model.unlock_level:
                    self._stdscr.addstr(row, 0, f"{i+1}. [LOCKED]")
                else:
                    self._stdscr.addstr(row, 0, f"{i+1}. {item.name}/")
            else:
                self._stdscr.addstr(row, 0, f"{i+1}. {item.name}")
            row += 1

        self._stdscr.refresh()

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

        if directory.lock_level > self._model.unlock_level:
            if self.password_entry(self._model.passwords[directory.lock_level]):
                self._model.increase_level()
                self.display_directory(directory, path)
            else:
                return
        else:
            self.display_file_list(
                directory.contents, self.current_path_to_string(path)
            )

    def display_bookmarks(self):
        """
        Display currently bookmarked files in the current window
        - Show file names
        - Each file is numbered, starting from 1
        """
        self.display_file_list(self._model.bookmarks, "Bookmarks")

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
        elif isinstance(file, ImageFile):
            self.display_image_file(file, path)

    def password_entry(self, password):
        self._stdscr.clear()
        self._stdscr.addstr("File locked. Enter password to authorize entry: ")

        entered_password = ""
        while True:
            key = self._stdscr.getkey()
            if key is not None:
                if key == "\n":
                    if entered_password == password:
                        return True
                    return False
                # if key ==
                self._stdscr.addstr(key)
                entered_password += str(key)
            sleep(0.002)
