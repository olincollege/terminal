import os
import pygame
import curses


class Model:

    def __init__(self):
        self._player_name = "____"
        self._unlock_level = 1
        self._unlock_password = {2: "vires_in_silentio", 3: "TESTETSETESTSET"}

    @property
    def unlock_level(self):
        """
        Retrieve the current unlock status of the player.

        Returns:
            int: The current unlock level of the player.
        """
        return self._unlock_level

    @property
    def passwords(self):
        return self._unlock_password

    def increase_level(self):
        self._unlock_level += 1


class File:

    def __init__(self, name, path):

        self._name = name[1:]
        self._contents = None
        os.chdir(path)

    @property
    def name(self):
        return self._name

    @property
    def contents(self):
        return self._contents


class TextFile(File):

    def __init__(self, filename, path):
        super().__init__(filename, path)
        with open(filename, "r") as f:
            self._contents = f.read()


class ImageFile(File):

    def __init__(self, filename, path):
        super().__init__(filename, path)
        self._contents = pygame.image.load(filename)


class Directory(File):

    def __init__(self, filename, path=os.getcwd()):
        super().__init__(filename, path)

        self._lock_level = 1
        if filename == "2archive":
            self._lock_level = 2
        elif filename == "3message":
            self._lock_level = 3

        path = path + "/" + filename
        os.chdir(path)

        self._contents = []

        names = os.listdir(path)[:]
        names.sort()

        for name in names:
            if name[-3:] == "txt":
                self._contents.append(TextFile(name, path))
            elif name[-3:] == "png":
                self._contents.append(ImageFile(name, path))
            else:
                self._contents.append(Directory(name, path))

    @property
    def lock_level(self):
        return self._lock_level
