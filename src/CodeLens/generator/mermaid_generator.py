#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mermaid diagram generator module.
This module provides functionality to generate Mermaid diagrams from parsed code data.
"""

import os
from typing import Dict, List, Any, Optional


class MermaidGenerator:
    """
    Generates Mermaid diagrams from parsed code data.
    """

    def __init__(self, output_dir: str = "docs"):
        """
        Initialize the Mermaid diagram generator.

        Args:
            output_dir: Directory to save generated Mermaid diagram files.
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_class_diagram(self, parsed_data: Dict[str, Any], output_file: str) -> str:
        """
        Generate a Mermaid class diagram from parsed code data.

        Args:
            parsed_data: Dictionary containing parsed code data.
            output_file: Name of the output file.

        Returns:
            str: Path to the generated Mermaid diagram file.
        """
        language = parsed_data.get("language", "Unknown")
        
        content = []
        content.append("```mermaid")
        content.append("classDiagram")
        
        if language == "C#":
            self._add_csharp_classes(content, parsed_data)
        elif language == "Python":
            self._add_python_classes(content, parsed_data)
        elif language == "JavaScript":
            self._add_javascript_classes(content, parsed_data)
        elif language == "C++":
            self._add_cpp_classes(content, parsed_data)
        
        content.append("```")
        
        # Write content to file
        file_path = os.path.join(self.output_dir, output_file)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(content))
        
        return file_path

    def generate_flow_diagram(self, parsed_data: Dict[str, Any], output_file: str) -> str:
        """
        Generate a Mermaid flow diagram from parsed code data.

        Args:
            parsed_data: Dictionary containing parsed code data.
            output_file: Name of the output file.

        Returns:
            str: Path to the generated Mermaid diagram file.
        """
        content = []
        content.append("```mermaid")
        content.append("flowchart TD")
        
        # This is a simplified implementation and will need to be expanded
        # based on how method calls are represented in the parsed data
        # Here we simply show how methods might be connected
        
        # Add nodes for classes and methods
        classes = parsed_data.get("classes", [])
        for i, class_info in enumerate(classes):
            class_name = class_info['name']
            content.append(f"    C{i}[{class_name}]")
            
            # Add nodes for methods
            methods = class_info.get("methods", [])
            for j, method in enumerate(methods):
                method_name = method['name']
                content.append(f"    C{i}M{j}[{method_name}]")
                content.append(f"    C{i} -->|has method| C{i}M{j}")
        
        # Add connections between methods if we have call information
        # This would require additional parsing to determine method calls
        
        content.append("```")
        
        # Write content to file
        file_path = os.path.join(self.output_dir, output_file)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(content))
        
        return file_path

    def generate_structure_diagram(self, parsed_data: Dict[str, Any], output_file: str) -> str:
        """
        Generate a Mermaid structure diagram from parsed code data.

        Args:
            parsed_data: Dictionary containing parsed code data.
            output_file: Name of the output file.

        Returns:
            str: Path to the generated Mermaid diagram file.
        """
        content = []
        content.append("```mermaid")
        content.append("graph TD")
        
        language = parsed_data.get("language", "Unknown")
        
        if language == "Shader":
            self._add_shader_structure(content, parsed_data)
        else:
            # Generic structure for other languages
            self._add_generic_structure(content, parsed_data)
        
        content.append("```")
        
        # Write content to file
        file_path = os.path.join(self.output_dir, output_file)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(content))
        
        return file_path

    def _add_csharp_classes(self, content: List[str], parsed_data: Dict[str, Any]):
        """
        Add C# classes to a Mermaid class diagram.

        Args:
            content: List of Mermaid diagram content lines.
            parsed_data: Dictionary containing parsed C# code data.
        """
        classes = parsed_data.get("classes", [])
        
        # Define class nodes and relationships
        for class_info in classes:
            class_name = class_info['name']
            
            # Add class
            content.append(f"    class {class_name} {{")
            
            # Add properties
            properties = class_info.get("properties", [])
            for prop in properties:
                content.append(f"        +{prop['type']} {prop['name']}")
            
            # Add fields
            fields = class_info.get("fields", [])
            for field in fields:
                modifier = field.get("modifier", "")
                modifier_symbol = "-" if modifier == "private" else "+"
                content.append(f"        {modifier_symbol}{field['type']} {field['name']}")
            
            # Add methods
            methods = class_info.get("methods", [])
            for method in methods:
                modifier = method.get("modifier", "")
                modifier_symbol = "-" if modifier == "private" else "+"
                
                # Format parameters
                params_str = ", ".join([f"{param['type']} {param['name']}" for param in method.get("parameters", [])])
                
                content.append(f"        {modifier_symbol}{method['name']}({params_str}) {method['return_type']}")
            
            content.append("    }")
            
            # Add inheritance relationships
            base_classes = class_info.get("base_classes", [])
            for base in base_classes:
                # Skip interfaces for now
                if not base.startswith("I"):
                    content.append(f"    {base} <|-- {class_name}")
            
            # Add interface implementation
            interfaces = [base for base in class_info.get("base_classes", []) if base.startswith("I")]
            for interface in interfaces:
                content.append(f"    {class_name} ..|> {interface} : implements")

    def _add_python_classes(self, content: List[str], parsed_data: Dict[str, Any]):
        """
        Add Python classes to a Mermaid class diagram.

        Args:
            content: List of Mermaid diagram content lines.
            parsed_data: Dictionary containing parsed Python code data.
        """
        classes = parsed_data.get("classes", [])
        
        # Define class nodes and relationships
        for class_info in classes:
            class_name = class_info['name']
            
            # Add class
            content.append(f"    class {class_name} {{")
            
            # Add attributes
            attributes = class_info.get("attributes", [])
            for attr in attributes:
                content.append(f"        +{attr['name']}")
            
            # Add methods
            methods = class_info.get("methods", [])
            for method in methods:
                # Format parameters
                params = method.get("parameters", [])
                
                # Skip 'self' parameter
                if params and params[0]['name'] == 'self':
                    params = params[1:]
                
                params_str = ", ".join([param['name'] for param in params])
                
                # Use private method notation for methods starting with underscore
                modifier_symbol = "-" if method['name'].startswith("_") else "+"
                
                returns_str = f" {method['returns']}" if method.get("returns") else ""
                
                content.append(f"        {modifier_symbol}{method['name']}({params_str}){returns_str}")
            
            content.append("    }")
            
            # Add inheritance relationships
            bases = class_info.get("bases", [])
            for base in bases:
                content.append(f"    {base} <|-- {class_name}")

    def _add_javascript_classes(self, content: List[str], parsed_data: Dict[str, Any]):
        """
        Add JavaScript classes to a Mermaid class diagram.

        Args:
            content: List of Mermaid diagram content lines.
            parsed_data: Dictionary containing parsed JavaScript code data.
        """
        classes = parsed_data.get("classes", [])
        
        # Define class nodes and relationships
        for class_info in classes:
            class_name = class_info['name']
            
            # Add class
            content.append(f"    class {class_name} {{")
            
            # Add properties
            properties = class_info.get("properties", [])
            for prop in properties:
                # Use private property notation for properties starting with underscore
                modifier_symbol = "-" if prop['name'].startswith("_") else "+"
                content.append(f"        {modifier_symbol}{prop['name']}")
            
            # Add methods
            methods = class_info.get("methods", [])
            for method in methods:
                # Format parameters
                params = method.get("parameters", [])
                params_str = ", ".join([param['name'] for param in params])
                
                # Use private method notation for methods starting with underscore
                modifier_symbol = "-" if method['name'].startswith("_") else "+"
                
                content.append(f"        {modifier_symbol}{method['name']}({params_str})")
            
            content.append("    }")
            
            # Add inheritance relationships
            parent = class_info.get("parent", "")
            if parent:
                content.append(f"    {parent} <|-- {class_name}")

    def _add_cpp_classes(self, content: List[str], parsed_data: Dict[str, Any]):
        """
        Add C++ classes to a Mermaid class diagram.

        Args:
            content: List of Mermaid diagram content lines.
            parsed_data: Dictionary containing parsed C++ code data.
        """
        classes = parsed_data.get("classes", [])
        
        # Define class nodes and relationships
        for class_info in classes:
            class_name = class_info['name']
            
            # Add class
            content.append(f"    class {class_name} {{")
            
            # Add properties
            properties = class_info.get("properties", [])
            for prop in properties:
                content.append(f"        +{prop['type']} {prop['name']}")
            
            # Add methods
            methods = class_info.get("methods", [])
            for method in methods:
                # Format parameters
                params_str = ", ".join([f"{param['type']} {param['name']}" if param['name'] else param['type'] for param in method.get("parameters", [])])
                
                content.append(f"        +{method['return_type']} {method['name']}({params_str})")
            
            content.append("    }")
            
            # Add inheritance relationships
            base_classes = class_info.get("base_classes", [])
            for base in base_classes:
                content.append(f"    {base} <|-- {class_name}")

    def _add_shader_structure(self, content: List[str], parsed_data: Dict[str, Any]):
        """
        Add Shader structure to a Mermaid structure diagram.

        Args:
            content: List of Mermaid diagram content lines.
            parsed_data: Dictionary containing parsed Shader code data.
        """
        shader_name = parsed_data.get("name", "Unknown Shader")
        
        # Add shader node
        content.append(f"    Shader[\"{shader_name}\"]")
        
        # Add properties
        content.append("    Properties[\"Properties\"]")
        content.append("    Shader --> Properties")
        
        properties = parsed_data.get("properties", [])
        for i, prop in enumerate(properties):
            prop_name = prop['name']
            content.append(f"    Prop{i}[\"{prop_name}: {prop['type']}\"]")
            content.append(f"    Properties --> Prop{i}")
        
        # Add subshaders
        subshaders = parsed_data.get("subshaders", [])
        for i, subshader in enumerate(subshaders):
            content.append(f"    SubShader{i}[\"SubShader {i+1}\"]")
            content.append(f"    Shader --> SubShader{i}")
            
            # Add passes
            passes = subshader.get("passes", [])
            for j, pass_info in enumerate(passes):
                pass_name = pass_info.get("name", f"Pass {j+1}")
                content.append(f"    Pass{i}_{j}[\"{pass_name}\"]")
                content.append(f"    SubShader{i} --> Pass{i}_{j}")
                
                # Add vertex and fragment programs
                vertex_program = pass_info.get("vertex_program", "")
                if vertex_program:
                    content.append(f"    Vertex{i}_{j}[\"Vertex Program: {vertex_program}\"]")
                    content.append(f"    Pass{i}_{j} --> Vertex{i}_{j}")
                
                fragment_program = pass_info.get("fragment_program", "")
                if fragment_program:
                    content.append(f"    Fragment{i}_{j}[\"Fragment Program: {fragment_program}\"]")
                    content.append(f"    Pass{i}_{j} --> Fragment{i}_{j}")

    def _add_generic_structure(self, content: List[str], parsed_data: Dict[str, Any]):
        """
        Add generic structure to a Mermaid structure diagram.

        Args:
            content: List of Mermaid diagram content lines.
            parsed_data: Dictionary containing parsed code data.
        """
        file_name = os.path.basename(parsed_data.get("file_path", "Unknown"))
        language = parsed_data.get("language", "Unknown")
        
        # Add file node
        content.append(f"    File[\"{file_name} ({language})\"]")
        
        # Add classes
        classes = parsed_data.get("classes", [])
        if classes:
            content.append("    Classes[\"Classes\"]")
            content.append("    File --> Classes")
            
            for i, class_info in enumerate(classes):
                class_name = class_info['name']
                content.append(f"    Class{i}[\"{class_name}\"]")
                content.append(f"    Classes --> Class{i}")
                
                # Add methods
                methods = class_info.get("methods", [])
                if methods:
                    content.append(f"    Methods{i}[\"Methods\"]")
                    content.append(f"    Class{i} --> Methods{i}")
                    
                    for j, method in enumerate(methods):
                        method_name = method['name']
                        content.append(f"    Method{i}_{j}[\"{method_name}\"]")
                        content.append(f"    Methods{i} --> Method{i}_{j}")
        
        # Add functions
        functions = parsed_data.get("functions", [])
        if functions:
            content.append("    Functions[\"Functions\"]")
            content.append("    File --> Functions")
            
            for i, function in enumerate(functions):
                function_name = function['name']
                content.append(f"    Function{i}[\"{function_name}\"]")
                content.append(f"    Functions --> Function{i}")
