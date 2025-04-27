import os
import pygame
import curses


class Model:

    def __init__(self):
        self._bookmark = []
        self._player_name = "____"
        self._unlock_status = 1
        self._unlock_password = {2: "vires_in_silentio", 3: "TESTETSETESTSET"}

    def bookmark(self, file):
        """
        Adds the current file to the bookmark list

        Args:
            file (_type_): _description_
        """
        self._bookmark.append(file)

    @property
    def unlock_status(self):
        """
        Retrieve the current unlock status of the player.

        Returns:
            int: The current unlock level of the player.
        """
        return self.unlock_status

    def verify_password_unlock(self, player_input):
        """
        Verify the player's input and unlock the next level if the input matches the required password.

        Args:
            player_input (str): The password input provided by the player.

        Returns:
            None, increases unlock status
        """
        next_level = self._unlock_status + 1

        # if the input from the player matches the corresponding password in the dictionary
        # the player moves up a level and unlocks the next layer of artifacts
        if player_input == self._unlock_password[next_level]:
            self._unlock_status = next_level

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
        if folder_number is not None and folder_number > self._unlock_status:
            return ["LOCKED"]

        # If unlocked, list files
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            files.sort()  # Optional: sort files alphabetically
            return files

        return []  # Folder doesn't exist or empty


class File:

    def __init__(self, name, path):

        self._name = name
        os.chdir(path)

    @property
    def name(self):
        return self._name

    def display(self):
        pass


class TextFile(File):

    def __init__(self, filename, path):
        super().__init__(filename, path)
        with open(filename, "r") as f:
            self._contents = f.read()

    def display(self):
        pad = curses.newpad(100, 100)
        pad.move(0, 0)
        pad.addstr(self._contents)
        pad.refresh(0, 0, 0, 0, 100, 100)


class ImageFile(File):

    def __init__(self, filename, path):
        super().__init__(filename, path)
        self._contents = pygame.image.load(filename)

    def display(self):
        scrn = pygame.display.set_mode(
            (self._contents.get_width(), self._contents.get_height())
        )
        pygame.display.set_caption(self._name)
        imp = self._contents.convert()
        scrn.blit(imp, (0, 0))
        pygame.display.flip()

        status = True
        while status:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    status = False

        pygame.quit()


class Directory(File):

    def __init__(self, filename, path=os.getcwd()):
        super().__init__(filename, path)

        path = path + "/" + filename
        os.chdir(path)

        self._contents = []
        for name in os.listdir(path):
            if name[-3:] == "txt":
                self._contents.append(TextFile(name, path))
            elif name[-3:] == "jpeg":
                self._contents.append(ImageFile(name, path))
            else:
                self._contents.append(Directory(name, path))

    @property
    def contents(self):
        return self._contents

    def display(self):
        print(self._name)
        for file in self._contents:
            print(file.name)
