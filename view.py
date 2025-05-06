"""
View module for handling all visual display and user interaction logic.
"""

from time import sleep
import curses
import pygame
from model import Directory, TextFile, ImageFile


class View:
    """
    View class for displaying file contents and interface in the game.
    """

    def __init__(self, stdscr, controller, model):
        """
        Initialize the View.

        Args:
            stdscr: Curses screen object.
            controller: Controller instance for input handling.
            model: Model instance for data and state.
        """
        self._stdscr = stdscr
        self._model = model
        self._controller = controller

        # Get max screen size and subtract 1 to avoid overflow
        self._rows, self._cols = self._stdscr.getmaxyx()
        self._rows -= 1
        self._cols -= 1

        # Instructions shown while viewing text/image files
        self._file_instructions = [
            "Press Q to go back",
        ]

        # Instructions shown while browsing directories
        self._dir_instructions = [
            "Press number keys to open files",
            "Press Q to go back",
        ]

    def current_path_to_string(self, dir_path):
        """
        Convert a list of File objects into a /-separated path string.

        Args:
            dir_path: List of File objects representing the current path.

        Returns:
            str: Full path as a string.
        """
        path = ""
        for element in dir_path:
            path += "/" + element.name
        return path

    def display_text_file(self, file, path):
        """
        Displays contents of a text file using a curses pad.

        Args:
            file: TextFile to be displayed.
            path: Path from root to this file.
        """
        self._stdscr.clear()

        # Print the current file path at top-left
        self._stdscr.addstr(0, 0, self.current_path_to_string(path))

        # Print user instructions at top-right
        for i, line in enumerate(self._file_instructions):
            self._stdscr.addstr(i, self._cols - 30, line)
        self._stdscr.refresh()

        # Create a pad to scroll through long text files
        text_pad = curses.newpad(1000, self._cols)
        mypad_pos = 0

        # Split file into lines and add to pad
        text_lines = file.contents.split("\n")
        current_row = 0

        for line in text_lines:
            # Wrap long lines that exceed screen width
            for i in range(int(len(line) / self._cols)):
                text_pad.addstr(
                    current_row,
                    0,
                    line[self._cols * i : self._cols * (i + 1) + 1],
                )
                current_row += 1
            # Add the remainder of the line
            text_pad.addstr(current_row, 0, line[-(len(line) % self._cols) :])
            current_row += 1

        # Render initial view of pad
        text_pad.refresh(0, 0, 2, 0, self._rows, self._cols)

        # Scroll with up/down keys, quit on "q"
        while True:
            input_key = self._stdscr.getch()
            if input_key == curses.KEY_DOWN:
                mypad_pos += 1
            elif input_key == curses.KEY_UP:
                mypad_pos -= 1
            elif input_key == 113:  # ASCII for 'q'
                break

            text_pad.refresh(mypad_pos, 0, 2, 0, self._rows, self._cols)
            sleep(0.002)

    def display_image_file(self, file, path):
        """
        Display a .png file using pygame.

        Args:
            file: ImageFile object.
            path: Path to file from root.
        """
        # Create a pygame window matching image size
        scrn = pygame.display.set_mode(
            (file.contents.get_width(), file.contents.get_height())
        )
        pygame.display.set_caption(self.current_path_to_string(path))

        # Render the image and update display
        imp = file.contents.convert()
        scrn.blit(imp, (0, 0))
        pygame.display.flip()

        # Wait until user closes the window
        status = True
        while status:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    status = False

        pygame.quit()

    def display_file_list(self, files, header):
        """
        Display a list of files and directories with indexes and header.

        Args:
            files: List of File/Directory objects.
            header: String to show as the title.
        """
        self._stdscr.clear()

        # Show the current directory name or context
        self._stdscr.addstr(0, 0, header)

        # Show instructions
        for i, line in enumerate(self._dir_instructions):
            self._stdscr.addstr(i, self._cols - 30, line)

        # Print each file/directory, numbered
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
        Display a directory, with password entry if locked.

        Args:
            directory: Directory object to view.
            path: Path list from root to this directory.
        """
        # Check if locked
        if directory.lock_level > self._model.unlock_level:
            # Prompt for password if locked
            if self.password_entry(self._model.passwords[directory.lock_level]):
                self._model.increase_level()
                self.display_directory(directory, path)
        else:
            # Show contents if unlocked
            self.display_file_list(
                directory.contents, self.current_path_to_string(path)
            )

    def display_bookmarks(self):
        """
        Display all files currently bookmarked.
        """
        self.display_file_list(self._model.bookmarks, "Bookmarks")

    def display_file(self, file, path):
        """
        Display a file or directory based on its type.

        Args:
            file: File or Directory object.
            path: Path list from root.
        """
        if isinstance(file, Directory):
            self.display_directory(file, path)
        elif isinstance(file, TextFile):
            self.display_text_file(file, path)
        elif isinstance(file, ImageFile):
            self.display_image_file(file, path)

    def password_entry(self, password):
        """
        Prompt user to enter a password and verify correctness.

        Args:
            password (str): Correct password to check against.

        Returns:
            bool: True if entered correctly, False otherwise.
        """
        self._stdscr.clear()
        self._stdscr.addstr("File locked. Enter password to authorize entry: ")

        entered_password = ""
        while True:
            key = self._stdscr.getkey()
            if key is not None:
                if key == "\n":
                    # Check password and return result
                    return entered_password == password
                # Display key as it's typed and update input
                self._stdscr.addstr(key)
                entered_password += str(key)
            sleep(0.002)
