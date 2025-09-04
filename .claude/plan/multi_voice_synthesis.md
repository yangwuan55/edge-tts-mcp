# 多语音合成功能实施规划

## 目标定义

### 业务目标
为 Edge-TTS MCP Server 添加多语音合成功能，支持一次请求输入多个语音配置，每个配置可以独立设置参数，最终合成一个音频文件。

### 技术目标
- 保持与现有 MCP 协议的兼容性
- 提供灵活的语音配置数组输入
- 实现音频文件的顺序合成
- 确保错误处理和参数验证的完整性

## 功能分解

### 1. 核心功能
- ✅ 支持数组形式的语音配置输入
- ✅ 每个语音配置支持独立参数设置
- ✅ 音频文件的顺序合成
- ✅ 统一的输出文件格式

### 2. 接口设计
- ✅ 新的 MCP 工具 `batch_text_to_speech`
- ✅ 向后兼容现有 `text_to_speech` 工具
- ✅ 清晰的输入输出 schema 定义

### 3. 数据处理
- ✅ 多语音配置的验证和解析
- ✅ 音频数据的顺序处理和合并
- ✅ 错误处理和部分成功场景

## 实施步骤

### 阶段一：数据模型设计 (1-2小时)
1. 创建 `BatchTextToSpeechRequest` 模型
2. 创建 `VoiceSegment` 子模型
3. 添加验证规则和默认值

### 阶段二：工具实现 (2-3小时)
1. 在 `tools.py` 中添加 `batch_text_to_speech` 方法
2. 实现多语音的序列化处理
3. 添加音频合成逻辑

### 阶段三：服务器集成 (1-2小时)
1. 在 `server.py` 中注册新工具
2. 添加请求处理函数
3. 更新工具 schema

### 阶段四：测试验证 (1-2小时)
1. 编写单元测试
2. 集成测试验证
3. 错误场景测试

## 接口设计

### 新的 MCP 工具: `batch_text_to_speech`

**输入 Schema:**
```json
{
  "type": "object",
  "properties": {
    "segments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "text": {"type": "string", "description": "要转换的文本内容"},
          "voice": {"type": "string", "description": "语音名称", "default": "en-US-EmmaMultilingualNeural"},
          "rate": {"type": "string", "description": "语速调整", "default": "+0%"},
          "volume": {"type": "string", "description": "音量调整", "default": "+0%"},
          "pitch": {"type": "string", "description": "音调调整", "default": "+0Hz"},
          "boundary": {"type": "string", "description": "边界类型", "default": "SentenceBoundary"}
        },
        "required": ["text"]
      },
      "minItems": 1,
      "maxItems": 20
    },
    "format": {"type": "string", "description": "输出格式", "default": "mp3"},
    "output_filename": {"type": "string", "description": "输出文件名（可选）"}
  },
  "required": ["segments"]
}
```

**输出 Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "file_path": {"type": "string"},
    "file_size": {"type": "number"},
    "segment_count": {"type": "number"},
    "processed_count": {"type": "number"},
    "failed_count": {"type": "number"},
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "index": {"type": "number"},
          "error": {"type": "string"}
        }
      }
    }
  }
}
```

## 数据模型

### 新的数据模型

**BatchTextToSpeechRequest:**
```python
class BatchTextToSpeechRequest(BaseModel):
    segments: List[VoiceSegment]
    format: Optional[str] = Field("mp3", description="输出格式")
    output_filename: Optional[str] = Field(None, description="输出文件名")
```

**VoiceSegment:**
```python
class VoiceSegment(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    voice: Optional[str] = Field("en-US-EmmaMultilingualNeural")
    rate: Optional[str] = Field("+0%")
    volume: Optional[str] = Field("+0%")
    pitch: Optional[str] = Field("+0Hz")
    boundary: Optional[str] = Field("SentenceBoundary")
```

## 依赖分析

### 需要修改的文件
1. **src/models.py** - 添加新的数据模型
2. **src/tools.py** - 添加批量处理工具方法
3. **src/server.py** - 注册新工具和处理函数
4. **config/server_config.yaml** - 添加批量处理限制配置

### 新增依赖
可能需要音频处理库来合并音频文件：
- `pydub` - 用于音频文件合并
- `ffmpeg` - 音频处理依赖（系统级）

## 测试策略

### 单元测试
1. 数据模型验证测试
2. 单个语音段处理测试
3. 多语音段顺序处理测试
4. 错误处理测试

### 集成测试
1. MCP 协议集成测试
2. 音频文件生成验证
3. 性能压力测试

### 验收测试
1. 正常场景：2-3个语音段合成
2. 边界场景：最大数量限制测试
3. 错误场景：部分失败处理

## 验收标准

### 功能完成标准
- ✅ 支持数组形式的语音配置输入
- ✅ 每个语音段可以独立配置参数
- ✅ 生成统一的音频输出文件
- ✅ 提供详细的处理结果统计
- ✅ 完整的错误处理和日志记录

### 质量标准
- ✅ 100% 单元测试覆盖率
- ✅ 集成测试通过率 100%
- ✅ 性能指标符合预期（处理时间 < 30秒/10个语音段）
- ✅ 文档完整性和准确性

## 风险评估

### 技术风险
1. **音频合并兼容性**: 不同格式音频的合并可能存在问题
2. **性能问题**: 大量语音段处理可能导致内存或时间问题
3. **依赖管理**: 新增音频处理库可能增加部署复杂度

### 缓解措施
1. 使用成熟的音频处理库（pydub）
2. 添加合理的数量限制和超时机制
3. 提供清晰的依赖安装说明

## 时间估算

**总工时**: 6-9小时
- 数据模型设计: 1-2小时
- 工具实现: 2-3小时  
- 服务器集成: 1-2小时
- 测试验证: 2小时

## 下一步行动

1. 开始实施数据模型设计
2. 评估音频合并方案的技术可行性
3. 确定最终的技术选型和依赖管理