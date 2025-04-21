import curses
from model import Model
from view import View


def main(stdscr):
    model = Model()
    view = View(stdscr)
    accessible_artifacts = model.get_accessible_artifacts()
    view.display_directory(accessible_artifacts)


if __name__ == "__main__":
    curses.wrapper(main)
