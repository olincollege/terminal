"""
Controller module for handling user input in a curses-based interface.
"""

from time import sleep


class Controller:
    """
    Handles key input and password entry using a curses stdscr object.
    """

    def __init__(self, stdscr, model):
        """
        Initialize the Controller.

        Args:
            stdscr (curses.window): The curses standard screen object.
            model (object): A model instance for managing game state.
        """
        self._stdscr = stdscr
        self._model = model

    def get_key_press(self):
        """
        Wait for and return a single key press from the user.

        Returns:
            str: The key character entered by the user.
        """
        while True:
            key = self._stdscr.getkey()
            if key is not None:
                return key
            sleep(0.002)

    def enter_password(self):
        """
        Capture user input character by character until newline is entered.

        Returns:
            str: The full password input by the user.
        """
        entered_password = ""
        while True:
            key = self._stdscr.getkey()
            if key == "\n":
                break
            entered_password += key
        return entered_password
