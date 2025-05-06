"""
Unit tests for the updated Model class using unittest.

Covers bookmarking, unlock logic, folder accessibility, and content visibility.
"""

import unittest
from unittest.mock import patch
from model import Model


class TestModel(unittest.TestCase):
    """
    A unittest.TestCase subclass for testing the Model class.

    Verifies:
    - Initial state
    - Password storage
    - Unlock level behavior
    - Bookmarking functionality
    - Folder and content access logic
    """

    def setUp(self):
        """Initialize a fresh model for each test."""
        self.model = Model()

    def test_initial_state(self):
        """Test initial unlock level, passwords, and bookmarks."""
        self.assertEqual(self.model.unlock_level, 1)
        self.assertEqual(self.model.bookmarks, [])
        self.assertEqual(
            self.model.passwords, {2: "vires_in_silentio", 3: "CENTENIEL-1"}
        )

    def test_bookmarking(self):
        """Test that bookmarking a file adds it to the list."""
        dummy_file = "test.txt"
        self.model.bookmark(dummy_file)
        self.assertIn(dummy_file, self.model.bookmarks)

    def test_increase_level(self):
        """Test that unlock level increases correctly."""
        self.model.increase_level()
        self.assertEqual(self.model.unlock_level, 2)
        self.model.increase_level()
        self.assertEqual(self.model.unlock_level, 3)

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isdir", return_value=True)
    @patch(
        "os.listdir",
        return_value=["artifacts_1", "artifacts_2", "notes", "not_a_folder"],
    )
    def test_get_accessible_folders(self, *_):
        """Test that only folders starting with 'artifacts_' are returned."""
        folders = self.model.get_accessible_folders()
        self.assertIn("artifacts_1", folders)
        self.assertIn("artifacts_2", folders)
        self.assertNotIn("notes", folders)
        self.assertNotIn("not_a_folder", folders)

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isdir", return_value=True)
    @patch("os.listdir", return_value=["file1.txt", "file2.txt"])
    def test_get_accessible_contents_unlocked(self, *_):
        """Test that contents are returned if folder is unlocked."""
        contents = self.model.get_accessible_contents("artifacts_1")
        self.assertEqual(contents, ["file1.txt", "file2.txt"])

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isdir", return_value=True)
    def test_get_accessible_contents_locked(self, *_):
        """Test that 'LOCKED' is returned if above unlock level."""
        self.model.set_unlock_level(1)

        result = self.model.get_accessible_contents("artifacts_3")
        self.assertEqual(result, ["LOCKED"])


if __name__ == "__main__":
    unittest.main()
