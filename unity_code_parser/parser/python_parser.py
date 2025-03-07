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
        class_function_names = set()
        
        # 首先收集所有类方法的名称，以便排除它们
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_function_names.add(item.name)
        
        # 然后收集所有不在类中定义的函数
        for node in ast.iter_child_nodes(self.ast_tree):
            if isinstance(node, ast.FunctionDef) and node.name not in class_function_names:
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
        Extract information from a function node.
        
        Args:
            func_node: The function AST node.
            
        Returns:
            Dict[str, Any]: A dictionary containing information about the function.
        """
        params = []
        
        for arg in func_node.args.args:
            param_info = {
                "name": arg.arg,
                "type": self._get_annotation(arg.annotation)
            }
            params.append(param_info)
            
        return_type = self._get_annotation(func_node.returns)
        
        return {
            "name": func_node.name,
            "params": params,
            "return_type": return_type,
            "docstring": ast.get_docstring(func_node) or ""
        }

    def _get_annotation(self, annotation) -> str:
        """
        Get the string representation of a type annotation.
        
        Args:
            annotation: The annotation AST node.
            
        Returns:
            str: The string representation of the annotation.
        """
        if annotation is None:
            return "Any"
            
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Attribute):
            return f"{self._get_name(annotation.value)}.{annotation.attr}"
        elif isinstance(annotation, ast.Subscript):
            return f"{self._get_name(annotation.value)}[{self._get_name(annotation.slice)}]"
        else:
            return str(annotation)

    def _get_name(self, node) -> str:
        """
        Get the string representation of a name node.
        
        Args:
            node: The name AST node.
            
        Returns:
            str: The string representation of the name.
        """
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[{self._get_name(node.slice)}]"
        else:
            return str(node)

    def _get_value(self, node) -> str:
        """
        Get the string representation of a value node.
        
        Args:
            node: The value AST node.
            
        Returns:
            str: The string representation of the value.
        """
        if isinstance(node, ast.Str):
            return f'"{node.s}"'
        elif isinstance(node, ast.Num):
            return str(node.n)
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
        elif isinstance(node, ast.List):
            elements = [self._get_value(elt) for elt in node.elts]
            return f"[{', '.join(elements)}]"
        elif isinstance(node, ast.Dict):
            keys = [self._get_value(key) for key in node.keys]
            values = [self._get_value(value) for value in node.values]
            items = [f"{k}: {v}" for k, v in zip(keys, values)]
            return f"{{{', '.join(items)}}}"
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            func_name = self._get_name(node.func)
            args = [self._get_value(arg) for arg in node.args]
            return f"{func_name}({', '.join(args)})"
        else:
            return "..."
