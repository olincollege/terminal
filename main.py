"""
Main entry point for the terminal-based file explorer game.

Initializes the model, controller, and view, and runs the main game loop.
"""

from time import sleep
import curses
from model import Model, Directory
from view import View
from controller import Controller


def main(stdscr):
    """
    Launch the game UI and handle navigation input.

    Args:
        stdscr (curses.window): The curses standard screen window.

    Returns:
        None
    """
    model = Model()
    controller = Controller(stdscr, model)
    view = View(stdscr, controller, model)

    basedir = Directory("1documents")
    current_dir = basedir
    current_dir_path = [current_dir]

    view.display_file(current_dir, current_dir_path)

    game_loop = True
    while game_loop:

        # get input from controller
        input_key = controller.get_key_press()

        # navigate back
        if input_key in ("q", "Q"):
            if len(current_dir_path) > 1:
                current_dir = current_dir_path[-2]
                current_dir_path = current_dir_path[:-1]
                view.display_file(current_dir, current_dir_path)

        # open file
        else:
            try:
                selected_file = current_dir.contents[int(input_key) - 1]
                current_dir = selected_file
                current_dir_path.append(current_dir)
                view.display_file(selected_file, current_dir_path)

                if not isinstance(selected_file, Directory):
                    if len(current_dir_path) > 1:
                        current_dir = current_dir_path[-2]
                        current_dir_path = current_dir_path[:-1]
                        view.display_file(current_dir, current_dir_path)

            except (IndexError, ValueError, AttributeError):
                # Ignore invalid input or no key pressed
                pass

        sleep(0.002)


if __name__ == "__main__":
    curses.wrapper(main)
