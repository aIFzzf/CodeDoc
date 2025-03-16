"""Application configuration for CodeLens MCP Server."""

# Import third-party modules
from mcp.server.fastmcp import FastMCP

# Import local modules
from CodeLens import __version__

# Constants
APP_NAME = "codelens_mcp_server"
APP_DESCRIPTION = "CodeLens MCP Server for code analysis and enhancement."
APP_DEPENDENCIES = [
    "mcp>=1.3.0",
    "httpx>=0.28.1",
    "loguru>=0.7.2",
    "platformdirs>=4.2.0",
]

# Initialize FastMCP server
mcp = FastMCP(
    name=APP_NAME,
    description=APP_DESCRIPTION,
    version=__version__,
    dependencies=APP_DEPENDENCIES,
)
