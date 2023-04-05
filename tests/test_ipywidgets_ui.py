import unittest
from unittest import mock
from unittest.mock import patch, mock_open
from lib.ipywidgets_ui import *

class TestStartingContexts(unittest.TestCase):

    def test_load_starting_contexts(self):
        # Test that the function finds the test files in the temporary directory
        with patch("lib.ipywidgets_ui.glob.glob") as mock_glob:
            with patch("builtins.open", mock_open(read_data="test")) as mock_file:
                mock_glob.return_value = ["file1.txt", "file2.txt"]
                starting_contexts = load_starting_contexts("system_prompts/starting_contexts")
                self.assertEqual(len(starting_contexts), 2)
                mock_glob.assert_called_once_with("system_prompts/starting_contexts/*.txt")
                mock_file.assert_any_call("file1.txt", "r")
                mock_file.assert_any_call("file2.txt", "r")

    def test_generate_system_prompt(self):
        with mock.patch("builtins.open") as mock_open:
            # Set up the mock return value for builtins.open
            mock_open.return_value.__enter__.return_value.read.return_value = "Hello, world!"
            
            # Call the function being tested
            system_prompt = generate_system_prompt("Prompt", "system_prompts/starting_contexts/greeting.txt")
            
            # Check that the function returned the expected value
            self.assertEqual(system_prompt, "Prompt Hello, world!")
