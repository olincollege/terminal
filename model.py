"""
Model module for managing game state, file access, and directory structure.
"""

import os
import pygame


class Model:
    """
    Handles game state including unlock level, and file system access.
    """

    def __init__(self):
        """
        Initialize the model with default player state.
        """
        self._player_name = "____"
        self._unlock_level = 1  # Player starts with only level 1 unlocked
        self._unlock_password = {  # Passwords required to unlock higher levels
            2: "vires_in_silentio",
            3: "CENTINEL-1",
        }

    @property
    def unlock_level(self):
        """
        Retrieve the current unlock level.

        Returns:
            int: The unlock level of the player.
        """
        return self._unlock_level

    @property
    def passwords(self):
        """
        Access the password dictionary.

        Returns:
            dict: Level-password mapping.
        """
        return self._unlock_password

    def increase_level(self):
        """
        Increment the player's unlock level by one.
        """
        self._unlock_level += 1

    def set_unlock_level(self, level):
        """
        Set the current unlock level manually (e.g., for testing).

        Args:
            level (int): The desired unlock level.
        """
        self._unlock_level = level


class File:
    """
    Base class representing a generic file in the game.
    """

    def __init__(self, name, path):
        """
        Initialize a file object and set its name and path.

        Args:
            name (str): File name with a prepended identifier character.
            path (str): Path to the file's directory.
        """
        self._name = name[1:]  # Remove the leading metadata character
        self._contents = None
        os.chdir(path)  # Move to the specified path

    @property
    def name(self):
        """
        Retrieve the file's name.

        Returns:
            str: The name of the file (without prepended character).
        """
        return self._name

    @property
    def contents(self):
        """
        Retrieve the file's contents.

        Returns:
            Any: Contents of the file (text, image, etc.).
        """
        return self._contents


class TextFile(File):
    """
    TextFile represents a readable .txt file within the game.
    """

    def __init__(self, filename, path):
        """
        Read a .txt file and store its contents.

        Args:
            filename (str): The file name.
            path (str): Directory containing the file.
        """
        super().__init__(filename, path)

        # Open the file using UTF-8 encoding and store its contents
        with open(filename, "r", encoding="utf-8") as file_obj:
            self._contents = file_obj.read()


class ImageFile(File):
    """
    ImageFile represents a .png image within the game.
    """

    def __init__(self, filename, path):
        """
        Load a .png image file using pygame.

        Args:
            filename (str): The file name.
            path (str): Directory containing the file.
        """
        super().__init__(filename, path)

        # Use pygame to load the image
        self._contents = pygame.image.load(filename)


class Directory(File):
    """
    Directory represents a navigable folder with other files or directories.
    """

    def __init__(self, filename, path=os.getcwd()):
        """
        Recursively load contents of a directory and set lock level.

        Args:
            filename (str): Name of the directory.
            path (str): Path to parent directory.
        """
        super().__init__(filename, path)

        # Set unlock level based on folder name
        self._lock_level = 1
        if filename == "2archive":
            self._lock_level = 2
        elif filename == "3message":
            self._lock_level = 3

        # Go into the specified subdirectory
        path = os.path.join(path, filename)
        os.chdir(path)

        self._contents = []

        # Get list of files in directory
        names = os.listdir(path)
        names.sort()

        # Recursively load files or subdirectories
        for name in names:
            if name.endswith(".txt"):
                self._contents.append(TextFile(name, path))
            elif name.endswith(".png"):
                self._contents.append(ImageFile(name, path))
            else:
                self._contents.append(Directory(name, path))

    @property
    def lock_level(self):
        """
        Return the required unlock level for this directory.

        Returns:
            int: The lock level (1–3).
        """
        return self._lock_level
