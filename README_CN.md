# Edge-TTS MCP Server 中文文档

基于 Microsoft Edge TTS 服务的 MCP (Model Context Protocol) 服务器，提供高质量的文本转语音功能。

## 🌟 特性

- ✅ **多语言支持**: 85种语言，585个不同语音
- ✅ **中文优化**: 支持31个中文语音，包括多种风格
- ✅ **实时语音**: 低延迟文本转语音生成
- ✅ **参数调节**: 语速、音量、音调精细控制
- ✅ **字幕生成**: 自动生成SRT格式字幕文件
- ✅ **文件保存**: 支持MP3、WAV、OGG多种格式
- ✅ **MCP协议**: 完整的Model Context Protocol支持

## 🚀 快速开始

### 一键启动
```bash
# 给脚本添加执行权限
chmod +x start_server.sh

# 一键启动
./start_server.sh
```

### 手动启动
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
python main.py
```

### 测试功能
```bash
# 运行功能测试
python test_server.py

# 运行客户端测试(需要先启动服务器)
python scripts/test_client.py
```

### Claude Code MCP 配置

在 Claude Code 的配置文件中添加以下 MCP 服务器配置：

```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "python",
      "args": [
        "/绝对路径/到/edge-tts/main.py"
      ],
      "env": {
        "PYTHONPATH": "/绝对路径/到/edge-tts/src"
      }
    }
  }
}
```

**配置示例**（根据您的实际路径修改）：

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

**Windows 系统配置**：
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

**使用虚拟环境**（推荐）：
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

**配置文件示例**：项目根目录提供了 `claude-mcp-config.json` 文件，包含完整的配置示例。

### 配置说明

1. **command**: 使用的 Python 解释器路径
2. **args**: 主程序文件路径
3. **env**: 环境变量，确保 Python 能找到源码
4. **disabled**: 是否禁用该服务器（默认 false）
5. **autoStart**: 是否自动启动（默认 true）

### 配置位置

Claude Code 的 MCP 配置文件通常位于：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

将配置添加到文件的 `mcpServers` 部分即可。

## 📖 使用指南

### 1. 基本使用

#### 查询语音列表
```bash
# 查询所有中文语音
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "list_voices",
    "arguments": {
      "locale": "zh-CN"
    }
  }'
```

#### 文本转语音
```bash
# 中文文本转语音
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "text_to_speech",
    "arguments": {
      "text": "你好，欢迎使用Edge-TTS服务",
      "voice": "zh-CN-XiaoxiaoNeural",
      "rate": "+10%",
      "volume": "+5%"
    }
  }'
```

### 2. Python客户端示例

```python
import asyncio
import aiohttp
import json
import base64

async def text_to_speech_example():
    """文本转语音示例"""
    async with aiohttp.ClientSession() as session:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "text_to_speech",
                "arguments": {
                    "text": "这是一个测试文本",
                    "voice": "zh-CN-XiaoxiaoNeural",
                    "rate": "+0%",
                    "volume": "+0%"
                }
            }
        }
        
        async with session.post("http://localhost:8000", json=payload) as response:
            result = await response.json()
            
            if "result" in result:
                # 解码音频数据
                audio_data = base64.b64decode(result["result"]["audio_data"])
                
                # 保存为MP3文件
                with open("output.mp3", "wb") as f:
                    f.write(audio_data)
                
                print("✅ 音频生成成功！")
                print(f"📊 元数据: {result['result']['metadata']}")
            else:
                print(f"❌ 错误: {result['error']}")

asyncio.run(text_to_speech_example())
```

### 3. 支持的语音

#### 常用中文语音
- `zh-CN-XiaoxiaoNeural` - 晓晓（女性，多种风格）
- `zh-CN-YunxiNeural` - 云希（男性）
- `zh-CN-YunjianNeural` - 云健（男性）
- `zh-CN-XiaoyiNeural` - 晓怡（女性）
- `zh-TW-HsiaoChenNeural` - 晓辰（台湾女性）
- `zh-HK-HiuMaanNeural` - 晓雯（香港女性）

#### 英文语音
- `en-US-JennyNeural` - 珍妮（女性）
- `en-US-EmmaMultilingualNeural` - 艾玛（多语言女性）
- `en-US-GuyNeural` - 盖伊（男性）

## 🛠️ API接口

### 工具列表

#### 1. text_to_speech - 文本转语音
```json
{
  "text": "要转换的文本",
  "voice": "语音名称",
  "rate": "语速(+10%)",
  "volume": "音量(+5%)",
  "pitch": "音调(+50Hz)",
  "boundary": "SentenceBoundary",
  "format": "mp3"
}
```

#### 2. list_voices - 语音列表查询
```json
{
  "locale": "zh-CN",
  "gender": "Female",
  "name_pattern": "Xiao"
}
```

#### 3. save_audio - 保存音频文件
```json
{
  "audio_data": "base64编码数据",
  "filename": "output.mp3",
  "format": "mp3"
}
```

#### 4. get_voice_info - 语音信息查询
```json
{
  "voice_name": "zh-CN-XiaoxiaoNeural"
}
```

#### 5. generate_subtitles - 生成字幕
```json
{
  "text": "文本内容",
  "voice": "zh-CN-XiaoxiaoNeural",
  "subtitle_format": "srt"
}
```

## ⚙️ 配置说明

编辑 `config/server_config.yaml`:

```yaml
server:
  host: localhost
  port: 8000
  log_level: INFO

defaults:
  voice: zh-CN-XiaoxiaoNeural  # 默认中文语音
  rate: +0%
  volume: +0%
  pitch: +0Hz

# 支持的语言格式和边界类型
supported_formats:
  - mp3
  - wav
  - ogg

boundary_types:
  - WordBoundary
  - SentenceBoundary
```

## 🐛 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   # 使用清华镜像源
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. **端口被占用**
   ```bash
   # 修改config/server_config.yaml中的端口号
   port: 8080
   ```

3. **语音列表为空**
   ```bash
   # 检查网络连接
   # 重新启动服务器
   ```

### 错误代码
- `1001`: 参数验证错误
- `1002`: 语音不存在
- `1003`: 参数格式错误
- `1004`: 网络连接错误
- `1005`: 音频生成错误

## 📁 项目结构

```
edge-tts/
├── src/                 # 源代码目录
│   ├── server.py       # MCP服务器主程序
│   ├── tools.py        # 工具实现
│   ├── models.py       # 数据模型(Pydantic)
│   └── utils.py        # 工具类
├── config/             # 配置文件
│   └── server_config.yaml
├── scripts/            # 脚本文件
│   ├── start_server.sh # 一键启动脚本
│   ├── install_deps.sh # 依赖安装脚本
│   └── test_client.py  # 客户端测试脚本
├── requirements.txt    # Python依赖
├── README.md          # 英文文档
├── README_CN.md       # 中文文档
├── main.py            # 主入口文件
└── test_server.py     # 功能测试
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [edge-tts](https://github.com/rany2/edge-tts) - 提供核心TTS功能
- [MCP协议](https://modelcontextprotocol.io/) - Model Context Protocol标准
- Microsoft Edge - 提供高质量的TTS服务

---

**享受高质量的文本转语音服务吧！** 🎉