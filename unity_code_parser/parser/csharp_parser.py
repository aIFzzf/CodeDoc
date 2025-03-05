#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# code parser module.
This module provides functionality to parse C# code files, specifically Unity C# scripts.
"""

import re
from typing import Dict, List, Any, Optional
from .base_parser import BaseParser


class CSharpParser(BaseParser):
    """
    Parser for C# code files.
    Extracts classes, methods, properties, and fields from C# code files.
    """

    def __init__(self, file_path: str):
        """
        Initialize the C# parser with a file path.

        Args:
            file_path: Path to the C# file to parse.
        """
        super().__init__(file_path)
        self.class_pattern = r"(?:public|private|protected|internal)?\s+(?:class|struct|interface)\s+(\w+)(?:\s*:\s*([^{]+))?"
        self.method_pattern = r"(?:public|private|protected|internal)?\s+(?:virtual|override|abstract|static)?\s+(\w+(?:<[^>]+>)?)\s+(\w+)\s*\(([^)]*)\)"
        self.property_pattern = r"(?:public|private|protected|internal)?\s+(?:virtual|override|abstract|static)?\s+(\w+(?:<[^>]+>)?)\s+(\w+)\s*\{(?:\s*get\s*;\s*set\s*;|\s*get\s*;\s*|\s*set\s*;\s*|\s*[^}]+)\}"
        self.field_pattern = r"(?:public|private|protected|internal)?\s+(?:readonly|static|const)?\s+(\w+(?:<[^>]+>)?)\s+(\w+)\s*=?[^;]*;"

    def parse(self) -> Dict[str, Any]:
        """
        Parse the C# code file and extract structured information.
        
        Returns:
            Dict[str, Any]: A dictionary containing structured information about the C# code.
        """
        return {
            "language": "C#",
            "classes": self.get_classes(),
            "methods": self.get_methods(),
            "properties": self.get_properties(),
            "fields": self.get_fields(),
            "namespaces": self.get_namespaces(),
            "using_directives": self.get_using_directives()
        }

    def get_classes(self) -> List[Dict[str, Any]]:
        """
        Extract classes information from the C# code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a class.
        """
        classes = []
        for match in re.finditer(self.class_pattern, self.content):
            class_name = match.group(1)
            base_classes = match.group(2).split(',') if match.group(2) else []
            
            # Cleanup base class names
            base_classes = [cls.strip() for cls in base_classes]
            
            class_info = {
                "name": class_name,
                "base_classes": base_classes,
                "methods": [],
                "properties": [],
                "fields": []
            }
            
            # Find the class content between { and matching }
            class_start = self.content.find('{', match.end())
            if class_start != -1:
                # Find the matching closing brace
                brace_count = 1
                class_end = class_start + 1
                while brace_count > 0 and class_end < len(self.content):
                    if self.content[class_end] == '{':
                        brace_count += 1
                    elif self.content[class_end] == '}':
                        brace_count -= 1
                    class_end += 1
                
                # Extract methods and properties within the class
                class_content = self.content[class_start:class_end]
                
                # Add methods, properties, and fields to class_info
                # This would require additional parsing logic
            
            classes.append(class_info)
            
        return classes

    def get_methods(self) -> List[Dict[str, Any]]:
        """
        Extract methods information from the C# code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a method.
        """
        methods = []
        for match in re.finditer(self.method_pattern, self.content):
            return_type = match.group(1)
            method_name = match.group(2)
            parameters_str = match.group(3)
            
            # Parse parameters
            parameters = []
            if parameters_str:
                for param in parameters_str.split(','):
                    param = param.strip()
                    if param:
                        param_parts = param.split()
                        param_type = ' '.join(param_parts[:-1])
                        param_name = param_parts[-1]
                        parameters.append({
                            "type": param_type.strip(),
                            "name": param_name.strip()
                        })
            
            method_info = {
                "name": method_name,
                "return_type": return_type,
                "parameters": parameters
            }
            
            methods.append(method_info)
            
        return methods

    def get_properties(self) -> List[Dict[str, Any]]:
        """
        Extract properties information from the C# code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a property.
        """
        properties = []
        for match in re.finditer(self.property_pattern, self.content):
            property_type = match.group(1)
            property_name = match.group(2)
            
            property_info = {
                "name": property_name,
                "type": property_type
            }
            
            properties.append(property_info)
            
        return properties

    def get_fields(self) -> List[Dict[str, Any]]:
        """
        Extract fields information from the C# code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a field.
        """
        fields = []
        for match in re.finditer(self.field_pattern, self.content):
            field_type = match.group(1)
            field_name = match.group(2)
            
            field_info = {
                "name": field_name,
                "type": field_type
            }
            
            fields.append(field_info)
            
        return fields
    
    def get_namespaces(self) -> List[str]:
        """
        Extract namespaces from the C# code.
        
        Returns:
            List[str]: A list of namespace names.
        """
        namespace_pattern = r"namespace\s+([^\s{;]+)"
        return [match.group(1) for match in re.finditer(namespace_pattern, self.content)]
    
    def get_using_directives(self) -> List[str]:
        """
        Extract using directives from the C# code.
        
        Returns:
            List[str]: A list of using directive statements.
        """
        using_pattern = r"using\s+([^;]+);"
        return [match.group(1).strip() for match in re.finditer(using_pattern, self.content)]
