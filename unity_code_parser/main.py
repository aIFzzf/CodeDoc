#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unity Code Documentation Generator Main Module.
This module is the entry point for the Unity Code Documentation Generator.
It coordinates the parsing of code files and the generation of documentation.
"""

import os
import argparse
import fnmatch
from typing import Dict, List, Any, Optional

from parser.base_parser import BaseParser
from parser.csharp_parser import CSharpParser
from parser.shader_parser import ShaderParser
from parser.python_parser import PythonParser
from parser.javascript_parser import JavaScriptParser
from parser.cpp_parser import CppParser

from generator.markdown_generator import MarkdownGenerator
from generator.mermaid_generator import MermaidGenerator


def get_parser_for_file(file_path: str) -> Optional[BaseParser]:
    """
    Get the appropriate parser for a given file based on its extension.
    
    Args:
        file_path: Path to the file to parse.
        
    Returns:
        BaseParser: An instance of the appropriate parser for the file, or None if no parser is available.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == '.cs':
        return CSharpParser(file_path)
    elif ext == '.shader':
        return ShaderParser(file_path)
    elif ext == '.py':
        return PythonParser(file_path)
    elif ext in ['.js', '.jsx', '.ts', '.tsx']:
        return JavaScriptParser(file_path)
    elif ext in ['.cpp', '.cc', '.h', '.hpp']:
        return CppParser(file_path)
    else:
        return None


def process_file(file_path: str, output_dir: str, generate_markdown: bool = True, generate_class_diagram: bool = True, generate_flow_diagram: bool = False) -> Dict[str, str]:
    """
    Process a single file and generate documentation.
    
    Args:
        file_path: Path to the file to process.
        output_dir: Directory to save generated documentation.
        generate_markdown: Whether to generate Markdown documentation.
        generate_class_diagram: Whether to generate a class diagram.
        generate_flow_diagram: Whether to generate a flow diagram.
        
    Returns:
        Dict[str, str]: A dictionary mapping document types to their file paths.
    """
    parser = get_parser_for_file(file_path)
    
    if parser is None:
        print(f"No parser available for file: {file_path}")
        return {}
    
    parsed_data = parser.parse()
    parsed_data["file_path"] = file_path
    
    output_files = {}
    
    # Generate Markdown
    if generate_markdown:
        markdown_generator = MarkdownGenerator(output_dir)
        file_name_base = os.path.basename(file_path)
        markdown_file = f"{file_name_base}.md"
        markdown_path = markdown_generator.generate(parsed_data, markdown_file)
        output_files["markdown"] = markdown_path
    
    # Generate Class Diagram
    if generate_class_diagram:
        mermaid_generator = MermaidGenerator(output_dir)
        file_name_base = os.path.basename(file_path)
        class_diagram_file = f"{file_name_base}_class.md"
        class_diagram_path = mermaid_generator.generate_class_diagram(parsed_data, class_diagram_file)
        output_files["class_diagram"] = class_diagram_path
    
    # Generate Flow Diagram
    if generate_flow_diagram:
        mermaid_generator = MermaidGenerator(output_dir)
        file_name_base = os.path.basename(file_path)
        flow_diagram_file = f"{file_name_base}_flow.md"
        flow_diagram_path = mermaid_generator.generate_flow_diagram(parsed_data, flow_diagram_file)
        output_files["flow_diagram"] = flow_diagram_path
    
    return output_files


def process_directory(directory_path: str, output_dir: str, file_patterns: List[str] = None, recursive: bool = True, generate_markdown: bool = True, generate_class_diagram: bool = True, generate_flow_diagram: bool = False) -> Dict[str, Dict[str, str]]:
    """
    Process all files in a directory and its subdirectories.
    
    Args:
        directory_path: Path to the directory to process.
        output_dir: Directory to save generated documentation.
        file_patterns: List of file patterns to match (e.g., ['*.cs', '*.shader']).
        recursive: Whether to process subdirectories recursively.
        generate_markdown: Whether to generate Markdown documentation.
        generate_class_diagram: Whether to generate a class diagram.
        generate_flow_diagram: Whether to generate a flow diagram.
        
    Returns:
        Dict[str, Dict[str, str]]: A dictionary mapping file paths to their output files.
    """
    if file_patterns is None:
        file_patterns = ['*.cs', '*.shader', '*.py', '*.js', '*.jsx', '*.ts', '*.tsx', '*.cpp', '*.cc', '*.h', '*.hpp']
    
    results = {}
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Check if the file matches any of the patterns
            if any(fnmatch.fnmatch(file, pattern) for pattern in file_patterns):
                output_files = process_file(
                    file_path, 
                    output_dir, 
                    generate_markdown, 
                    generate_class_diagram, 
                    generate_flow_diagram
                )
                
                if output_files:
                    results[file_path] = output_files
        
        if not recursive:
            break
    
    return results


def main():
    """
    Main function to parse command-line arguments and process files.
    """
    parser = argparse.ArgumentParser(description='Generate documentation from Unity code.')
    
    # Add arguments
    parser.add_argument('input', help='Path to a file or directory to process')
    parser.add_argument('-o', '--output', default='docs', help='Directory to save generated documentation (default: docs)')
    parser.add_argument('-p', '--patterns', nargs='+', help='File patterns to match (e.g., *.cs *.shader)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Process subdirectories recursively')
    parser.add_argument('--no-markdown', action='store_true', help='Do not generate Markdown documentation')
    parser.add_argument('--no-class-diagram', action='store_true', help='Do not generate class diagrams')
    parser.add_argument('--flow-diagram', action='store_true', help='Generate flow diagrams')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Process input
    if os.path.isfile(args.input):
        print(f"Processing file: {args.input}")
        output_files = process_file(
            args.input, 
            args.output, 
            not args.no_markdown, 
            not args.no_class_diagram, 
            args.flow_diagram
        )
        
        if output_files:
            print("Generated files:")
            for doc_type, file_path in output_files.items():
                print(f"  {doc_type}: {file_path}")
        else:
            print("No documentation generated.")
    
    elif os.path.isdir(args.input):
        print(f"Processing directory: {args.input}")
        results = process_directory(
            args.input, 
            args.output, 
            args.patterns, 
            args.recursive, 
            not args.no_markdown, 
            not args.no_class_diagram, 
            args.flow_diagram
        )
        
        if results:
            print(f"Processed {len(results)} files:")
            for file_path, output_files in results.items():
                print(f"  {file_path}:")
                for doc_type, doc_path in output_files.items():
                    print(f"    {doc_type}: {doc_path}")
        else:
            print("No documentation generated.")
    
    else:
        print(f"Error: {args.input} is not a valid file or directory.")


if __name__ == '__main__':
    main()
