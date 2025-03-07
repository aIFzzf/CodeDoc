#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CodeDoc MCP 服务器模块
提供代码文档生成服务，使用 Model Context Protocol (MCP) 实现
"""

# Import built-in modules
import os
import sys
import logging
import argparse
from typing import Dict, List, Any, Optional

# Import third-party modules
from mcp.server.fastmcp import FastMCP, Context

# 添加项目根目录到系统路径，确保能够导入 unity_code_parser
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import local modules
from unity_code_parser.main import get_parser_for_file, process_file, process_directory

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("code-doc-mcp")

# 创建 MCP 服务器
mcp = FastMCP("CodeDoc", 
              description="代码文档生成服务，支持多种编程语言的代码解析和文档生成",
              dependencies=["flask", "flask-restful", "python-dotenv", "requests", "aiohttp", "antlr4-python3-runtime", "jinja2"])

# 全局变量
OUTPUT_DIR = "docs"

def set_output_dir(dir_path: str) -> None:
    """
    设置输出目录
    
    Args:
        dir_path: 输出目录路径
    """
    global OUTPUT_DIR
    OUTPUT_DIR = dir_path
    
    # 确保输出目录存在
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logger.info(f"创建输出目录: {OUTPUT_DIR}")

# 工具定义
@mcp.tool()
def parse_code(file_path: str) -> Dict[str, Any]:
    """
    解析指定的代码文件，提取结构化信息
    
    Args:
        file_path: 要解析的代码文件路径
        
    Returns:
        Dict[str, Any]: 包含解析结果的字典
    """
    logger.info(f"解析文件: {file_path}")
    
    parser = get_parser_for_file(file_path)
    if parser is None:
        raise ValueError(f"不支持的文件类型: {file_path}")
        
    parsed_data = parser.parse()
    return parsed_data

@mcp.tool()
def generate_documentation(file_path: str, ctx: Context) -> Dict[str, str]:
    """
    为指定的代码文件生成文档
    
    Args:
        file_path: 要生成文档的代码文件路径
        ctx: MCP 上下文对象
        
    Returns:
        Dict[str, str]: 包含生成的文档文件路径的字典
    """
    logger.info(f"为文件生成文档: {file_path}")
    
    # 使用 unity_code_parser 的文档生成功能
    output_files = process_file(
        file_path,
        OUTPUT_DIR,
        generate_markdown=True,
        generate_class_diagram=True,
        generate_flow_diagram=False
    )
    
    if output_files:
        ctx.info("生成的文件:")
        for doc_type, doc_path in output_files.items():
            ctx.info(f"  {doc_type}: {doc_path}")
    else:
        ctx.warning("未生成文档。")
        
    return output_files

@mcp.tool()
def process_directory_docs(directory_path: str, ctx: Context, recursive: bool = True) -> Dict[str, Dict[str, str]]:
    """
    处理目录中的所有代码文件并生成文档
    
    Args:
        directory_path: 要处理的目录路径
        ctx: MCP 上下文对象
        recursive: 是否递归处理子目录
        
    Returns:
        Dict[str, Dict[str, str]]: 包含生成的文档文件路径的字典
    """
    logger.info(f"处理目录: {directory_path}")
    
    results = process_directory(
        directory_path, 
        OUTPUT_DIR, 
        file_patterns=None,  # 使用默认模式
        recursive=recursive, 
        generate_markdown=True, 
        generate_class_diagram=True, 
        generate_flow_diagram=False
    )
    
    if results:
        ctx.info(f"处理了 {len(results)} 个文件:")
        for file_path, output_files in results.items():
            ctx.info(f"  {file_path}:")
            for doc_type, doc_path in output_files.items():
                ctx.info(f"    {doc_type}: {doc_path}")
    else:
        ctx.warning("未生成文档。")
        
    return results

# 资源定义
@mcp.resource("code://{file_path}")
def get_code_content(file_path: str) -> str:
    """
    获取代码文件的内容
    
    Args:
        file_path: 代码文件路径
        
    Returns:
        str: 文件内容
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        logger.error(f"读取文件错误: {str(e)}")
        raise

@mcp.resource("docs://{doc_path}")
def get_doc_content(doc_path: str) -> str:
    """
    获取生成的文档内容
    
    Args:
        doc_path: 文档文件路径
        
    Returns:
        str: 文档内容
    """
    try:
        full_path = os.path.join(OUTPUT_DIR, doc_path)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        logger.error(f"读取文档错误: {str(e)}")
        raise

# 提示定义
@mcp.prompt()
def analyze_code(language: str, code: str) -> str:
    """
    分析代码的提示模板
    
    Args:
        language: 编程语言
        code: 代码内容
        
    Returns:
        str: 提示模板
    """
    return f"""请分析以下{language}代码：

```{language}
{code}
```

请提取关键信息并生成文档大纲，包括：
1. 类和函数的结构
2. 主要功能和用途
3. 关键算法和设计模式
4. 依赖关系
"""

def process_input_path(input_path: str, output_dir: str) -> None:
    """
    处理输入路径，生成文档
    
    Args:
        input_path: 输入文件或目录路径
        output_dir: 输出目录
    """
    if input_path is None:
        logger.info("未提供输入路径，跳过处理")
        return
        
    # 设置输出目录
    set_output_dir(output_dir)
        
    # 处理输入
    if os.path.isfile(input_path):
        logger.info(f"处理文件: {input_path}")
        output_files = process_file(
            input_path, 
            OUTPUT_DIR, 
            generate_markdown=True, 
            generate_class_diagram=True, 
            generate_flow_diagram=False
        )
        
        if output_files:
            logger.info("生成的文件:")
            for doc_type, file_path in output_files.items():
                logger.info(f"  {doc_type}: {file_path}")
        else:
            logger.info("未生成文档。")
    
    elif os.path.isdir(input_path):
        logger.info(f"处理目录: {input_path}")
        results = process_directory(
            input_path, 
            OUTPUT_DIR, 
            file_patterns=None,  # 使用默认模式
            recursive=True, 
            generate_markdown=True, 
            generate_class_diagram=True, 
            generate_flow_diagram=False
        )
        
        if results:
            logger.info(f"处理了 {len(results)} 个文件:")
            for file_path, output_files in results.items():
                logger.info(f"  {file_path}:")
                for doc_type, doc_path in output_files.items():
                    logger.info(f"    {doc_type}: {doc_path}")
        else:
            logger.info("未生成文档。")
    
    else:
        logger.error(f"错误: {input_path} 不是有效的文件或目录。")

def main():
    """
    主函数，解析命令行参数并启动服务器
    """
    parser = argparse.ArgumentParser(description='CodeDoc MCP 服务器')
    
    # 添加参数
    parser.add_argument('--file_path', '-f', help='要处理的文件或目录路径')
    parser.add_argument('--output', '-o', default='docs', help='生成文档的输出目录 (默认: docs)')
    
    args = parser.parse_args()
    
    # 如果提供了文件路径，先处理它
    if args.file_path:
        process_input_path(args.file_path, args.output)
    
    # 设置全局输出目录
    set_output_dir(args.output)
    
    # 启动 MCP 服务器
    logger.info("启动 MCP 服务器...")
    mcp.run()

if __name__ == "__main__":
    main()
