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
        self._bookmarks = []  # List of bookmarked files
        self._player_name = "____"
        self._unlock_level = 1  # Player starts with only level 1 unlocked
        self._unlock_password = {  # Passwords required to unlock higher levels
            2: "vires_in_silentio",
            3: "CENTINEL-1",
        }

    def bookmark(self, file):
        """
        Adds the current file to the bookmark list.

        Args:
            file (File): File or Directory object to bookmark.
        """
        self._bookmarks.append(file)

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

    @property
    def bookmarks(self):
        """
        Access the list of bookmarked files.

        Returns:
            list: Bookmarked File/Directory objects.
        """
        return self._bookmarks

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

    def get_accessible_folders(self):
        """
        Return list of folders named 'artifacts_X' in the artifacts directory.

        Returns:
            list[str]: Folder names that match the 'artifacts_' prefix.
        """
        base_path = "artifacts"
        folders = []

        # Check if the artifacts directory exists
        if os.path.exists(base_path):
            for folder in os.listdir(base_path):
                folder_path = os.path.join(base_path, folder)

                # Only include folders that start with 'artifacts_'
                if os.path.isdir(folder_path) and folder.startswith(
                    "artifacts_"
                ):
                    folders.append(folder)

        return folders

    def get_accessible_contents(self, folder_name):
        """
        Given a folder name (e.g., artifacts_1), return its files if unlocked,
        otherwise return ["LOCKED"].

        Args:
            folder_name (str): Name of the folder to access.

        Returns:
            list[str]: File names or ["LOCKED"] if access is restricted.
        """
        base_path = "artifacts"
        folder_path = os.path.join(base_path, folder_name)

        folder_number = None
        # Try to extract the folder number (e.g., "artifacts_2" → 2)
        if folder_name.startswith("artifacts_"):
            try:
                folder_number = int(folder_name.split("_")[1])
            except (IndexError, ValueError):
                pass  # Ignore if format is wrong

        # If the folder's unlock level is too high, block access
        if folder_number is not None and folder_number > self._unlock_level:
            return ["LOCKED"]

        # If unlocked, return its sorted contents
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            files.sort()
            return files

        return []  # Return empty list if folder doesn't exist


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
