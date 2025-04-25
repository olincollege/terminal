import curses
from model import Model
from view import View
from controller import Controller  # if needed


def main():
    stdscr = curses.initscr()

    model = Model()
    view = View(stdscr)  # <<< Pass model into View's constructor!
    controller = Controller()  # if you have this

    accessible_artifacts = model.get_accessible_folders()
    view.display_directory(model, accessible_artifacts)


if __name__ == "__main__":
    main()
