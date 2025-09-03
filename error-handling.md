# Edge-TTS MCP Server 错误处理方案

## 1. 错误代码体系

### 1.1 通用错误 (1000-1099)
- `1000`: 未知错误
- `1001`: 无效的JSON-RPC请求
- `1002`: 方法不存在
- `1003`: 参数验证失败
- `1004`: 内部服务器错误
- `1005`: 服务不可用

### 1.2 工具相关错误 (1100-1199)
- `1101`: 文本过长错误
- `1102`: 语音不存在错误
- `1103`: 语音参数无效
- `1104`: 音频生成失败
- `1105`: 文件保存失败
- `1106`: 字幕生成失败

### 1.3 资源相关错误 (1200-1299)
- `1201`: 语音列表获取失败
- `1202`: 网络连接超时
- `1203`: 服务配额超限
- `1204`: 缓存错误

### 1.4 安全相关错误 (1300-1399)
- `1301`: 认证失败
- `1302`: 权限不足
- `1303`: 输入验证失败
- `1304`: 文件路径不安全

## 2. 错误响应格式

### 2.1 标准错误响应
```json
{
  "jsonrpc": "2.0",
  "id": "request-id",
  "error": {
    "code": 错误代码,
    "message": "错误描述",
    "data": {
      "details": "详细错误信息",
      "suggestion": "解决建议",
      "context": {}
    }
  }
}
```

### 2.2 具体错误示例

**语音不存在错误**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": 1102,
    "message": "Voice not found: invalid-voice-name",
    "data": {
      "details": "The requested voice 'invalid-voice-name' does not exist",
      "suggestion": "Use list_voices tool to get available voices",
      "context": {
        "requested_voice": "invalid-voice-name",
        "available_locales": ["en-US", "zh-CN", "ja-JP"]
      }
    }
  }
}
```

**文本过长错误**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": 1101,
    "message": "Text too long",
    "data": {
      "details": "Text length 6000 exceeds maximum limit of 5000 characters",
      "suggestion": "Split text into smaller chunks",
      "context": {
        "text_length": 6000,
        "max_allowed": 5000,
        "excess": 1000
      }
    }
  }
}
```

## 3. 异常处理策略

### 3.1 输入验证异常
```python
class ValidationError(Exception):
    """参数验证错误"""
    def __init__(self, field: str, message: str, value: Any = None):
        self.field = field
        self.message = message
        self.value = value
        super().__init__(f"{field}: {message}")

# 使用示例
def validate_text_length(text: str, max_length: int = 5000):
    if len(text) > max_length:
        raise ValidationError(
            "text", 
            f"Text exceeds maximum length of {max_length} characters",
            len(text)
        )
```

### 3.2 语音相关异常
```python
class VoiceNotFoundError(Exception):
    """语音不存在错误"""
    def __init__(self, voice_name: str, available_voices: List[str] = None):
        self.voice_name = voice_name
        self.available_voices = available_voices or []
        super().__init__(f"Voice not found: {voice_name}")

class VoiceParameterError(Exception):
    """语音参数错误"""
    def __init__(self, parameter: str, value: Any, valid_values: List[Any] = None):
        self.parameter = parameter
        self.value = value
        self.valid_values = valid_values
        super().__init__(f"Invalid {parameter}: {value}")
```

### 3.3 网络相关异常
```python
class NetworkError(Exception):
    """网络错误"""
    def __init__(self, operation: str, url: str, status_code: int = None):
        self.operation = operation
        self.url = url
        self.status_code = status_code
        message = f"Network error during {operation} to {url}"
        if status_code:
            message += f" (status: {status_code})"
        super().__init__(message)

class TimeoutError(Exception):
    """超时错误"""
    def __init__(self, operation: str, timeout: float):
        self.operation = operation
        self.timeout = timeout
        super().__init__(f"{operation} timed out after {timeout}s")
```

## 4. 错误处理中间件

### 4.1 全局异常处理器
```python
import logging
from typing import Dict, Any
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

app = FastAPI()

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "jsonrpc": "2.0",
            "id": request.state.request_id,
            "error": {
                "code": 1003,
                "message": f"Validation error: {exc.field}",
                "data": {
                    "details": exc.message,
                    "field": exc.field,
                    "value": exc.value
                }
            }
        }
    )

@app.exception_handler(VoiceNotFoundError)
async def voice_not_found_handler(request: Request, exc: VoiceNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "jsonrpc": "2.0",
            "id": request.state.request_id,
            "error": {
                "code": 1102,
                "message": f"Voice not found: {exc.voice_name}",
                "data": {
                    "details": f"The voice '{exc.voice_name}' is not available",
                    "suggestion": "Use list_voices to get available voices",
                    "available_voices": exc.available_voices[:10]  # 只返回前10个
                }
            }
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "jsonrpc": "2.0",
            "id": request.state.request_id,
            "error": {
                "code": 1004,
                "message": "Internal server error",
                "data": {
                    "details": "An unexpected error occurred",
                    "suggestion": "Please try again later"
                }
            }
        }
    )
```

### 4.2 错误日志记录
```python
def setup_logging():
    """配置结构化日志记录"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("server.log"),
            logging.StreamHandler()
        ]
    )

class StructuredLogger:
    """结构化日志记录器"""
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log_error(self, error_code: int, message: str, context: Dict[str, Any] = None):
        """记录错误日志"""
        log_data = {
            "error_code": error_code,
            "message": message,
            "context": context or {}
        }
        self.logger.error(json.dumps(log_data))
```

## 5. 客户端错误处理建议

### 5.1 重试策略
```python
def with_retry(func, max_retries=3, backoff_factor=0.5):
    """带重试的函数调用"""
    async def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except (NetworkError, TimeoutError) as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = backoff_factor * (2 ** attempt)
                await asyncio.sleep(wait_time)
            except Exception as e:
                raise
    return wrapper
```

### 5.2 错误恢复
```python
async def safe_text_to_speech(text: str, voice: str, fallback_voice: str = None):
    """安全的文本转语音，支持回退"""
    try:
        return await text_to_speech(text, voice)
    except VoiceNotFoundError:
        if fallback_voice:
            return await text_to_speech(text, fallback_voice)
        raise
    except TextTooLongError:
        # 分割文本并分批处理
        chunks = split_text(text, max_length=2000)
        results = []
        for chunk in chunks:
            results.append(await text_to_speech(chunk, voice))
        return combine_audio_results(results)
```

## 6. 监控和告警

### 6.1 错误率监控
```python
class ErrorMetrics:
    """错误指标监控"""
    def __init__(self):
        self.error_counts = defaultdict(int)
        self.total_requests = 0
    
    def record_error(self, error_code: int):
        """记录错误"""
        self.error_counts[error_code] += 1
        self.total_requests += 1
    
    def get_error_rate(self) -> float:
        """获取错误率"""
        if self.total_requests == 0:
            return 0.0
        total_errors = sum(self.error_counts.values())
        return total_errors / self.total_requests
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取指标数据"""
        return {
            "total_requests": self.total_requests,
            "total_errors": sum(self.error_counts.values()),
            "error_rate": self.get_error_rate(),
            "error_breakdown": dict(self.error_counts)
        }
```

### 6.2 告警规则
- 错误率 > 5% 持续5分钟
- 特定错误代码频繁出现
- 响应时间超过阈值
- 服务不可用时间超过1分钟