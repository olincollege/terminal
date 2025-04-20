import pygame
import curses


class Model:

    def __init__(self):
        self._player_name = "____"


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

    def __init__(self, filename, content_names):
        super().__init__(filename)
        self._contents = []
        for name in content_names:
            if name[-3:] == "txt":
                self._contents.append(TextFile(name))
            elif name[-3:] == "png":
                self._contents.append(ImageFile(name))
            else:
                self._contents.append(Directory(name))  # needs to be fixed
