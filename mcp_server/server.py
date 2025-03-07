from mcp_server import McpServer, ServerCapabilities, LoggingLevel
from mcp_server.tools import ToolRegistration
from mcp_server.resources import ResourceRegistration
from mcp_server.prompts import PromptRegistration
import logging

class CodeDocMcpServer:
    def __init__(self):
        # 配置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("code-doc-mcp")

        # 创建MCP服务器
        self.server = McpServer.sync(transport="stdio")  # 使用标准输入输出作为传输层
        self.server.server_info(
            name="code-doc-server",
            version="1.0.0"
        )
        
        # 配置服务器能力
        self.server.capabilities(
            ServerCapabilities.builder()
            .resources(True)  # 启用资源支持（用于访问代码文件）
            .tools(True)     # 启用工具支持（用于代码解析和文档生成）
            .prompts(True)   # 启用提示支持
            .logging()       # 启用日志支持
            .build()
        )

    def register_tools(self):
        """注册所有工具"""
        # 代码解析工具
        self.server.add_tool(
            ToolRegistration.builder()
            .name("parse_code")
            .description("解析指定的代码文件")
            .handler(self._handle_parse_code)
            .build()
        )

        # 文档生成工具
        self.server.add_tool(
            ToolRegistration.builder()
            .name("generate_docs")
            .description("生成Markdown文档")
            .handler(self._handle_generate_docs)
            .build()
        )

        # 图表生成工具
        self.server.add_tool(
            ToolRegistration.builder()
            .name("generate_diagrams")
            .description("生成Mermaid图表")
            .handler(self._handle_generate_diagrams)
            .build()
        )

    def register_resources(self):
        """注册资源处理器"""
        # 代码文件资源
        self.server.add_resource(
            ResourceRegistration.builder()
            .uri_pattern("file://code/*")
            .description("访问代码文件")
            .handler(self._handle_code_resource)
            .build()
        )

        # 文档资源
        self.server.add_resource(
            ResourceRegistration.builder()
            .uri_pattern("file://docs/*")
            .description("访问生成的文档")
            .handler(self._handle_doc_resource)
            .build()
        )

    def register_prompts(self):
        """注册提示模板"""
        # 代码分析提示
        self.server.add_prompt(
            PromptRegistration.builder()
            .name("analyze_code")
            .description("分析代码结构和关系")
            .template("请分析以下{language}代码：\n\n{code}\n\n提取关键信息并生成文档大纲。")
            .build()
        )

    def _handle_parse_code(self, request):
        """处理代码解析请求"""
        try:
            file_path = request.get("file_path")
            language = request.get("language")
            # TODO: 实现具体的代码解析逻辑
            return {"success": True, "data": {"parsed": True}}
        except Exception as e:
            self.logger.error(f"代码解析错误: {str(e)}")
            return {"success": False, "error": str(e)}

    def _handle_generate_docs(self, request):
        """处理文档生成请求"""
        try:
            parsed_data = request.get("parsed_data")
            output_format = request.get("format", "markdown")
            # TODO: 实现具体的文档生成逻辑
            return {"success": True, "data": {"generated": True}}
        except Exception as e:
            self.logger.error(f"文档生成错误: {str(e)}")
            return {"success": False, "error": str(e)}

    def _handle_generate_diagrams(self, request):
        """处理图表生成请求"""
        try:
            parsed_data = request.get("parsed_data")
            diagram_type = request.get("type", "class")
            # TODO: 实现具体的图表生成逻辑
            return {"success": True, "data": {"generated": True}}
        except Exception as e:
            self.logger.error(f"图表生成错误: {str(e)}")
            return {"success": False, "error": str(e)}

    def _handle_code_resource(self, request):
        """处理代码文件资源请求"""
        try:
            uri = request.get("uri")
            # TODO: 实现代码文件的读取逻辑
            return {"success": True, "data": {"content": "..."}}
        except Exception as e:
            self.logger.error(f"代码资源访问错误: {str(e)}")
            return {"success": False, "error": str(e)}

    def _handle_doc_resource(self, request):
        """处理文档资源请求"""
        try:
            uri = request.get("uri")
            # TODO: 实现文档文件的读取逻辑
            return {"success": True, "data": {"content": "..."}}
        except Exception as e:
            self.logger.error(f"文档资源访问错误: {str(e)}")
            return {"success": False, "error": str(e)}

    def start(self):
        """启动MCP服务器"""
        try:
            self.register_tools()
            self.register_resources()
            self.register_prompts()
            self.logger.info("MCP服务器启动成功")
            self.server.start()
        except Exception as e:
            self.logger.error(f"服务器启动错误: {str(e)}")
            raise

    def stop(self):
        """停止MCP服务器"""
        try:
            self.server.close()
            self.logger.info("MCP服务器已停止")
        except Exception as e:
            self.logger.error(f"服务器停止错误: {str(e)}")
            raise

if __name__ == "__main__":
    server = CodeDocMcpServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
    except Exception as e:
        logging.error(f"服务器运行错误: {str(e)}")
