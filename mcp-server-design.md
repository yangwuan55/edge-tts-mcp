# Edge-TTS MCP Server 设计方案

## 1. MCP Server 核心功能设计

### 支持的 Tools

1. **text_to_speech** - 文本转语音工具
2. **list_voices** - 语音列表查询工具
3. **save_audio** - 音频文件保存工具
4. **get_voice_info** - 语音详细信息查询工具
5. **generate_subtitles** - 字幕生成工具

## 2. 工具详细设计

### 2.1 text_to_speech 工具

**功能**: 将文本转换为语音音频

**参数**:
```json
{
  "text": "要转换的文本内容",
  "voice": "语音名称 (可选，默认: en-US-EmmaMultilingualNeural)",
  "rate": "语速 (可选，默认: +0%)",
  "volume": "音量 (可选，默认: +0%)",
  "pitch": "音调 (可选，默认: +0Hz)",
  "boundary": "边界类型 (可选，默认: SentenceBoundary)",
  "format": "输出格式 (可选，默认: mp3)"
}
```

**返回**:
```json
{
  "audio_data": "base64编码的音频数据",
  "metadata": {
    "voice": "使用的语音名称",
    "text_length": 文本长度,
    "audio_duration": 音频时长(秒),
    "format": "音频格式"
  }
}
```

### 2.2 list_voices 工具

**功能**: 查询可用的语音列表

**参数**:
```json
{
  "locale": "语言区域过滤 (可选)",
  "gender": "性别过滤 (可选: Male/Female)",
  "name_pattern": "名称模式匹配 (可选)"
}
```

**返回**:
```json
{
  "voices": [
    {
      "name": "语音全名",
      "short_name": "语音短名",
      "gender": "性别",
      "locale": "语言区域",
      "supported_styles": "支持的风格",
      "voice_type": "语音类型"
    }
  ],
  "total_count": 总数量
}
```

### 2.3 save_audio 工具

**功能**: 将音频数据保存到文件

**参数**:
```json
{
  "audio_data": "base64编码的音频数据",
  "filename": "保存的文件名",
  "format": "文件格式 (可选，默认: mp3)"
}
```

**返回**:
```json
{
  "success": true,
  "file_path": "保存的文件路径",
  "file_size": 文件大小
}
```

### 2.4 get_voice_info 工具

**功能**: 获取特定语音的详细信息

**参数**:
```json
{
  "voice_name": "语音名称"
}
```

**返回**:
```json
{
  "voice": {
    "name": "语音全名",
    "short_name": "语音短名", 
    "gender": "性别",
    "locale": "语言区域",
    "supported_styles": ["风格列表"],
    "voice_type": "语音类型",
    "status": "状态",
    "words_per_minute": "语速范围"
  }
}
```

### 2.5 generate_subtitles 工具

**功能**: 生成语音的字幕文件

**参数**:
```json
{
  "text": "文本内容",
  "voice": "语音名称",
  "subtitle_format": "字幕格式 (可选，默认: srt)",
  "boundary_type": "边界类型 (可选，默认: SentenceBoundary)"
}
```

**返回**:
```json
{
  "subtitles": "字幕内容",
  "format": "字幕格式",
  "segment_count": 分段数量
}
```

## 3. 架构设计

### 3.1 项目结构
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

### 3.2 依赖管理

**requirements.txt**:
```
edge-tts>=7.2.0
mcp>=1.0.0
aiohttp>=3.8.0
pydantic>=2.0.0
pyyaml>=6.0.0
```

### 3.3 配置方式

**server_config.yaml**:
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
  boundary: SentenceBoundary
  format: mp3

cache:
  enabled: true
  ttl: 3600  # 1小时

limits:
  max_text_length: 5000
  max_concurrent_requests: 10
```

## 4. 接口设计

### 4.1 MCP 协议兼容性

服务器将实现 MCP (Model Context Protocol) 标准协议，支持:
- Tools 发现和调用
- 资源管理
- 进度通知
- 错误处理

### 4.2 JSON Schema 定义

每个工具都有严格的 JSON Schema 验证:

**text_to_speech schema**:
```json
{
  "type": "object",
  "properties": {
    "text": {"type": "string", "minLength": 1},
    "voice": {"type": "string", "default": "en-US-EmmaMultilingualNeural"},
    "rate": {"type": "string", "pattern": "^[+-]?\\d+%$"},
    "volume": {"type": "string", "pattern": "^[+-]?\\d+%$"},
    "pitch": {"type": "string", "pattern": "^[+-]?\\d+Hz$"},
    "boundary": {"type": "string", "enum": ["WordBoundary", "SentenceBoundary"]},
    "format": {"type": "string", "enum": ["mp3", "wav", "ogg"]}
  },
  "required": ["text"]
}
```

### 4.3 请求响应格式

**请求示例**:
```json
{
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
```

**响应示例**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "audio_data": "UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGA...",
    "metadata": {
      "voice": "en-US-JennyNeural",
      "text_length": 13,
      "audio_duration": 2.5,
      "format": "mp3"
    }
  }
}
```

## 5. 错误处理

### 5.1 错误代码

- `1001`: 文本过长错误
- `1002`: 语音不存在错误  
- `1003`: 参数验证错误
- `1004`: 网络连接错误
- `1005`: 音频生成错误

### 5.2 错误响应格式
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": 1002,
    "message": "Voice not found: invalid-voice",
    "data": {
      "available_voices": ["en-US-EmmaNeural", "en-US-JennyNeural"]
    }
  }
}
```

## 6. 性能优化

- 语音列表缓存
- 连接池管理
- 音频数据流式处理
- 请求限流控制

## 7. 安全考虑

- 输入验证和清理
- 请求频率限制
- 敏感数据过滤
- 文件路径安全检查