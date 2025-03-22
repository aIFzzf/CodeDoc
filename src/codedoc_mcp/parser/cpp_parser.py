#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C++ code parser module.
This module provides functionality to parse C++ code files.
"""

import re
from typing import Dict, List, Any, Optional
from .base_parser import BaseParser


class CppParser(BaseParser):
    """
    Parser for C++ code files.
    Extracts classes, methods, properties, and functions from C++ code files.
    """

    def __init__(self, file_path: str):
        """
        Initialize the C++ parser with a file path.

        Args:
            file_path: Path to the C++ file to parse.
        """
        super().__init__(file_path)
        # Regex patterns for C++ parsing
        self.class_pattern = r"(?:class|struct)\s+(\w+)(?:\s*:\s*(?:public|protected|private)\s+([^{]+))?\s*\{"
        self.method_pattern = r"(?:virtual\s+)?(?:static\s+)?(?:inline\s+)?(?:explicit\s+)?(?:const\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*\(([^)]*)\)(?:\s*const)?\s*(?:=\s*0)?\s*(?:override)?\s*(?:final)?\s*(?:noexcept)?\s*(?:;\s*|\{)"
        self.property_pattern = r"(?:public|protected|private):\s*(?:static\s+)?(?:const\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)(?:\s*=\s*[^;]+)?;"
        self.function_pattern = r"(?:static\s+)?(?:inline\s+)?(?:explicit\s+)?(?:const\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*\(([^)]*)\)(?:\s*const)?\s*(?:noexcept)?\s*(?:;\s*|\{)"
        self.namespace_pattern = r"namespace\s+(\w+)\s*\{"
        self.include_pattern = r"#include\s+[<\"]([^>\"]+)[>\"]"

    def parse(self) -> Dict[str, Any]:
        """
        Parse the C++ code file and extract structured information.
        
        Returns:
            Dict[str, Any]: A dictionary containing structured information about the C++ code.
        """
        return {
            "language": "C++",
            "classes": self.get_classes(),
            "methods": self.get_methods(),
            "properties": self.get_properties(),
            "functions": self.get_functions(),
            "namespaces": self.get_namespaces(),
            "includes": self.get_includes()
        }

    def get_classes(self) -> List[Dict[str, Any]]:
        """
        Extract classes information from the C++ code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a class.
        """
        classes = []
        
        for match in re.finditer(self.class_pattern, self.content):
            class_name = match.group(1)
            base_classes_str = match.group(2) if match.group(2) else ""
            
            # Parse base classes
            base_classes = []
            if base_classes_str:
                # Split by commas, but be careful of template parameters which might contain commas
                current = ""
                bracket_count = 0
                
                for char in base_classes_str:
                    if char == '<':
                        bracket_count += 1
                        current += char
                    elif char == '>':
                        bracket_count -= 1
                        current += char
                    elif char == ',' and bracket_count == 0:
                        base_classes.append(current.strip())
                        current = ""
                    else:
                        current += char
                
                if current:
                    base_classes.append(current.strip())
            
            # Find the class body
            class_start = self.content.find('{', match.end())
            if class_start > 0:
                # Find the matching closing brace
                brace_count = 1
                class_end = class_start + 1
                while brace_count > 0 and class_end < len(self.content):
                    if self.content[class_end] == '{':
                        brace_count += 1
                    elif self.content[class_end] == '}':
                        brace_count -= 1
                    class_end += 1
                
                class_content = self.content[class_start:class_end]
                
                class_info = {
                    "name": class_name,
                    "base_classes": base_classes,
                    "methods": self._extract_class_methods(class_content),
                    "properties": self._extract_class_properties(class_content)
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
        Extract all properties from all classes.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a property.
        """
        all_properties = []
        
        for class_info in self.get_classes():
            for prop in class_info.get("properties", []):
                prop["class"] = class_info["name"]
                all_properties.append(prop)
                
        return all_properties

    def get_functions(self) -> List[Dict[str, Any]]:
        """
        Extract global functions from the C++ code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a function.
        """
        functions = []
        
        for match in re.finditer(self.function_pattern, self.content):
            return_type = match.group(1)
            function_name = match.group(2)
            parameters_str = match.group(3)
            
            # Skip if this is a method of a class (we handle those separately)
            class_pattern = r"class\s+\w+\s*\{[^}]*" + function_name + r"\s*\("
            if re.search(class_pattern, self.content):
                continue
            
            # Parse parameters
            parameters = self._parse_parameters(parameters_str)
            
            function_info = {
                "name": function_name,
                "return_type": return_type,
                "parameters": parameters
            }
            
            functions.append(function_info)
            
        return functions

    def get_namespaces(self) -> List[Dict[str, Any]]:
        """
        Extract namespaces from the C++ code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a namespace.
        """
        namespaces = []
        
        for match in re.finditer(self.namespace_pattern, self.content):
            namespace_name = match.group(1)
            
            namespace_info = {
                "name": namespace_name
            }
            
            namespaces.append(namespace_info)
            
        return namespaces

    def get_includes(self) -> List[str]:
        """
        Extract include statements from the C++ code.
        
        Returns:
            List[str]: A list of include files.
        """
        includes = []
        
        for match in re.finditer(self.include_pattern, self.content):
            include_file = match.group(1)
            includes.append(include_file)
            
        return includes

    def _extract_class_methods(self, class_content: str) -> List[Dict[str, Any]]:
        """
        Extract methods from a class content.
        
        Args:
            class_content: The content of the class.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a method.
        """
        methods = []
        
        for match in re.finditer(self.method_pattern, class_content):
            return_type = match.group(1)
            method_name = match.group(2)
            parameters_str = match.group(3)
            
            # Parse parameters
            parameters = self._parse_parameters(parameters_str)
            
            method_info = {
                "name": method_name,
                "return_type": return_type,
                "parameters": parameters
            }
            
            methods.append(method_info)
            
        return methods

    def _extract_class_properties(self, class_content: str) -> List[Dict[str, Any]]:
        """
        Extract properties from a class content.
        
        Args:
            class_content: The content of the class.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a property.
        """
        properties = []
        
        # Regular expression for C++ class properties
        for match in re.finditer(self.property_pattern, class_content):
            property_type = match.group(1)
            property_name = match.group(2)
            
            property_info = {
                "name": property_name,
                "type": property_type
            }
            
            properties.append(property_info)
            
        return properties

    def _parse_parameters(self, parameters_str: str) -> List[Dict[str, str]]:
        """
        Parse a parameter string into a list of parameter dictionaries.
        
        Args:
            parameters_str: The parameter string to parse.
            
        Returns:
            List[Dict[str, str]]: A list of dictionaries, each containing information about a parameter.
        """
        parameters = []
        
        if parameters_str.strip():
            # Split by commas, but be careful of template parameters which might contain commas
            current = ""
            bracket_count = 0
            
            for char in parameters_str:
                if char == '<':
                    bracket_count += 1
                    current += char
                elif char == '>':
                    bracket_count -= 1
                    current += char
                elif char == ',' and bracket_count == 0:
                    parameters.append(self._parse_single_parameter(current.strip()))
                    current = ""
                else:
                    current += char
            
            if current:
                parameters.append(self._parse_single_parameter(current.strip()))
                
        return parameters

    def _parse_single_parameter(self, param_str: str) -> Dict[str, str]:
        """
        Parse a single parameter string into a parameter dictionary.
        
        Args:
            param_str: The parameter string to parse.
            
        Returns:
            Dict[str, str]: A dictionary containing information about the parameter.
        """
        # Handle default parameters
        param_parts = param_str.split('=')
        param_no_default = param_parts[0].strip()
        param_default = param_parts[1].strip() if len(param_parts) > 1 else None
        
        # Split type and name
        parts = param_no_default.split()
        
        if len(parts) == 1:
            # This might be just a type with no name
            param_type = parts[0]
            param_name = ""
        else:
            # The last part is the name, everything else is the type
            param_name = parts[-1]
            param_type = ' '.join(parts[:-1])
            
            # Handle pointer/reference in the name
            if param_name.startswith('*') or param_name.startswith('&'):
                param_type += ' ' + param_name[0]
                param_name = param_name[1:]
        
        param_info = {
            "name": param_name,
            "type": param_type
        }
        
        if param_default:
            param_info["default"] = param_default
            
        return param_info
