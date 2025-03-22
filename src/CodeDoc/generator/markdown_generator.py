#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Markdown generator module.
This module provides functionality to generate Markdown documentation from parsed code data.
"""

import os
from typing import Dict, List, Any, Optional


class MarkdownGenerator:
    """
    Generates Markdown documentation from parsed code data.
    """

    def __init__(self, output_dir: str = "docs"):
        """
        Initialize the Markdown generator.

        Args:
            output_dir: Directory to save generated Markdown files.
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate(self, parsed_data: Dict[str, Any], output_file: str) -> str:
        """
        Generate Markdown documentation from parsed code data.

        Args:
            parsed_data: Dictionary containing parsed code data.
            output_file: Name of the output file.

        Returns:
            str: Path to the generated Markdown file.
        """
        language = parsed_data.get("language", "Unknown")
        
        if language == "C#":
            content = self._generate_csharp_markdown(parsed_data)
        elif language == "Shader":
            content = self._generate_shader_markdown(parsed_data)
        elif language == "Python":
            content = self._generate_python_markdown(parsed_data)
        elif language == "JavaScript":
            content = self._generate_javascript_markdown(parsed_data)
        elif language == "C++":
            content = self._generate_cpp_markdown(parsed_data)
        else:
            content = self._generate_generic_markdown(parsed_data)
        
        # Write content to file
        file_path = os.path.join(self.output_dir, output_file)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return file_path

    def _generate_csharp_markdown(self, parsed_data: Dict[str, Any]) -> str:
        """
        Generate Markdown for C# code.

        Args:
            parsed_data: Dictionary containing parsed C# code data.

        Returns:
            str: Markdown content for C# code.
        """
        content = []
        
        # Add title
        file_name = os.path.basename(parsed_data.get("file_path", "Unknown"))
        content.append(f"# {file_name}\n")
        
        # Add namespaces
        namespaces = parsed_data.get("namespaces", [])
        if namespaces:
            content.append("## Namespaces\n")
            for namespace in namespaces:
                content.append(f"- `{namespace}`\n")
            content.append("")
        
        # Add using directives
        using_directives = parsed_data.get("using_directives", [])
        if using_directives:
            content.append("## Using Directives\n")
            for directive in using_directives:
                content.append(f"- `{directive}`\n")
            content.append("")
        
        # Add classes
        classes = parsed_data.get("classes", [])
        if classes:
            for class_info in classes:
                content.append(f"## Class: {class_info['name']}\n")
                
                # Add base classes
                base_classes = class_info.get("base_classes", [])
                if base_classes:
                    content.append("### Inherits From\n")
                    for base in base_classes:
                        content.append(f"- `{base}`\n")
                    content.append("")
                
                # Add properties
                properties = class_info.get("properties", [])
                if properties:
                    content.append("### Properties\n")
                    for prop in properties:
                        content.append(f"- `{prop['name']}`: {prop['type']}\n")
                    content.append("")
                
                # Add fields
                fields = class_info.get("fields", [])
                if fields:
                    content.append("### Fields\n")
                    for field in fields:
                        content.append(f"- `{field['name']}`: {field['type']}\n")
                    content.append("")
                
                # Add methods
                methods = class_info.get("methods", [])
                if methods:
                    content.append("### Methods\n")
                    for method in methods:
                        # Format parameters
                        params_str = ", ".join([f"{param['type']} {param['name']}" for param in method.get("parameters", [])])
                        content.append(f"- `{method['name']}({params_str})`: {method['return_type']}\n")
                    content.append("")
        
        return "\n".join(content)

    def _generate_shader_markdown(self, parsed_data: Dict[str, Any]) -> str:
        """
        Generate Markdown for Shader code.

        Args:
            parsed_data: Dictionary containing parsed Shader code data.

        Returns:
            str: Markdown content for Shader code.
        """
        content = []
        
        # Add title
        shader_name = parsed_data.get("name", "Unknown Shader")
        content.append(f"# Shader: {shader_name}\n")
        
        # Add properties
        properties = parsed_data.get("properties", [])
        if properties:
            content.append("## Properties\n")
            for prop in properties:
                content.append(f"- `{prop['name']}`: {prop['type']} - {prop['display_name']}")
                if "default_value" in prop:
                    content.append(f" (Default: {prop['default_value']})")
                content.append("\n")
            content.append("")
        
        # Add subshaders
        subshaders = parsed_data.get("subshaders", [])
        if subshaders:
            content.append("## SubShaders\n")
            for i, subshader in enumerate(subshaders):
                content.append(f"### SubShader {i+1}\n")
                
                # Add tags
                tags = subshader.get("tags", {})
                if tags:
                    content.append("#### Tags\n")
                    for tag_name, tag_value in tags.items():
                        content.append(f"- `{tag_name}`: {tag_value}\n")
                    content.append("")
                
                # Add passes
                passes = subshader.get("passes", [])
                if passes:
                    content.append("#### Passes\n")
                    for j, pass_info in enumerate(passes):
                        pass_name = pass_info.get("name", f"Pass {j+1}")
                        content.append(f"##### {pass_name}\n")
                        
                        # Add pass tags
                        pass_tags = pass_info.get("tags", {})
                        if pass_tags:
                            content.append("###### Tags\n")
                            for tag_name, tag_value in pass_tags.items():
                                content.append(f"- `{tag_name}`: {tag_value}\n")
                            content.append("")
                        
                        # Add vertex program
                        vertex_program = pass_info.get("vertex_program", "")
                        if vertex_program:
                            content.append(f"###### Vertex Program: `{vertex_program}`\n")
                        
                        # Add fragment program
                        fragment_program = pass_info.get("fragment_program", "")
                        if fragment_program:
                            content.append(f"###### Fragment Program: `{fragment_program}`\n")
                        
                        content.append("")
        
        return "\n".join(content)

    def _generate_python_markdown(self, parsed_data: Dict[str, Any]) -> str:
        """
        Generate Markdown for Python code.

        Args:
            parsed_data: Dictionary containing parsed Python code data.

        Returns:
            str: Markdown content for Python code.
        """
        content = []
        
        # Add title
        file_name = os.path.basename(parsed_data.get("file_path", "Unknown"))
        content.append(f"# Python Module: {file_name}\n")
        
        # Add imports
        imports = parsed_data.get("imports", [])
        if imports:
            content.append("## Imports\n")
            for import_info in imports:
                if import_info.get("type") == "import":
                    import_str = f"import {import_info['name']}"
                    if import_info.get("alias"):
                        import_str += f" as {import_info['alias']}"
                    content.append(f"- `{import_str}`\n")
                elif import_info.get("type") == "from_import":
                    import_str = f"from {import_info['module']} import {import_info['name']}"
                    if import_info.get("alias"):
                        import_str += f" as {import_info['alias']}"
                    content.append(f"- `{import_str}`\n")
            content.append("")
        
        # Add classes
        classes = parsed_data.get("classes", [])
        if classes:
            for class_info in classes:
                content.append(f"## Class: {class_info['name']}\n")
                
                # Add docstring
                docstring = class_info.get("docstring", "")
                if docstring:
                    content.append(f"{docstring}\n")
                
                # Add bases
                bases = class_info.get("bases", [])
                if bases:
                    content.append("### Inherits From\n")
                    for base in bases:
                        content.append(f"- `{base}`\n")
                    content.append("")
                
                # Add attributes
                attributes = class_info.get("attributes", [])
                if attributes:
                    content.append("### Attributes\n")
                    for attr in attributes:
                        value_str = attr.get("value", "")
                        content.append(f"- `{attr['name']}`: {value_str}\n")
                    content.append("")
                
                # Add methods
                methods = class_info.get("methods", [])
                if methods:
                    content.append("### Methods\n")
                    for method in methods:
                        # Format parameters
                        params = method.get("parameters", [])
                        params_str = ", ".join([f"{param['name']}: {param['type']}" if param.get("type") else param['name'] for param in params])
                        returns_str = f" -> {method['returns']}" if method.get("returns") else ""
                        
                        content.append(f"#### `{method['name']}({params_str}){returns_str}`\n")
                        
                        # Add docstring
                        method_docstring = method.get("docstring", "")
                        if method_docstring:
                            content.append(f"{method_docstring}\n")
                        
                        content.append("")
        
        # Add functions
        functions = parsed_data.get("functions", [])
        if functions:
            content.append("## Functions\n")
            for function in functions:
                # Format parameters
                params = function.get("parameters", [])
                params_str = ", ".join([f"{param['name']}: {param['type']}" if param.get("type") else param['name'] for param in params])
                returns_str = f" -> {function['returns']}" if function.get("returns") else ""
                
                content.append(f"### `{function['name']}({params_str}){returns_str}`\n")
                
                # Add docstring
                function_docstring = function.get("docstring", "")
                if function_docstring:
                    content.append(f"{function_docstring}\n")
                
                content.append("")
        
        # Add global variables
        globals_list = parsed_data.get("globals", [])
        if globals_list:
            content.append("## Global Variables\n")
            for global_var in globals_list:
                value_str = global_var.get("value", "")
                content.append(f"- `{global_var['name']}`: {value_str}\n")
            content.append("")
        
        return "\n".join(content)

    def _generate_javascript_markdown(self, parsed_data: Dict[str, Any]) -> str:
        """
        Generate Markdown for JavaScript code.

        Args:
            parsed_data: Dictionary containing parsed JavaScript code data.

        Returns:
            str: Markdown content for JavaScript code.
        """
        content = []
        
        # Add title
        file_name = os.path.basename(parsed_data.get("file_path", "Unknown"))
        content.append(f"# JavaScript File: {file_name}\n")
        
        # Add imports
        imports = parsed_data.get("imports", [])
        if imports:
            content.append("## Imports\n")
            for import_info in imports:
                module = import_info.get("module", "")
                
                if import_info.get("type") == "named":
                    import_items = import_info.get("imports", [])
                    content.append(f"- `import {{ {', '.join(import_items)} }} from '{module}'`\n")
                elif import_info.get("type") == "default":
                    import_name = import_info.get("import", "")
                    content.append(f"- `import {import_name} from '{module}'`\n")
            content.append("")
        
        # Add classes
        classes = parsed_data.get("classes", [])
        if classes:
            for class_info in classes:
                content.append(f"## Class: {class_info['name']}\n")
                
                # Add parent class
                parent = class_info.get("parent", "")
                if parent:
                    content.append(f"Extends: `{parent}`\n\n")
                
                # Add properties
                properties = class_info.get("properties", [])
                if properties:
                    content.append("### Properties\n")
                    for prop in properties:
                        value_str = prop.get("value", "")
                        content.append(f"- `{prop['name']}`: {value_str}\n")
                    content.append("")
                
                # Add methods
                methods = class_info.get("methods", [])
                if methods:
                    content.append("### Methods\n")
                    for method in methods:
                        # Format parameters
                        params = method.get("parameters", [])
                        params_str = ", ".join([param['name'] + (f" = {param['default']}" if "default" in param else "") for param in params])
                        
                        content.append(f"- `{method['name']}({params_str})`\n")
                    content.append("")
        
        # Add functions
        functions = parsed_data.get("functions", [])
        if functions:
            content.append("## Functions\n")
            for function in functions:
                # Format parameters
                params = function.get("parameters", [])
                params_str = ", ".join([param['name'] + (f" = {param['default']}" if "default" in param else "") for param in params])
                
                function_type = function.get("type", "function")
                if function_type == "function":
                    content.append(f"### `function {function['name']}({params_str})`\n")
                elif function_type == "arrow_function":
                    content.append(f"### `const {function['name']} = ({params_str}) => {{}}`\n")
                
                content.append("")
        
        return "\n".join(content)

    def _generate_cpp_markdown(self, parsed_data: Dict[str, Any]) -> str:
        """
        Generate Markdown for C++ code.

        Args:
            parsed_data: Dictionary containing parsed C++ code data.

        Returns:
            str: Markdown content for C++ code.
        """
        content = []
        
        # Add title
        file_name = os.path.basename(parsed_data.get("file_path", "Unknown"))
        content.append(f"# C++ File: {file_name}\n")
        
        # Add includes
        includes = parsed_data.get("includes", [])
        if includes:
            content.append("## Includes\n")
            for include in includes:
                content.append(f"- `#include <{include}>`\n")
            content.append("")
        
        # Add namespaces
        namespaces = parsed_data.get("namespaces", [])
        if namespaces:
            content.append("## Namespaces\n")
            for namespace in namespaces:
                content.append(f"- `{namespace['name']}`\n")
            content.append("")
        
        # Add classes
        classes = parsed_data.get("classes", [])
        if classes:
            for class_info in classes:
                content.append(f"## Class: {class_info['name']}\n")
                
                # Add base classes
                base_classes = class_info.get("base_classes", [])
                if base_classes:
                    content.append("### Inherits From\n")
                    for base in base_classes:
                        content.append(f"- `{base}`\n")
                    content.append("")
                
                # Add properties
                properties = class_info.get("properties", [])
                if properties:
                    content.append("### Properties\n")
                    for prop in properties:
                        content.append(f"- `{prop['name']}`: {prop['type']}\n")
                    content.append("")
                
                # Add methods
                methods = class_info.get("methods", [])
                if methods:
                    content.append("### Methods\n")
                    for method in methods:
                        # Format parameters
                        params_str = ", ".join([f"{param['type']} {param['name']}" if param['name'] else param['type'] for param in method.get("parameters", [])])
                        content.append(f"- `{method['return_type']} {method['name']}({params_str})`\n")
                    content.append("")
        
        # Add global functions
        functions = parsed_data.get("functions", [])
        if functions:
            content.append("## Global Functions\n")
            for function in functions:
                # Format parameters
                params_str = ", ".join([f"{param['type']} {param['name']}" if param['name'] else param['type'] for param in function.get("parameters", [])])
                content.append(f"- `{function['return_type']} {function['name']}({params_str})`\n")
            content.append("")
        
        return "\n".join(content)

    def _generate_generic_markdown(self, parsed_data: Dict[str, Any]) -> str:
        """
        Generate generic Markdown for any code.

        Args:
            parsed_data: Dictionary containing parsed code data.

        Returns:
            str: Markdown content.
        """
        content = []
        
        # Add title
        file_name = os.path.basename(parsed_data.get("file_path", "Unknown"))
        language = parsed_data.get("language", "Unknown")
        content.append(f"# {language} File: {file_name}\n")
        
        # Add error if present
        error = parsed_data.get("error", "")
        if error:
            content.append(f"**Error**: {error}\n")
        
        # Recursively add all other data as sections
        self._add_sections(content, parsed_data, 2)
        
        return "\n".join(content)

    def _add_sections(self, content: List[str], data: Dict[str, Any], level: int):
        """
        Recursively add sections from a dictionary to the content list.

        Args:
            content: List to add content to.
            data: Dictionary containing data to add.
            level: Current heading level.
        """
        # Skip certain sections we don't want to include
        skip_keys = ["language", "file_path", "error"]
        
        for key, value in data.items():
            if key in skip_keys:
                continue
            
            # Add section header
            header = "#" * level
            content.append(f"{header} {key.replace('_', ' ').title()}\n")
            
            # Handle different types of values
            if isinstance(value, dict):
                # Recursively add subsections for dictionaries
                self._add_sections(content, value, level + 1)
            elif isinstance(value, list):
                # Add list items for lists
                for item in value:
                    if isinstance(item, dict):
                        # Handle dictionaries in lists
                        for item_key, item_value in item.items():
                            content.append(f"- **{item_key}**: {item_value}\n")
                    else:
                        # Handle simple list items
                        content.append(f"- {item}\n")
                content.append("")
            else:
                # Add simple values
                content.append(f"{value}\n\n")
