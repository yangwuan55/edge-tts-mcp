#!/bin/bash

# Edge-TTS MCP Server 依赖安装脚本

echo "📦 安装 Edge-TTS MCP Server 依赖..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3，请先安装 Python 3.7+"
    exit 1
fi

# 使用国内镜像源加速下载
PIP_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"

echo "🔧 安装核心依赖..."
pip install -i $PIP_MIRROR edge-tts mcp

echo "🔧 安装Web框架依赖..."
pip install -i $PIP_MIRROR aiohttp pydantic pyyaml uvicorn fastapi

echo "✅ 所有依赖安装完成！"
echo ""
echo "🚀 启动服务器:"
echo "  python main.py"
echo ""
echo "📋 或者使用一键启动脚本:"
echo "  chmod +x scripts/start_server.sh"
echo "  ./scripts/start_server.sh"