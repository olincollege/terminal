import unittest
from unittest.mock import patch, mock_open
from model import Model


class TestModel(unittest.TestCase):

    def setUp(self):
        self.model = Model()

    def test_initial_unlock_status(self):
        # Initially, unlock status should be 1
        self.assertEqual(self.model._unlock_status, 1)

    def test_bookmarking(self):
        dummy_file = "dummy.txt"
        self.model.bookmark(dummy_file)
        self.assertIn(dummy_file, self.model.bookmarks)

    def test_verify_password_unlock_success(self):
        # Assuming password for level 2 is correct
        self.model.verify_password_unlock("vires_in_silentio")
        self.assertEqual(self.model._unlock_status, 2)

    def test_verify_password_unlock_failure(self):
        # Wrong password should not increase unlock status
        self.model.verify_password_unlock("wrong_password")
        self.assertEqual(self.model._unlock_status, 1)

    @patch("os.path.exists", return_value=True)
    @patch(
        "os.listdir",
        return_value=["artifacts_1", "artifacts_2", "not_artifact"],
    )
    @patch("os.path.isdir", return_value=True)
    def test_get_accessible_folders(
        self, mock_isdir, mock_listdir, mock_exists
    ):
        folders = self.model.get_accessible_folders()
        self.assertIn("artifacts_1", folders)
        self.assertIn("artifacts_2", folders)
        self.assertNotIn("not_artifact", folders)

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isdir", return_value=True)
    @patch("os.listdir", return_value=["file1.txt", "file2.txt"])
    def test_get_accessible_contents_unlocked(
        self, mock_listdir, mock_isdir, mock_exists
    ):
        contents = self.model.get_accessible_contents("artifacts_1")
        self.assertEqual(contents, ["file1.txt", "file2.txt"])

    def test_get_accessible_contents_locked(self):
        # Set unlock_status to 1, and try accessing artifacts_3 (locked)
        self.model._unlock_status = 1
        result = self.model.get_accessible_contents("artifacts_3")
        self.assertEqual(result, ["LOCKED"])


if __name__ == "__main__":
    unittest.main()
