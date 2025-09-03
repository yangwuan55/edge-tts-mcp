# Edge-TTS MCP Server

[中文文档](README_CN.md) | English Documentation

基于 Microsoft Edge TTS 服务的 MCP (Model Context Protocol) 服务器，提供文本转语音功能。

## Claude Code MCP Configuration

Add the following MCP server configuration to your Claude Code settings:

```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "python",
      "args": [
        "/absolute/path/to/edge-tts/main.py"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/edge-tts/src"
      }
    }
  }
}
```

**Configuration Example** (modify with your actual path):

```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "python",
      "args": [
        "/Users/ymr/github/edge-tts/main.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/ymr/github/edge-tts/src"
      }
    }
  }
}
```

**Windows Configuration**:
```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "python",
      "args": [
        "C:\\path\\to\\edge-tts\\main.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\edge-tts\\src"
      }
    }
  }
}
```

**Using Virtual Environment** (recommended):
```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "/path/to/venv/bin/python",
      "args": [
        "/path/to/edge-tts/main.py"
      ]
    }
  }
}
```

**Configuration File Example**: The project root provides `claude-mcp-config.json` with a complete configuration example.

### Configuration Details

1. **command**: Path to Python interpreter
2. **args**: Path to main program file
3. **env**: Environment variables to ensure Python can find source code
4. **disabled**: Whether to disable this server (default false)
5. **autoStart**: Whether to auto-start (default true)

### Configuration Location

Claude Code MCP configuration file is typically located at:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Add the configuration to the `mcpServers` section of the file.

## 功能特性

- ✅ 文本转语音（支持多种语言和语音）
- ✅ 语音列表查询（支持按语言、性别过滤）
- ✅ 音频文件保存
- ✅ 语音详细信息查询
- ✅ 字幕生成（SRT格式）
- ✅ 完整的 MCP 协议支持
- ✅ 严格的参数验证
- ✅ 详细的错误处理

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务器

```bash
# 方式1: 使用主脚本
python main.py

# 方式2: 直接运行服务器
python -m src.server
```

## 工具列表

### 1. text_to_speech
将文本转换为语音音频

**参数:**
- `text`: 要转换的文本内容（必填）
- `voice`: 语音名称（默认: en-US-EmmaMultilingualNeural）
- `rate`: 语速调整（默认: +0%）
- `volume`: 音量调整（默认: +0%）
- `pitch`: 音调调整（默认: +0Hz）
- `boundary`: 边界类型（默认: SentenceBoundary）
- `format`: 输出格式（默认: mp3）

### 2. list_voices
查询可用的语音列表

**参数:**
- `locale`: 语言区域过滤
- `gender`: 性别过滤（Male/Female）
- `name_pattern`: 名称模式匹配

### 3. save_audio
将音频数据保存到文件

**参数:**
- `audio_data`: base64编码的音频数据（必填）
- `filename`: 保存的文件名（必填）
- `format`: 文件格式（默认: mp3）

### 4. get_voice_info
获取特定语音的详细信息

**参数:**
- `voice_name`: 语音名称（必填）

### 5. generate_subtitles
生成语音的字幕文件

**参数:**
- `text`: 文本内容（必填）
- `voice`: 语音名称（默认: en-US-EmmaMultilingualNeural）
- `subtitle_format`: 字幕格式（默认: srt）
- `boundary_type`: 边界类型（默认: SentenceBoundary）

## 使用示例

### 命令行测试

```bash
# 查询中文语音列表
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "list_voices",
    "arguments": {
      "locale": "zh-CN"
    }
  }'

# 文本转语音
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "text_to_speech",
    "arguments": {
      "text": "你好，世界！",
      "voice": "zh-CN-XiaoxiaoNeural"
    }
  }'
```

### Python 客户端示例

```python
import asyncio
import aiohttp
import json

async def test_tts():
    async with aiohttp.ClientSession() as session:
        # 文本转语音
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "text_to_speech",
                "arguments": {
                    "text": "Hello, world!",
                    "voice": "en-US-JennyNeural"
                }
            }
        }
        
        async with session.post("http://localhost:8000", json=payload) as response:
            result = await response.json()
            print(json.dumps(result, indent=2))

asyncio.run(test_tts())
```

## 错误代码

- `1001`: 验证错误
- `1002`: 语音不存在
- `1003`: 参数错误
- `1004`: 网络错误
- `1005`: 音频生成错误

## 配置说明

编辑 `config/server_config.yaml` 文件进行配置：

```yaml
server:
  host: localhost
  port: 8000
  log_level: INFO

defaults:
  voice: en-US-EmmaMultilingualNeural
  rate: +0%
  volume: +0%
  pitch: +0Hz
```

## 支持的语音

支持 85 种语言的 585 个不同语音，包括：

- 中文: `zh-CN-XiaoxiaoNeural`, `zh-CN-YunyangNeural`
- 英文: `en-US-JennyNeural`, `en-US-EmmaMultilingualNeural`
- 日文: `ja-JP-NanamiNeural`
- 韩文: `ko-KR-SunHiNeural`

使用 `list_voices` 工具查看完整列表。

## 开发说明

项目结构：
```
edge-tts-mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py          # MCP Server 主文件
│   ├── tools.py           # 工具实现
│   ├── models.py          # 数据模型
│   └── utils.py           # 工具函数
├── config/
│   └── server_config.yaml # 服务器配置
├── requirements.txt       # 依赖文件
├── README.md
└── main.py               # 启动脚本
```

## 许可证

MIT License