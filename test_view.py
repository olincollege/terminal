"""
Unit tests for the View class from view.py.

These tests cover display logic for file lists and path formatting.
"""

import unittest
from unittest.mock import MagicMock
from view import View
from model import Directory, TextFile


class DummyFile:
    """
    Minimal stub for a File object used in current_path_to_string() testing.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def describe(self):
        """
        Dummy method to satisfy pylint's minimum method count.
        """
        return f"DummyFile: {self.name}"


class TestView(unittest.TestCase):
    """
    Test suite for the View class.
    """

    def setUp(self):
        """
        Create a View object with mocked stdscr, model, and controller.
        """
        self.mock_stdscr = MagicMock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)
        self.mock_controller = MagicMock()
        self.mock_model = MagicMock()
        self.view = View(
            self.mock_stdscr, self.mock_controller, self.mock_model
        )

    def test_current_path_to_string(self):
        """
        Test path-to-string conversion from a list of File-like objects.
        """
        path = [DummyFile("root"), DummyFile("subdir"), DummyFile("file.txt")]
        result = self.view.current_path_to_string(path)
        self.assertEqual(result, "/root/subdir/file.txt")

    def test_display_file_list_locked_directory(self):
        """
        Test that locked directories are displayed as '[LOCKED]'.
        """
        mock_dir = MagicMock(spec=Directory)
        mock_dir.lock_level = 2
        mock_dir.name = "secret"
        self.mock_model.unlock_level = 1
        self.view.display_file_list([mock_dir], "Header")
        self.mock_stdscr.addstr.assert_any_call(2, 0, "1. [LOCKED]")

    def test_display_file_list_unlocked_directory(self):
        """
        Test that unlocked directories show with a trailing slash.
        """
        mock_dir = MagicMock(spec=Directory)
        mock_dir.lock_level = 1
        mock_dir.name = "public"
        self.mock_model.unlock_level = 2
        self.view.display_file_list([mock_dir], "Header")
        self.mock_stdscr.addstr.assert_any_call(2, 0, "1. public/")

    def test_display_file_list_text_file(self):
        """
        Test that text files are displayed as plain file names.
        """
        mock_file = MagicMock(spec=TextFile)
        mock_file.name = "notes.txt"
        self.view.display_file_list([mock_file], "Header")
        self.mock_stdscr.addstr.assert_any_call(2, 0, "1. notes.txt")


if __name__ == "__main__":
    unittest.main()
