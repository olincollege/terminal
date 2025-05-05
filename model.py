import os
import pygame
import curses


class Model:

    def __init__(self):
        self._bookmarks = []
        self._player_name = "____"
        self._unlock_level = 1
        self._unlock_password = {2: "vires_in_silentio", 3: "CENTENIEL-1"}

    def bookmark(self, file):
        """
        Adds the current file to the bookmark list

        Args:
            file (_type_): _description_
        """
        self._bookmarks.append(file)

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

    @property
    def bookmarks(self):
        return self._bookmarks

    def increase_level(self):
        self._unlock_level += 1

    def get_accessible_folders(self):
        """
        Returns a list of all artifact folders (artifacts_1, artifacts_2, etc.)
        """
        base_path = "artifacts"
        folders = []

        if os.path.exists(base_path):
            for folder in os.listdir(base_path):
                folder_path = os.path.join(base_path, folder)
                if os.path.isdir(folder_path) and folder.startswith(
                    "artifacts_"
                ):
                    folders.append(folder)

        return folders

    def set_unlock_level(self, level):
        """
        Set the current unlock level manually (e.g., for testing).

        Args:
            level (int): The desired unlock level.

        Returns:
            None
        """
        self._unlock_level = level

    def get_accessible_contents(self, folder_name):
        """
        Given a folder name (e.g., artifacts_1), return a list of its files
        if unlocked. Otherwise, return ["LOCKED"].
        """
        base_path = "artifacts"
        folder_path = os.path.join(base_path, folder_name)

        # Parse folder number
        folder_number = None
        if folder_name.startswith("artifacts_"):
            try:
                folder_number = int(folder_name.split("_")[1])
            except (IndexError, ValueError):
                pass  # folder_number stays None

        # Check if folder is locked
        if folder_number is not None and folder_number > self._unlock_level:
            return ["LOCKED"]

        # If unlocked, list files
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            files.sort()  # Optional: sort files alphabetically
            return files

        return []  # Folder doesn't exist or empty


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
