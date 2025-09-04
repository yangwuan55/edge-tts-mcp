[根目录](../CLAUDE.md) > **scripts**

# scripts 模块文档

## 模块职责

脚本工具模块，包含 Edge-TTS MCP Server 的辅助脚本：
- 服务器启动脚本
- 依赖安装脚本  
- 客户端测试脚本
- 开发辅助工具

## 脚本列表

### 主要脚本文件

1. **start_server.sh** - 一键启动脚本
   - 检查 Python 环境
   - 自动安装缺失依赖
   - 启动服务器

2. **install_deps.sh** - 依赖安装脚本
   - 使用国内镜像源加速
   - 安装所有必需依赖
   - 提供清晰的安装反馈

3. **test_client.py** - 客户端测试脚本
   - HTTP API 测试客户端
   - 测试所有 MCP 工具功能
   - 生成测试音频文件

## 使用说明

### 启动服务器
```bash
# 使用一键启动脚本（推荐）
chmod +x scripts/start_server.sh
./scripts/start_server.sh

# 或手动启动
python main.py
```

### 安装依赖
```bash
# 使用安装脚本（推荐）
chmod +x scripts/install_deps.sh
./scripts/install_deps.sh

# 或手动安装
pip install -r requirements.txt
```

### 测试功能
```bash
# 使用客户端测试
python scripts/test_client.py

# 或使用单元测试
python test_server.py
```

## 脚本功能详情

### start_server.sh 功能
- ✅ 检查 Python 3.7+ 环境
- ✅ 自动安装 edge-tts 和 mcp 依赖
- ✅ 检查并安装其他必需包
- ✅ 提供友好的进度提示
- ✅ 最终启动服务器

### install_deps.sh 功能  
- ✅ 使用清华镜像源加速下载
- ✅ 分批次安装依赖包
- ✅ 清晰的安装进度显示
- ✅ 安装完成后的使用指引

### test_client.py 功能
- ✅ 测试语音列表查询功能
- ✅ 测试文本转语音功能
- ✅ 测试语音信息查询功能
- ✅ 生成测试音频文件
- ✅ 详细的测试结果输出

## 开发建议

### 添加新脚本
1. 在 `scripts/` 目录下创建新脚本
2. 确保脚本有执行权限 (`chmod +x`)
3. 在文档中记录脚本功能
4. 更新根目录的 CLAUDE.md

### 脚本规范
- 使用 `#!/bin/bash` 或 `#!/usr/bin/env python3`
- 添加详细的注释说明
- 提供错误处理和用户提示
- 保持脚本简洁专注

## 相关文件清单

- `start_server.sh` - 启动脚本 (49行)
- `install_deps.sh` - 安装脚本 (29行)  
- `test_client.py` - 测试客户端 (163行)

## 变更记录 (Changelog)

### 2025-09-03
- 创建脚本模块文档
- 记录所有脚本功能
- 提供使用说明和开发建议

---

*本文档由 Claude Code 自动生成，最后更新于 2025-09-03*