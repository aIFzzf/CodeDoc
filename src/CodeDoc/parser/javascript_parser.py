#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript code parser module.
This module provides functionality to parse JavaScript code files.
"""

import re
from typing import Dict, List, Any, Optional
from .base_parser import BaseParser


class JavaScriptParser(BaseParser):
    """
    Parser for JavaScript code files.
    Extracts classes, methods, properties, and functions from JavaScript code files.
    """

    def __init__(self, file_path: str):
        """
        Initialize the JavaScript parser with a file path.

        Args:
            file_path: Path to the JavaScript file to parse.
        """
        super().__init__(file_path)
        # Regex patterns for JavaScript parsing
        self.class_pattern = r"class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{"
        self.method_pattern = r"(?:async\s+)?(?:function\s+)?(\w+)\s*\(([^)]*)\)\s*\{"
        self.property_pattern = r"this\.(\w+)\s*=\s*([^;]+);"
        self.function_pattern = r"(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)\s*\{"
        self.arrow_function_pattern = r"(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)\s*=>\s*[{]?"
        self.import_pattern = r"import\s+(?:{([^}]+)}|([^{][^;]+))\s+from\s+['\"]([^'\"]+)['\"]"

    def parse(self) -> Dict[str, Any]:
        """
        Parse the JavaScript code file and extract structured information.
        
        Returns:
            Dict[str, Any]: A dictionary containing structured information about the JavaScript code.
        """
        return {
            "language": "JavaScript",
            "classes": self.get_classes(),
            "methods": self.get_methods(),
            "properties": self.get_properties(),
            "functions": self.get_functions(),
            "imports": self.get_imports()
        }

    def get_classes(self) -> List[Dict[str, Any]]:
        """
        Extract classes information from the JavaScript code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a class.
        """
        classes = []
        
        for match in re.finditer(self.class_pattern, self.content):
            class_name = match.group(1)
            parent_class = match.group(2) if match.group(2) else ""
            
            # Find the class body
            class_start = self.content.find('{', match.end() - 1) + 1
            if class_start > 0:
                # Find the matching closing brace
                brace_count = 1
                class_end = class_start
                while brace_count > 0 and class_end < len(self.content):
                    if self.content[class_end] == '{':
                        brace_count += 1
                    elif self.content[class_end] == '}':
                        brace_count -= 1
                    class_end += 1
                
                class_body = self.content[class_start:class_end-1]
                
                class_info = {
                    "name": class_name,
                    "parent": parent_class,
                    "methods": self._extract_class_methods(class_body),
                    "properties": self._extract_class_properties(class_body)
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
        Extract global functions from the JavaScript code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a function.
        """
        functions = []
        
        # Regular functions
        for match in re.finditer(self.function_pattern, self.content):
            function_name = match.group(1)
            parameters_str = match.group(2)
            
            # Parse parameters
            parameters = self._parse_parameters(parameters_str)
            
            function_info = {
                "name": function_name,
                "parameters": parameters,
                "type": "function"
            }
            
            functions.append(function_info)
            
        # Arrow functions
        for match in re.finditer(self.arrow_function_pattern, self.content):
            function_name = match.group(1)
            parameters_str = match.group(2)
            
            # Parse parameters
            parameters = self._parse_parameters(parameters_str)
            
            function_info = {
                "name": function_name,
                "parameters": parameters,
                "type": "arrow_function"
            }
            
            functions.append(function_info)
            
        return functions

    def get_imports(self) -> List[Dict[str, Any]]:
        """
        Extract import statements from the JavaScript code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about an import.
        """
        imports = []
        
        for match in re.finditer(self.import_pattern, self.content):
            named_imports = match.group(1)
            default_import = match.group(2)
            module_path = match.group(3)
            
            import_info = {
                "module": module_path
            }
            
            if named_imports:
                import_info["type"] = "named"
                import_info["imports"] = [name.strip() for name in named_imports.split(',')]
            elif default_import:
                import_info["type"] = "default"
                import_info["import"] = default_import.strip()
            
            imports.append(import_info)
            
        return imports

    def _extract_class_methods(self, class_body: str) -> List[Dict[str, Any]]:
        """
        Extract methods from a class body.
        
        Args:
            class_body: The body of the class.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a method.
        """
        methods = []
        
        # Class method pattern for ES6 classes
        class_method_pattern = r"(?:async\s+)?(\w+)\s*\(([^)]*)\)\s*\{"
        
        for match in re.finditer(class_method_pattern, class_body):
            method_name = match.group(1)
            parameters_str = match.group(2)
            
            # Parse parameters
            parameters = self._parse_parameters(parameters_str)
            
            method_info = {
                "name": method_name,
                "parameters": parameters
            }
            
            methods.append(method_info)
            
        return methods

    def _extract_class_properties(self, class_body: str) -> List[Dict[str, Any]]:
        """
        Extract properties from a class body.
        
        Args:
            class_body: The body of the class.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a property.
        """
        properties = []
        
        # Look for constructor
        constructor_pattern = r"constructor\s*\(([^)]*)\)\s*\{([^}]+)}"
        constructor_match = re.search(constructor_pattern, class_body, re.DOTALL)
        
        if constructor_match:
            constructor_body = constructor_match.group(2)
            
            # Extract properties initialized in constructor
            for match in re.finditer(self.property_pattern, constructor_body):
                prop_name = match.group(1)
                prop_value = match.group(2)
                
                property_info = {
                    "name": prop_name,
                    "value": prop_value.strip()
                }
                
                properties.append(property_info)
                
        # Look for class fields (a more modern JavaScript feature)
        field_pattern = r"(\w+)\s*=\s*([^;]+);"
        
        for match in re.finditer(field_pattern, class_body):
            field_name = match.group(1)
            field_value = match.group(2)
            
            # Skip if the field name is a method we've already extracted
            if any(method["name"] == field_name for method in self._extract_class_methods(class_body)):
                continue
                
            property_info = {
                "name": field_name,
                "value": field_value.strip()
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
            for param in parameters_str.split(','):
                param = param.strip()
                if param:
                    # Handle default parameters
                    param_parts = param.split('=')
                    param_name = param_parts[0].strip()
                    param_default = param_parts[1].strip() if len(param_parts) > 1 else None
                    
                    # Handle destructuring
                    if param_name.startswith('{') or param_name.startswith('['):
                        param_name = "destructured"
                    
                    param_info = {
                        "name": param_name
                    }
                    
                    if param_default:
                        param_info["default"] = param_default
                        
                    parameters.append(param_info)
                    
        return parameters
