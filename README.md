# OpenAI Chatbot Project

This project demonstrates the use of OpenAI API's chat feature to power an ongoing chatbot UI built with ipywidgets in a Jupyter notebook. It maintains a separate system prompt for defining the context of the conversation that the end user has using the widgets in the notebook.

## Getting Started

1. Clone this repository.
2. Add your OpenAI API key to `config/openai_api_key.txt`. (Or `~/.openai/api_key.txt`)
3. Run the `chat_ui.ipynb` notebook.

The notebook includes its own documentation explaining what each cell does.

## Running the `chat_ui.ipynb` Notebook

Options for running the `chat_ui.ipynb` notebook, include the command-line interface or an integrated development environment (IDE) like Visual Studio Code (VS Code).

### Command-line way:

1. Open a terminal or command prompt and navigate to the `notebooks` directory containing the `chat_ui.ipynb` notebook.
2. Activate your Python environment if necessary.
3. Start Jupyter Notebook by running the command `jupyter notebook`.
4. This will open Jupyter Notebook in your default web browser. Click on the `chat_ui.ipynb` notebook to open it.
5. In the notebook, click on the "Run" button or use the keyboard shortcut `Shift + Enter` to execute each cell of code.

### VS Code way:

1. Open VS Code and navigate to the `notebooks` directory containing the `chat_ui.ipynb` notebook.
2. Open the `chat_ui.ipynb` notebook in VS Code.
3. If you haven't already, install the Jupyter extension for VS Code.
4. Click on the "Run Cell" button or use the keyboard shortcut `Shift + Enter` to execute each cell of code in the notebook.

Note that to run the `chat_ui.ipynb` notebook, you'll need to have all the necessary dependencies and packages installed, and any required data files should be in the correct directory. You may also need to activate your Python environment if you're using a virtual environment.

# Development

## Running tests

The Jupyter notebook will run the tests for each code file it loads from `lib/`, but if you're doing development then you can run the tests manually.

### Running Tests from the Command Line

To run tests from the command line using `unittest`, follow these steps:

1. Navigate to the root directory of your project in the terminal.
2. Activate your Python environment if necessary.
3. To run all the tests in the project, use the following command:

    ```
    python -m unittest discover -s tests -p 'test*.py'
    ```

    This command tells `unittest` to search the `tests` directory for all files ending in `_test.py` and run all the tests in those files. You can adjust the `-p` option to match the naming convention of your test files.

4. To run a single test file, use the following command:

    ```
    python -m unittest tests.test_load_openai_key
    ```

    This command tells `unittest` to run the tests in the `tests/test_load_openai_key.py` file.

5. To run a specific test method in a test file, use the following command:

    ```
    python -m unittest tests.test_load_openai_key.TestLoadOpenAIKey.test_load_key_from_config_directory
    ```

    This command tells `unittest` to run the `test_load_key_from_config_directory()` method in the `TestLoadOpenAIKey` class in the `tests/test_load_openai_key.py` file.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.