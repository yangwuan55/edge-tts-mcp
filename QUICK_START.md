# 🚀 Edge-TTS MCP Server 快速开始

## 1分钟快速体验

### 第一步：安装依赖
```bash
# 使用一键安装脚本
chmod +x scripts/install_deps.sh
./scripts/install_deps.sh

# 或者手动安装
pip install edge-tts mcp aiohttp pydantic pyyaml uvicorn fastapi
```

### 第二步：启动服务器
```bash
# 使用一键启动脚本
chmod +x scripts/start_server.sh
./scripts/start_server.sh

# 或者手动启动
python main.py
```

### 第三步：测试功能
```bash
# 在新的终端窗口中运行客户端测试
python scripts/test_client.py
```

## 快速验证

服务器启动后，打开新的终端尝试以下命令：

```bash
# 测试中文语音列表
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "list_voices",
    "arguments": {
      "locale": "zh-CN"
    }
  }'

# 生成测试语音
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "text_to_speech",
    "arguments": {
      "text": "你好，Edge-TTS服务已就绪！",
      "voice": "zh-CN-XiaoxiaoNeural"
    }
  }'
```

## 预期结果

✅ 服务器正常启动，监听端口8000  
✅ 能够查询到31个中文语音  
✅ 成功生成MP3音频文件  
✅ 客户端测试全部通过  

## 遇到问题？

1. **端口冲突**: 修改 `config/server_config.yaml` 中的端口号
2. **依赖安装失败**: 使用 `scripts/install_deps.sh` 脚本
3. **网络问题**: 确保可以访问微软TTS服务

详细文档请查看 [README_CN.md](README_CN.md)