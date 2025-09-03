#!/usr/bin/env python3
"""
Edge-TTS MCP Server 启动脚本

使用方式:
python main.py  # 启动服务器
"""

import asyncio
import logging
import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.server import EdgeTTSServer


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """主函数"""
    logger.info("正在启动 Edge-TTS MCP Server...")
    
    try:
        server = EdgeTTSServer()
        server.run()
    except KeyboardInterrupt:
        logger.info("服务器已正常停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()