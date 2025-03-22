#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for CodeLens package.
"""

from setuptools import setup, find_packages

# 读取版本信息
with open("src/CodeLens/__version__.py", "r") as f:
    exec(f.read())

# 读取README作为长描述
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "CodeLens - Code analysis and documentation tool"

setup(
    name="code-lens-tool",  # 修改为一个独特的名称
    version=__version__,  # 从__version__.py中获取
    description="Code analysis and documentation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CodeLens Team",
    author_email="codelens@example.com",
    url="https://github.com/aIFzzf/CodeLens",  # 更新为您的GitHub仓库URL
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "loguru>=0.6.0",
        "mcp>=1.0.0",
        "regex>=2022.10.31",
        "jinja2>=3.1.2",
        "markdown>=3.4.3",
    ],
    entry_points={
        "console_scripts": [
            "code-lens-tool=CodeLens.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
    ],
    keywords="code analysis, documentation, markdown, mermaid, diagram",
    python_requires=">=3.8",
    project_urls={
        "Bug Reports": "https://github.com/aIFzzf/CodeLens/issues",
        "Source": "https://github.com/aIFzzf/CodeLens",
        "Documentation": "https://github.com/aIFzzf/CodeLens#readme",
    },
    include_package_data=True,
    zip_safe=False,
)
