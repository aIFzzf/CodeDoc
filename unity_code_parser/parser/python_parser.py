#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python code parser module.
This module provides functionality to parse Python code files.
"""

import ast
from typing import Dict, List, Any, Optional
from .base_parser import BaseParser


class PythonParser(BaseParser):
    """
    Parser for Python code files.
    Extracts classes, methods, functions, and variables from Python code files.
    """

    def __init__(self, file_path: str):
        """
        Initialize the Python parser with a file path.

        Args:
            file_path: Path to the Python file to parse.
        """
        super().__init__(file_path)
        self.ast_tree = None
        try:
            self.ast_tree = ast.parse(self.content)
        except SyntaxError as e:
            print(f"Error parsing Python file {self.file_path}: {str(e)}")

    def parse(self) -> Dict[str, Any]:
        """
        Parse the Python code file and extract structured information.
        
        Returns:
            Dict[str, Any]: A dictionary containing structured information about the Python code.
        """
        if not self.ast_tree:
            return {
                "language": "Python",
                "error": "Failed to parse the Python file"
            }
            
        return {
            "language": "Python",
            "imports": self.get_imports(),
            "classes": self.get_classes(),
            "functions": self.get_functions(),
            "globals": self.get_globals()
        }

    def get_classes(self) -> List[Dict[str, Any]]:
        """
        Extract classes information from the Python code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a class.
        """
        if not self.ast_tree:
            return []
            
        classes = []
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "bases": [self._get_name(base) for base in node.bases],
                    "methods": self._get_class_methods(node),
                    "attributes": self._get_class_attributes(node),
                    "docstring": ast.get_docstring(node) or ""
                }
                
                classes.append(class_info)
                
        return classes

    def get_methods(self) -> List[Dict[str, Any]]:
        """
        Extract all methods from all classes.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a method.
        """
        all_methods = []
        
        for class_info in self.get_classes():
            for method in class_info.get("methods", []):
                method["class"] = class_info["name"]
                all_methods.append(method)
                
        return all_methods

    def get_properties(self) -> List[Dict[str, Any]]:
        """
        Extract properties (class attributes) information from the Python code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a property.
        """
        all_properties = []
        
        for class_info in self.get_classes():
            for attr in class_info.get("attributes", []):
                attr["class"] = class_info["name"]
                all_properties.append(attr)
                
        return all_properties

    def get_functions(self) -> List[Dict[str, Any]]:
        """
        Extract global functions from the Python code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a function.
        """
        if not self.ast_tree:
            return []
            
        functions = []
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef) and node.parent_field != "body":  # Exclude class methods
                function_info = self._extract_function_info(node)
                functions.append(function_info)
                
        return functions

    def get_imports(self) -> List[Dict[str, Any]]:
        """
        Extract import statements from the Python code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about an import.
        """
        if not self.ast_tree:
            return []
            
        imports = []
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    import_info = {
                        "type": "import",
                        "name": name.name,
                        "alias": name.asname
                    }
                    imports.append(import_info)
                    
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for name in node.names:
                    import_info = {
                        "type": "from_import",
                        "module": module,
                        "name": name.name,
                        "alias": name.asname
                    }
                    imports.append(import_info)
                    
        return imports

    def get_globals(self) -> List[Dict[str, Any]]:
        """
        Extract global variables from the Python code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a global variable.
        """
        if not self.ast_tree:
            return []
            
        globals_list = []
        
        for node in ast.iter_child_nodes(self.ast_tree):
            if isinstance(node, ast.Assign) and not isinstance(node.targets[0], ast.Attribute):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        global_info = {
                            "name": target.id,
                            "value": self._get_value(node.value)
                        }
                        globals_list.append(global_info)
                        
        return globals_list

    def _get_class_methods(self, class_node: ast.ClassDef) -> List[Dict[str, Any]]:
        """
        Extract methods from a class.
        
        Args:
            class_node: The class AST node.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a method.
        """
        methods = []
        
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                method_info = self._extract_function_info(node)
                methods.append(method_info)
                
        return methods

    def _get_class_attributes(self, class_node: ast.ClassDef) -> List[Dict[str, Any]]:
        """
        Extract attributes from a class.
        
        Args:
            class_node: The class AST node.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about an attribute.
        """
        attributes = []
        
        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        attr_info = {
                            "name": target.id,
                            "value": self._get_value(node.value)
                        }
                        attributes.append(attr_info)
                        
        return attributes

    def _extract_function_info(self, func_node: ast.FunctionDef) -> Dict[str, Any]:
        """
        Extract information about a function.
        
        Args:
            func_node: The function AST node.
            
        Returns:
            Dict[str, Any]: A dictionary containing information about the function.
        """
        # Extract return type annotation if available
        returns = ""
        if func_node.returns:
            returns = self._get_name(func_node.returns)
            
        # Extract parameters
        parameters = []
        
        for arg in func_node.args.args:
            param_info = {
                "name": arg.arg,
                "type": self._get_name(arg.annotation) if arg.annotation else ""
            }
            parameters.append(param_info)
            
        # Extract docstring
        docstring = ast.get_docstring(func_node) or ""
        
        return {
            "name": func_node.name,
            "parameters": parameters,
            "returns": returns,
            "docstring": docstring
        }

    def _get_name(self, node: ast.AST) -> str:
        """
        Get the name of an AST node.
        
        Args:
            node: The AST node.
            
        Returns:
            str: The name of the node.
        """
        if node is None:
            return ""
            
        if isinstance(node, ast.Name):
            return node.id
            
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
            
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[{self._get_name(node.slice)}]"
            
        elif isinstance(node, ast.Call):
            return f"{self._get_name(node.func)}(...)"
            
        elif isinstance(node, ast.Str):
            return f'"{node.s}"'
            
        elif isinstance(node, ast.Num):
            return str(node.n)
            
        elif isinstance(node, ast.List):
            return "[...]"
            
        elif isinstance(node, ast.Dict):
            return "{...}"
            
        elif isinstance(node, ast.NameConstant):
            return str(node.value)
            
        else:
            return str(type(node).__name__)

    def _get_value(self, node: ast.AST) -> str:
        """
        Get a string representation of a value.
        
        Args:
            node: The AST node representing a value.
            
        Returns:
            str: A string representation of the value.
        """
        return self._get_name(node)
