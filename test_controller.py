"""
Tests for the Controller class using pytest.

Each test mocks user input via a custom MockStdscr class.
"""

from controller import Controller


class MockStdscr:  # pylint: disable=too-few-public-methods
    """
    Mock curses stdscr to simulate getkey() calls.
    """

    def __init__(self, inputs):
        self.inputs = inputs
        self.index = 0

    def getkey(self):
        """
        Simulate a single key press.

        Returns:
            str: The next input in the sequence.
        """
        if self.index >= len(self.inputs):
            raise IndexError("Ran out of mock inputs")
        key = self.inputs[self.index]
        self.index += 1
        return key


class MockModel:  # pylint: disable=too-few-public-methods
    """
    Mock model class to test Controller.bookmark().
    """

    def __init__(self):
        self.bookmarked = False

    def bookmark(self):
        """
        Simulates bookmarking a file.
        """
        self.bookmarked = True


def test_get_key_press_normal():
    """
    Test that get_key_press returns a regular key.

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
    assert not model.bookmarked


def test_get_key_press_bookmark():
    """
    Test that get_key_press returns '+' and triggers model.bookmark().

    Args:
        None

    Returns:
        None
    """
    stdscr = MockStdscr(["+"])
    model = MockModel()
    controller = Controller(stdscr, model)

    result = controller.get_key_press()
    assert result == "+"
    assert model.bookmarked


def test_enter_password():
    """
    Test that enter_password collects typed characters until newline is entered.

    Args:
        None

    Returns:
        None
    """
    input_sequence = list("vires_in_silentio") + ["\n"]
    stdscr = MockStdscr(input_sequence)
    model = MockModel()
    controller = Controller(stdscr, model)

    expected = "vires_in_silentio"
    password = controller.enter_password()
    assert password == expected
