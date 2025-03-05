#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shader parser module.
This module provides functionality to parse Unity shader files.
"""

import re
from typing import Dict, List, Any, Optional
from .base_parser import BaseParser


class ShaderParser(BaseParser):
    """
    Parser for Unity shader files.
    Extracts shader properties, passes, and subshaders.
    """

    def __init__(self, file_path: str):
        """
        Initialize the shader parser with a file path.

        Args:
            file_path: Path to the shader file to parse.
        """
        super().__init__(file_path)
        # Regex patterns for shader parsing
        self.shader_name_pattern = r"Shader\s+\"([^\"]+)\""
        self.properties_block_pattern = r"Properties\s*{([^}]*)}"
        self.property_pattern = r"_(\w+)\s*\(\s*\"([^\"]*)\"\s*,\s*(\w+)\s*\)\s*=\s*([^\\n]*)"
        self.subshader_pattern = r"SubShader\s*{([^}]*)}"
        self.pass_pattern = r"Pass\s*{([^}]*)}"
        self.cg_program_pattern = r"CGPROGRAM(.*?)ENDCG"
        self.hlsl_program_pattern = r"HLSLPROGRAM(.*?)ENDHLSL"

    def parse(self) -> Dict[str, Any]:
        """
        Parse the shader file and extract structured information.
        
        Returns:
            Dict[str, Any]: A dictionary containing structured information about the shader.
        """
        return {
            "language": "Shader",
            "name": self.get_shader_name(),
            "properties": self.get_properties(),
            "subshaders": self.get_subshaders(),
            "passes": self.get_passes()
        }

    def get_shader_name(self) -> str:
        """
        Get the name of the shader.
        
        Returns:
            str: The name of the shader.
        """
        match = re.search(self.shader_name_pattern, self.content)
        return match.group(1) if match else "Unknown Shader"

    def get_properties(self) -> List[Dict[str, Any]]:
        """
        Extract properties from the shader.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a property.
        """
        properties = []
        
        # Find the Properties block
        properties_match = re.search(self.properties_block_pattern, self.content, re.DOTALL)
        if properties_match:
            properties_block = properties_match.group(1)
            
            # Extract individual properties
            for prop_match in re.finditer(self.property_pattern, properties_block):
                prop_name = prop_match.group(1)
                prop_display_name = prop_match.group(2)
                prop_type = prop_match.group(3)
                prop_default = prop_match.group(4).strip()
                
                property_info = {
                    "name": f"_{prop_name}",
                    "display_name": prop_display_name,
                    "type": prop_type,
                    "default_value": prop_default
                }
                
                properties.append(property_info)
                
        return properties

    def get_subshaders(self) -> List[Dict[str, Any]]:
        """
        Extract subshaders from the shader.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a subshader.
        """
        subshaders = []
        
        for subshader_match in re.finditer(self.subshader_pattern, self.content, re.DOTALL):
            subshader_content = subshader_match.group(1)
            
            subshader_info = {
                "tags": self.extract_tags(subshader_content),
                "passes": self.extract_passes(subshader_content)
            }
            
            subshaders.append(subshader_info)
            
        return subshaders

    def get_passes(self) -> List[Dict[str, Any]]:
        """
        Extract all passes from all subshaders.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a pass.
        """
        all_passes = []
        
        for subshader in self.get_subshaders():
            all_passes.extend(subshader["passes"])
            
        return all_passes

    def extract_tags(self, content: str) -> Dict[str, str]:
        """
        Extract tags from a shader block.
        
        Args:
            content: The content to extract tags from.
            
        Returns:
            Dict[str, str]: A dictionary of tag names and values.
        """
        tags = {}
        tag_block_pattern = r"Tags\s*{([^}]*)}"
        tag_pattern = r"\"(\w+)\"\s*=\s*\"([^\"]*)\""
        
        tag_block_match = re.search(tag_block_pattern, content, re.DOTALL)
        if tag_block_match:
            tag_block = tag_block_match.group(1)
            
            for tag_match in re.finditer(tag_pattern, tag_block):
                tag_name = tag_match.group(1)
                tag_value = tag_match.group(2)
                tags[tag_name] = tag_value
                
        return tags

    def extract_passes(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract passes from a shader block.
        
        Args:
            content: The content to extract passes from.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a pass.
        """
        passes = []
        
        for pass_match in re.finditer(self.pass_pattern, content, re.DOTALL):
            pass_content = pass_match.group(1)
            
            # Extract shader programs (CG or HLSL)
            cg_programs = []
            for cg_match in re.finditer(self.cg_program_pattern, pass_content, re.DOTALL):
                cg_programs.append(cg_match.group(1))
                
            hlsl_programs = []
            for hlsl_match in re.finditer(self.hlsl_program_pattern, pass_content, re.DOTALL):
                hlsl_programs.append(hlsl_match.group(1))
                
            pass_info = {
                "name": self.extract_pass_name(pass_content),
                "tags": self.extract_tags(pass_content),
                "cg_programs": cg_programs,
                "hlsl_programs": hlsl_programs,
                "vertex_program": self.extract_vertex_program(pass_content),
                "fragment_program": self.extract_fragment_program(pass_content)
            }
            
            passes.append(pass_info)
            
        return passes

    def extract_pass_name(self, pass_content: str) -> str:
        """
        Extract the name of a pass.
        
        Args:
            pass_content: The content of the pass.
            
        Returns:
            str: The name of the pass.
        """
        name_pattern = r"Name\s+\"([^\"]*)\""
        match = re.search(name_pattern, pass_content)
        return match.group(1) if match else "Unnamed Pass"

    def extract_vertex_program(self, pass_content: str) -> str:
        """
        Extract the vertex program from a pass.
        
        Args:
            pass_content: The content of the pass.
            
        Returns:
            str: The vertex program code.
        """
        # This is a simplified version, actual implementation would be more complex
        vertex_pattern = r"#pragma\s+vertex\s+(\w+)"
        match = re.search(vertex_pattern, pass_content)
        return match.group(1) if match else ""

    def extract_fragment_program(self, pass_content: str) -> str:
        """
        Extract the fragment program from a pass.
        
        Args:
            pass_content: The content of the pass.
            
        Returns:
            str: The fragment program code.
        """
        # This is a simplified version, actual implementation would be more complex
        fragment_pattern = r"#pragma\s+fragment\s+(\w+)"
        match = re.search(fragment_pattern, pass_content)
        return match.group(1) if match else ""
