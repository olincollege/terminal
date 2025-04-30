from time import sleep
import curses
from model import Model
from model import Directory
from view import View
from controller import Controller


def main(stdscr):

    model = Model()
    controller = Controller(stdscr, model)
    view = View(stdscr, controller)

    basedir = Directory("artifacts")

    current_dir = basedir
    current_dir_path = [current_dir]

    view.display_file(current_dir, current_dir_path)

    game_loop = True
    while game_loop:

        # get input from controller
        input_key = controller.get_key_press()

        # detect if going back
        if input_key == "q" or input_key == "Q":
            if len(current_dir_path) > 0:
                current_dir = current_dir_path[-2]
                current_dir_path = current_dir_path[:-1]
                view.display_file(current_dir, current_dir_path)
        # open file using number key
        else:
            try:
                selected_file = current_dir.contents[int(input_key) - 1]
                current_dir = selected_file
                current_dir_path.append(current_dir)
                view.display_file(selected_file, current_dir_path)

            # TODO: specify exceptions
            except:
                pass

        sleep(0.002)


if __name__ == "__main__":
    curses.wrapper(main)
