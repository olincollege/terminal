import curses
import pygame
from model import Model, TextFile, ImageFile, Directory


class View:
    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._pad = curses.newpad(100, 100)
        self._model = Model()

    def current_path_to_string(self, dir_path):
        path = ""
        for element in dir_path:
            path += "/" + element.name
        return path

    def display_text_file(self, file, path):
        self._stdscr.clear()
        self._stdscr.addstr(0, 0, self.current_path_to_string(path))
        self._stdscr.addstr(2, 0, file.contents)
        self._stdscr.refresh()

    def display_image_file(self, file, path):
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
        Display immediate contents of the current directory:
        - Show folder names (with /)
        - Show file names
        - Do not expand inside folders
        """
        self._stdscr.clear()

        self._stdscr.addstr(0, 0, self.current_path_to_string(path))

        row = 2

        if isinstance(directory, list):
            for folder_name in directory:
                self._stdscr.addstr(row, 0, f"{folder_name}/")
                row += 1
        else:
            for i, item in enumerate(directory.contents):
                if isinstance(item, Directory):
                    self._stdscr.addstr(row, 0, f"{i+1}. {item.name}/")
                else:
                    self._stdscr.addstr(row, 0, f"{i + 1}. {item.name}")
                row += 1

        self._stdscr.refresh()

    def display_bookmarks(self):
        pass
        # TODO

    def display_file(self, file, path):
        """
        Display a file's contents.
        """
        if isinstance(file, Directory):
            self.display_directory(file, path)
        elif isinstance(file, TextFile):
            self.display_text_file(file, path)
        elif isinstance(file, ImageFile):
            self.display_image_file(file, path)

    def display_bookmarks(self):
        pass
