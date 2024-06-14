#!/usr/bin/env python3

"""A simple script to extract the definitions within a python file.

The output is JSON formatted object containing the following fields:
- docs: The docstring of the file.
- classes: A list of class definitions.
- functions: A list of function definitions.

The class and function definitions are themselves objects containing
the following fields:
- name: The name of the class or function
- docstring: The docstring of the class or function
- content: The content of the class or function
"""

import ast
import sys
import json
from typing import List, TypedDict


class FunctionInfo(TypedDict):
    """Information of a definition."""
    name: str
    docstring: str
    content: str


class ClassInfo(TypedDict):
    """Information of a class."""
    name: str
    docstring: str
    bases: List[str]
    methods: List[FunctionInfo]


class ModuleInfo(TypedDict):
    """Information of a file."""
    docs: str
    classes: List[ClassInfo]
    functions: List[FunctionInfo]


def get_function_info(node: ast.FunctionDef, file_content) -> FunctionInfo:
    """Get the information of the function."""
    fname = node.name
    fdoc = ast.get_docstring(node)
    fcontent = ast.get_source_segment(file_content, node)
    return FunctionInfo(name=fname, docstring=fdoc, content=fcontent)


def get_module_info(file_content) -> ModuleInfo:
    """Get the information of the file."""

    tree = ast.parse(file_content)
    stmts = tree.body

    if isinstance(stmts[0], ast.Expr):
        file_docstring = stmts[0].value.value
    else:
        file_docstring = None

    result = ModuleInfo(docs=file_docstring, classes=[], functions=[])

    functions = [node for node in stmts if isinstance(node, ast.FunctionDef)]
    for f in functions:
        result['functions'].append(get_function_info(f, file_content))

    classes = [node for node in stmts if isinstance(node, ast.ClassDef)]
    for c in classes:
        cname = c.name
        cdoc = ast.get_docstring(c)
        cbases = [base.id for base in c.bases]
        result['classes'].append(ClassInfo(name=cname, docstring=cdoc, bases=cbases, methods=[]))
        methods = [node for node in c.body if isinstance(node, ast.FunctionDef)]
        for f in methods:
            result['classes'][-1]['methods'].append(get_function_info(f, file_content))

    return result


if __name__ == '__main__':
    filenames = sys.argv[1:]
    for f in filter(lambda x: x.endswith('.py'), filenames):
        with open(f, 'r', encoding="utf-8") as _f:
            info = get_module_info(_f.read())
            print(json.dumps(info, indent=2))
