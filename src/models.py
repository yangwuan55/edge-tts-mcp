from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
import re


class VoiceSegment(BaseModel):
    """语音段配置模型"""
    text: str = Field(..., min_length=1, max_length=5000, description="要转换的文本内容")
    voice: Optional[str] = Field("en-US-EmmaMultilingualNeural", description="语音名称")
    rate: Optional[str] = Field("+0%", description="语速调整")
    volume: Optional[str] = Field("+0%", description="音量调整")
    pitch: Optional[str] = Field("+0Hz", description="音调调整")
    boundary: Optional[str] = Field("SentenceBoundary", description="边界类型")

    @validator('rate', 'volume')
    def validate_percentage(cls, v):
        if v is not None and not re.match(r'^[+-]?\d+%$', v):
            raise ValueError('必须为百分比格式，如 +10% 或 -5%')
        return v

    @validator('pitch')
    def validate_pitch(cls, v):
        if v is not None and not re.match(r'^[+-]?\d+Hz$', v):
            raise ValueError('必须为Hz格式，如 +50Hz 或 -20Hz')
        return v

    @validator('boundary')
    def validate_boundary(cls, v):
        if v not in ['WordBoundary', 'SentenceBoundary']:
            raise ValueError('边界类型必须是 WordBoundary 或 SentenceBoundary')
        return v


class TextToSpeechRequest(BaseModel):
    """文本转语音请求模型"""
    text: str = Field(..., min_length=1, max_length=5000, description="要转换的文本内容")
    voice: Optional[str] = Field("en-US-EmmaMultilingualNeural", description="语音名称")
    rate: Optional[str] = Field("+0%", description="语速调整")
    volume: Optional[str] = Field("+0%", description="音量调整")
    pitch: Optional[str] = Field("+0Hz", description="音调调整")
    boundary: Optional[str] = Field("SentenceBoundary", description="边界类型")
    format: Optional[str] = Field("mp3", description="输出格式")

    @validator('rate', 'volume')
    def validate_percentage(cls, v):
        if v is not None and not re.match(r'^[+-]?\d+%$', v):
            raise ValueError('必须为百分比格式，如 +10% 或 -5%')
        return v

    @validator('pitch')
    def validate_pitch(cls, v):
        if v is not None and not re.match(r'^[+-]?\d+Hz$', v):
            raise ValueError('必须为Hz格式，如 +50Hz 或 -20Hz')
        return v

    @validator('boundary')
    def validate_boundary(cls, v):
        if v not in ['WordBoundary', 'SentenceBoundary']:
            raise ValueError('边界类型必须是 WordBoundary 或 SentenceBoundary')
        return v

    @validator('format')
    def validate_format(cls, v):
        if v not in ['mp3', 'wav', 'ogg']:
            raise ValueError('格式必须是 mp3, wav 或 ogg')
        return v


class BatchTextToSpeechRequest(BaseModel):
    """批量文本转语音请求模型"""
    segments: List[VoiceSegment] = Field(..., min_items=1, max_items=20, description="语音段配置列表")
    format: Optional[str] = Field("mp3", description="输出格式")
    output_filename: Optional[str] = Field(None, description="输出文件名")

    @validator('format')
    def validate_format(cls, v):
        if v not in ['mp3', 'wav', 'ogg']:
            raise ValueError('格式必须是 mp3, wav 或 ogg')
        return v
    
    @validator('segments')
    def validate_segments(cls, v):
        # 检查总字符数限制
        total_chars = sum(len(segment.text) for segment in v)
        if total_chars > 10000:  # 从配置读取，这里先硬编码
            raise ValueError('批量处理总字符数不能超过10000个字符')
        return v


class ListVoicesRequest(BaseModel):
    """语音列表查询请求模型"""
    locale: Optional[str] = Field(None, description="语言区域过滤")
    gender: Optional[Literal['Male', 'Female']] = Field(None, description="性别过滤")
    name_pattern: Optional[str] = Field(None, description="名称模式匹配")


class VoiceInfo(BaseModel):
    """语音信息模型"""
    name: str
    short_name: str
    gender: str
    locale: str
    supported_styles: List[str]
    voice_type: str


class AudioResponse(BaseModel):
    """音频响应模型"""
    audio_data: str = Field(..., description="base64编码的音频数据")
    metadata: dict = Field(..., description="音频元数据")


class SaveAudioRequest(BaseModel):
    """保存音频请求模型"""
    audio_data: str = Field(..., description="base64编码的音频数据")
    filename: str = Field(..., description="保存的文件名")
    format: Optional[str] = Field("mp3", description="文件格式")


class GenerateSubtitlesRequest(BaseModel):
    """生成字幕请求模型"""
    text: str = Field(..., min_length=1, description="文本内容")
    voice: Optional[str] = Field("en-US-EmmaMultilingualNeural", description="语音名称")
    subtitle_format: Optional[str] = Field("srt", description="字幕格式")
    boundary_type: Optional[str] = Field("SentenceBoundary", description="边界类型")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    code: int
    message: str
    data: Optional[dict] = None