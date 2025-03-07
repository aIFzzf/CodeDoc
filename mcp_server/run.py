from server import CodeDocMcpServer
import argparse
import logging

def main():
    parser = argparse.ArgumentParser(description='启动代码文档MCP服务器')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    args = parser.parse_args()

    # 配置日志级别
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level)

    # 启动服务器
    server = CodeDocMcpServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
    except Exception as e:
        logging.error(f"服务器运行错误: {str(e)}")
        raise

if __name__ == "__main__":
    main()
