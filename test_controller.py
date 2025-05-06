"""
Unit tests for the Controller class using pytest.

Simulates user input via a mock stdscr interface to test keyboard interaction.
"""

from controller import Controller


class MockStdscr:  # pylint: disable=too-few-public-methods
    """
    Mock for the curses stdscr object to simulate getkey() inputs.
    """

    def __init__(self, inputs):
        self.inputs = inputs
        self.index = 0

    def getkey(self):
        """
        Simulates pressing a key by returning the next value from the input.

        Returns:
            str: A single character string representing a keypress.
        """
        if self.index >= len(self.inputs):
            raise IndexError("Ran out of mock inputs.")
        key = self.inputs[self.index]
        self.index += 1
        return key


class MockModel:  # pylint: disable=too-few-public-methods
    """
    Dummy model stub to satisfy Controller dependencies.
    """

    def __init__(self):
        pass


def test_get_key_press_returns_character():
    """
    Test that get_key_press returns a key character from input sequence.

    Args:
        None

    Returns:
        None
    """
    stdscr = MockStdscr(["a"])
    model = MockModel()
    controller = Controller(stdscr, model)

    result = controller.get_key_press()
    assert result == "a"


def test_enter_password_collects_until_newline():
    """
    Test that enter_password collects characters until newline ('\\n').

    Args:
        None

    Returns:
        None
    """
    input_sequence = list("secret123") + ["\n"]
    stdscr = MockStdscr(input_sequence)
    model = MockModel()
    controller = Controller(stdscr, model)

    password = controller.enter_password()
    assert password == "secret123"
