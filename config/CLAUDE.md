[根目录](../CLAUDE.md) > **config**

# config 模块文档

## 模块职责

服务器配置模块，包含 Edge-TTS MCP Server 的所有配置选项：
- 服务器网络配置
- 默认语音参数
- 功能限制设置
- 错误代码定义

## 配置文件

### 主要配置文件
- **server_config.yaml**: 服务器主配置文件

### 配置位置
```
config/
└── server_config.yaml
```

## 配置详情

### 服务器配置 (server)
```yaml
server:
  host: localhost    # 服务器监听地址
  port: 8000         # 服务器监听端口
  log_level: INFO    # 日志级别
```

### 默认参数 (defaults)
```yaml
defaults:
  voice: en-US-EmmaMultilingualNeural  # 默认语音
  rate: +0%                            # 默认语速
  volume: +0%                          # 默认音量  
  pitch: +0Hz                          # 默认音调
  boundary: SentenceBoundary           # 默认边界类型
  format: mp3                          # 默认输出格式
```

### 缓存配置 (cache)
```yaml
cache:
  enabled: true      # 是否启用缓存
  ttl: 3600          # 缓存有效期（秒）
```

### 功能限制 (limits)
```yaml
limits:
  max_text_length: 5000           # 最大文本长度
  max_concurrent_requests: 10     # 最大并发请求数
```

### 支持格式
```yaml
supported_formats:
  - mp3
  - wav  
  - ogg

boundary_types:
  - WordBoundary
  - SentenceBoundary
```

### 错误代码
```yaml
error_codes:
  validation_error: 1001        # 验证错误
  voice_not_found: 1002         # 语音不存在
  parameter_error: 1003         # 参数错误
  network_error: 1004           # 网络错误
  audio_generation_error: 1005  # 音频生成错误
```

## 配置使用

### 读取配置
配置在服务器启动时自动加载，通过各模块引用：
- `server.py`: 服务器网络配置
- `tools.py`: 默认参数和限制
- `models.py`: 验证规则

### 修改配置
1. 编辑 `server_config.yaml` 文件
2. 重启服务器使配置生效

## 相关文件清单

- `server_config.yaml` - 主配置文件 (41行)

## 变更记录 (Changelog)

### 2025-09-03
- 创建配置模块文档
- 记录所有配置选项
- 说明配置使用方法

---

*本文档由 Claude Code 自动生成，最后更新于 2025-09-03*