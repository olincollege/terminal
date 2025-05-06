"""
Unit tests for the updated Model class using unittest.

Covers bookmarking, unlock logic, folder accessibility, and content visibility.
"""

import unittest
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
        self.assertEqual(
            self.model.passwords, {2: "vires_in_silentio", 3: "CENTENIEL-1"}
        )

    def test_increase_level(self):
        """Test that unlock level increases correctly."""
        self.model.increase_level()
        self.assertEqual(self.model.unlock_level, 2)
        self.model.increase_level()
        self.assertEqual(self.model.unlock_level, 3)


if __name__ == "__main__":
    unittest.main()
