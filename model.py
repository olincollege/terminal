import os
import pygame
import curses


class Model:

    def __init__(self):
        self._player_name = "____"
        self._unlock_status = 1
        self._unlock_password = {2: "vires_in_silentio", 3: "TESTETSETESTSET"}

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

    def get_accessible_artifacts(self):
        return [f"artifacts_{i}" for i in range(1, self._unlock_status + 1)]


class File:

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def display(self):
        pass


class TextFile(File):

    def __init__(self, filename):
        super().__init__(filename)
        with open(filename, "r") as f:
            self._contents = f.read()

    def display(self):
        pad = curses.newpad(100, 100)
        pad.move(0, 0)
        pad.addstr(self._contents)
        pad.refresh(0, 0, 0, 0, 100, 100)


class ImageFile(File):

    def __init__(self, filename):
        super().__init__(filename)
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

    def __init__(self, filename, path):
        super().__init__(filename)

        os.chdir(path)

        self._contents = []
        for name in os.listdir(path):
            if name[-3:] == "txt":
                self._contents.append(TextFile(name))
            elif name[-3:] == "jpeg":
                self._contents.append(ImageFile(name))
            else:
                self._contents.append(Directory(name, path + "/" + name))

    def display(self):
        print(self._name)
        for file in self._contents:
            print(file.name)
            if file.name[-3:] != "txt":
                file.display()
