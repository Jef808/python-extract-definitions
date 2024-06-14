This script extracts and prints definitions within a Python module in
JSON format. It provides detailed information about the module's
docstring, classes, and functions, including their docstrings and source
code.

### Features

- Extracts the module-level docstring.
- Lists all class definitions, including their base classes, docstrings,
  and methods.
- Lists all function definitions, including their docstrings and source
  code.
- Outputs the extracted information in a structured JSON format.

### Dependencies

This script only uses built-in Python 3 features.

### Usage

1.  **Clone the repository:**

    ``` bash
    git clone https://github.com/yourusername/python-module-extractor.git
    cd python-module-extractor
    ```

2.  **Run the script:**

    ``` bash
    ./extract_definitions.py <file1.py> <file2.py> ...
    ```

    Replace `<file1.py> <file2.py> ...` with the paths to the Python
    files you want to process. The script will print the extracted
    information in JSON format.

### Example

Given a Python file `example.py` with the following content:

``` python
"""
This is an example module.
"""

class ExampleClass:
    """This is an example class."""

    def example_method(self):
        """This is an example method."""
        pass

def example_function():
    """This is an example function."""
    pass
```

Running the script:

``` bash
./extract_definitions.py example.py
```

Will produce the following JSON output:

``` json
{
  "docstring": "This is an example module.",
  "classes": [
    {
      "name": "ExampleClass",
      "docstring": "This is an example class.",
      "bases": [],
      "methods": [
        {
          "name": "example_method",
          "docstring": "This is an example method.",
          "content": "def example_method(self):\n    \"\"\"This is an example method.\"\"\"\n    pass"
        }
      ]
    }
  ],
  "functions": [
    {
      "name": "example_function",
      "docstring": "This is an example function.",
      "content": "def example_function():\n    \"\"\"This is an example function.\"\"\"\n    pass"
    }
  ]
}
```

### Contributing

Contributions are welcome! Please open an issue or submit a pull request
if you have any improvements or bug fixes.

### License

This project is licensed under the MIT License. See the
[file:LICENSE](LICENSE) file for details.

### Contact

For any questions or suggestions, feel free to open an issue or contact
the repository owner.
