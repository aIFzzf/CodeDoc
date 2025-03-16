"""CodeLens MCP Server.

This module provides a FastMCP server for CodeLens functionality.
It exposes tools for code analysis, documentation generation, and visualization.
"""

# Import built-in modules
import os
import sys

# 确保当前目录在路径中，便于相对导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import local modules
from __version__ import __version__
from CodeLens.app import mcp, APP_NAME
from CodeLens.errors import CodeLensError, ErrorCode

# 导入解析器
from CodeLens.parser.base_parser import BaseParser
from CodeLens.parser.python_parser import PythonParser
from CodeLens.parser.csharp_parser import CSharpParser
from CodeLens.parser.cpp_parser import CppParser
from CodeLens.parser.javascript_parser import JavaScriptParser
from CodeLens.parser.shader_parser import ShaderParser

# 导入生成器
from CodeLens.generator.markdown_generator import MarkdownGenerator
from CodeLens.generator.mermaid_generator import MermaidGenerator

# 导入MCP工具
from CodeLens.file import analyze_code_file, analyze_directory

# 暴露主要API
__all__ = [
    "__version__",
    "APP_NAME",
    "mcp",
    "CodeLensError",
    "ErrorCode",
    "BaseParser",
    "PythonParser",
    "CSharpParser",
    "CppParser",
    "JavaScriptParser",
    "ShaderParser",
    "MarkdownGenerator",
    "MermaidGenerator",
    "analyze_code_file",
    "analyze_directory"
]
