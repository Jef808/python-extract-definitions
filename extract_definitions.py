#!/usr/bin/env python3
"""Extract and print definitions within a Python module in JSON format.

The output JSON object contains the following fields:
- docs: The docstring of the file.
- classes: A list of class definitions.
- functions: A list of function definitions.

Each class definition includes:
- name: The name of the class.
- docstring: The docstring of the class.
- bases: A list of base classes.
- methods: A list of method definitions.

Each function/method definition includes:
- name: The name of the function/method.
- docstring: The docstring of the function/method.
- content: The source code of the function/method.
"""

import ast
import sys
import json
from typing import List, TypedDict


class FunctionInfo(TypedDict):
    """Represents information about a function or method."""
    name: str
    docstring: str
    content: str


class ClassInfo(TypedDict):
    """Represents information about a class."""
    name: str
    docstring: str
    bases: List[str]
    methods: List[FunctionInfo]


class ModuleInfo(TypedDict):
    """Represents information about a module."""
    docstring: str
    classes: List[ClassInfo]
    functions: List[FunctionInfo]


def extract_function_info(node: ast.FunctionDef,
                          file_content: str) -> FunctionInfo:
    """Extract information from a function definition node.

    Args:
        node (ast.FunctionDef): The AST node representing the function
                                definition.
        file_content (str): The full content of the file.

    Returns:
        FunctionInfo: A dictionary containing the function's name, docstring and
        content.
    """
    return FunctionInfo(
        name=node.name,
        docstring=ast.get_docstring(node),
        content=ast.get_source_segment(file_content, node) or ""
    )


def extract_class_info(node: ast.ClassDef, file_content: str) -> ClassInfo:
    """Extract information from a class definition node.

    Args:
        node (ast.ClassDef): The AST node representing the class definition.
        file_content (str): The full content of the file.

    Returns:
        ClassInfo: A dictionary containing the class's name, docstring,
                   base classes, and methods.
    """
    methods = [extract_function_info(f, file_content)
               for f in node.body if isinstance(f, ast.FunctionDef)]
    return ClassInfo(
        name=node.name,
        docstring=ast.get_docstring(node),
        bases=[base.id for base in node.bases],
        methods=methods
    )


def get_module_info(file_content: str) -> ModuleInfo:
    """
    Extract information from a module's content.

    Args:
        file_content (str): The full content of the file.

    Returns:
        ModuleInfo: A dictionary containing the module's docstring,
                    classes and functions.
    """
    tree = ast.parse(file_content)
    module_docstring = ast.get_docstring(tree)

    functions = [extract_function_info(node, file_content)
                 for node in tree.body if isinstance(node, ast.FunctionDef)]
    classes = [extract_class_info(node, file_content)
               for node in tree.body if isinstance(node, ast.ClassDef)]

    return ModuleInfo(
        docstring=module_docstring,
        classes=classes,
        functions=functions
    )


def main(files: List[str]) -> None:
    """Main function to process the given files and print their data.

    The data is a ModuleInfo object and is printed in JSON format.

    Args:
        files (List[str]): A list of filepaths to process.
    """
    for f in filter(lambda x: x.endswith('.py'), files):
        try:
            with open(f, 'r', encoding="utf-8") as file:
                file_content = file.read()
        except IOError as e:
            print(f"Error reading file {f}: {e}", file=sys.stderr)
            continue
        module_info = get_module_info(file_content)
        print(json.dumps(module_info, indent=2))


if __name__ == '__main__':
    main(sys.argv[1:])
