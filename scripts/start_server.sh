#!/bin/bash

# Edge-TTS MCP Server 一键启动脚本

echo "🚀 启动 Edge-TTS MCP Server..."

# 检查Python是否安装
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python，请先安装 Python 3.7+"
    exit 1
fi

# 优先使用 python3
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# 检查依赖是否安装
if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误: 未找到 requirements.txt"
    exit 1
fi

echo "📦 检查依赖安装..."
if ! $PYTHON_CMD -c "import edge_tts" 2>/dev/null; then
    echo "安装 edge-tts 依赖..."
    pip install edge-tts
fi

if ! $PYTHON_CMD -c "import mcp" 2>/dev/null; then
    echo "安装 mcp 依赖..."
    pip install mcp
fi

# 检查其他依赖
REQUIRED_PACKAGES=("aiohttp" "pydantic" "pyyaml" "uvicorn" "fastapi")
for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! $PYTHON_CMD -c "import $package" 2>/dev/null; then
        echo "安装 $package..."
        pip install $package
    fi
done

echo "✅ 所有依赖已就绪"
echo "🔊 启动 Edge-TTS MCP Server..."

# 启动服务器
$PYTHON_CMD main.py