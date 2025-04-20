import curses
import os

from model import Model
from view import View
from controller import Controller


def main():
    print("hey there")

    stdscr = curses.initscr()

    game_model = Model()
    game_view = View(stdscr)
    game_controller = Controller()


if __name__ == "__main__":
    main()
