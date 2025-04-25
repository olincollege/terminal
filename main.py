from time import sleep
import os
import curses
from model import Model
from model import TextFile
from model import ImageFile
from model import Directory
from view import View
from controller import Controller


def main():
    stdscr = curses.initscr()

    model = Model()
    view = View(stdscr)
    controller = Controller(curses.newpad(100, 100), model)
    # accessible_artifacts = model.get_accessible_artifacts()

    basedir = Directory("artifacts")

    current_dir = basedir

    game_loop = True
    while game_loop:
        view.display_dir(current_dir)
        input = controller.get_key_press()
        try:
            view.display_file(current_dir.contents[int(input) - 1])
        except:
            pass
        sleep(0.02)


if __name__ == "__main__":
    curses.wrapper(main)
