[根目录](../CLAUDE.md) > **src**

# src 模块文档

## 模块职责

核心代码模块，包含 Edge-TTS MCP Server 的所有业务逻辑实现：
- MCP 服务器主程序
- 工具函数实现
- 数据模型定义
- 工具函数和客户端

## 入口与启动

### 主要入口文件
- **server.py**: MCP 服务器主程序，包含 `EdgeTTSServer` 类
- **main.py**: 项目启动脚本（位于根目录）

### 启动方式
```python
# 通过主脚本启动
python ../main.py

# 直接运行服务器模块
python -m src.server
```

## 对外接口

### MCP 工具列表
服务器提供以下 6 个 MCP 工具：

1. **text_to_speech** - 文本转语音
   - 输入: 文本内容、语音参数
   - 输出: 音频文件引用

2. **batch_text_to_speech** - 批量文本转语音
   - 输入: 语音段配置数组，每个元素可独立配置
   - 输出: 合成的音频文件引用和处理统计

3. **list_voices** - 语音列表查询
   - 输入: 过滤条件（语言、性别）
   - 输出: 语音列表

4. **save_audio** - 保存音频
   - 输入: base64音频数据、文件名
   - 输出: 文件保存结果

5. **get_voice_info** - 语音信息查询
   - 输入: 语音名称
   - 输出: 语音详细信息

6. **generate_subtitles** - 生成字幕
   - 输入: 文本内容、语音参数
   - 输出: SRT格式字幕

## 关键依赖与配置

### 核心依赖
- `edge-tts>=7.2.0`: Microsoft Edge TTS 服务
- `mcp>=1.0.0`: Model Context Protocol 支持
- `pydantic>=2.0.0`: 数据验证和模型定义
- `aiohttp>=3.8.0`: 异步 HTTP 客户端

### 配置依赖
- 语音参数默认值在 `../config/server_config.yaml` 中配置
- 错误代码定义在配置文件中

## 数据模型

### 主要数据模型（models.py）
- `TextToSpeechRequest`: 文本转语音请求
- `BatchTextToSpeechRequest`: 批量文本转语音请求
- `VoiceSegment`: 语音段配置模型
- `ListVoicesRequest`: 语音列表查询请求  
- `VoiceInfo`: 语音信息模型
- `SaveAudioRequest`: 保存音频请求
- `GenerateSubtitlesRequest`: 生成字幕请求
- `ErrorResponse`: 错误响应模型

### 验证规则
- 文本长度限制: 1-5000 字符
- 语音参数格式验证（百分比、Hz等）
- 文件格式验证（mp3, wav, ogg）

## 测试与质量

### 测试覆盖
- **单元测试**: `test_server.py` 测试核心功能
- **集成测试**: 需要手动验证 MCP 协议

### 质量工具
- 类型注解全覆盖
- Pydantic 数据验证
- 详细的错误处理和日志记录

## 常见问题 (FAQ)

### Q: 如何添加新的语音工具？
A: 在 `tools.py` 中添加工具方法，在 `server.py` 中注册，在 `models.py` 中添加对应的请求模型。

### Q: 音频文件保存位置？
A: 默认保存在当前工作目录，文件名格式: `tts_{timestamp}_{text_hash}.{format}`

### Q: 如何扩展支持的语音格式？
A: 修改 `tools.py` 中的 `supported_formats` 列表和对应的验证逻辑。

## 相关文件清单

- `server.py` - MCP 服务器主程序 (183行)
- `tools.py` - 工具实现 (240行) 
- `models.py` - 数据模型 (83行)
- `utils.py` - 工具函数 (178行)
- `__init__.py` - 模块初始化

## 变更记录 (Changelog)

### 2025-09-03
- 创建模块文档
- 记录核心接口和依赖
- 添加数据模型说明

---

*本文档由 Claude Code 自动生成，最后更新于 2025-09-03*