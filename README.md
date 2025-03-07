# Unity Code Documentation Framework (MCP版本)

一个基于Model Context Protocol (MCP)的代码文档生成框架，可以自动解析Unity C#代码、Shader代码和其他编程语言，生成对应的Markdown文档和Mermaid图表，以提高代码的可读性和可维护性。

## 特性

- **多语言支持**:
  - Unity C#代码
  - Unity Shader代码
  - Python代码
  - JavaScript代码
  - C++代码

- **文档生成**:
  - Markdown文档，包含详细的代码结构
  - Mermaid类图，展示类之间的关系
  - Mermaid流程图，展示方法调用（可选）

- **MCP架构优势**:
  - 标准化的工具和资源接口
  - 内置的提示模板系统
  - 完善的日志和错误处理
  - 支持异步操作
  - 可扩展的设计

## 安装

1. 克隆仓库:
   ```bash
   git clone https://github.com/yourusername/unity-code-doc.git
   cd unity-code-doc
   ```

2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

### 启动MCP服务器

```bash
python mcp_server/run.py [--debug]
```

参数说明:
- `--debug`: 启用调试模式，显示详细日志

### MCP工具

服务器提供以下工具：

1. `parse_code`: 解析指定的代码文件
2. `generate_docs`: 生成Markdown文档
3. `generate_diagrams`: 生成Mermaid图表

### MCP资源

可以通过以下URI模式访问资源：

- `file://code/*`: 访问代码文件
- `file://docs/*`: 访问生成的文档

### 提示模板

内置的代码分析提示模板可帮助生成更准确的文档。

## 项目结构

```
unity_code_parser/          # 原始代码解析模块
├── parser/
│   ├── base_parser.py
│   ├── csharp_parser.py
│   ├── shader_parser.py
│   └── ...
└── generator/
    ├── markdown_generator.py
    └── mermaid_generator.py

mcp_server/                # MCP服务器模块
├── server.py              # MCP服务器实现
└── run.py                 # 服务器启动脚本
```

## 添加新语言支持

1. 在 `unity_code_parser/parser` 目录下创建新的解析器类
2. 继承 `BaseParser` 类并实现必要的方法
3. 在 MCP 服务器中注册新的语言支持

## 贡献

欢迎提交Pull Request！

## 许可证

本项目采用MIT许可证 - 详见LICENSE文件
