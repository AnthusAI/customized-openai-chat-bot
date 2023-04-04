import unittest
from unittest.mock import mock_open, patch
from lib.load_openai_api_key import load_openai_api_key
import os
from unittest.mock import ANY

class TestLoadApiKey(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="abcd-1234-efgh-5678-abcd-1234-efgh-5678-abcd-1234-abcd-12")
    @patch("os.path.exists", return_value=True)
    def test_load_from_config_file(self, mock_exists, mock_file):
        key = load_openai_api_key()
        self.assertEqual(key, "abcd-1234-efgh-5678-abcd-1234-efgh-5678-abcd-1234-abcd-12")

        # Get the actual file path from the mock_file call arguments
        actual_path, _ = mock_file.call_args[0]

        # Check if the actual path ends with the expected relative path
        self.assertTrue(actual_path.endswith("config/api_key.txt"))

    @patch("builtins.open", new_callable=mock_open, read_data="xyz-9876-uvw-5432-xyz-9876-uvw-5432-xyz-9876-xyz-98")
    @patch("os.path.exists")
    def test_load_from_home_dir(self, mock_exists, mock_file):
        fallback_path = os.path.expanduser("~/.openai/api_key.txt")
        mock_exists.side_effect = lambda x: x == fallback_path
        key = load_openai_api_key()
        self.assertEqual(key, "xyz-9876-uvw-5432-xyz-9876-uvw-5432-xyz-9876-xyz-98")
        mock_file.assert_any_call(fallback_path, "r")

    @patch("builtins.open", new_callable=mock_open, read_data="a1b2c3d4e5-fg")
    @patch("os.path.exists", return_value=True)  # Mock os.path.exists
    def test_invalid_key(self, mock_exists, mock_file):
        with self.assertRaises(ValueError):
            load_openai_api_key()

    @patch("builtins.open", new_callable=mock_open, read_data="x" * 49)
    @patch("os.path.exists", return_value=True)  # Mock os.path.exists
    def test_key_too_short(self, mock_exists, mock_file):
        with self.assertRaises(ValueError):
            load_openai_api_key()

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("os.path.exists", return_value=False)  # Mock os.path.exists
    def test_key_not_found(self, mock_exists, mock_file):
        with self.assertRaises(FileNotFoundError):  # Update the expected exception
            load_openai_api_key()