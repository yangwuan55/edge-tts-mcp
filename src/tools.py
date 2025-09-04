from typing import Dict, Any, List, Optional
import asyncio
import base64
import os
from .models import (
    TextToSpeechRequest, 
    ListVoicesRequest, 
    AudioResponse, 
    SaveAudioRequest,
    GenerateSubtitlesRequest,
    VoiceInfo,
    ErrorResponse,
    BatchTextToSpeechRequest,
    VoiceSegment
)
from .utils import EdgeTTSClient


class EdgeTTSTools:
    """Edge-TTS MCP 工具类"""
    
    def __init__(self):
        self.client = EdgeTTSClient()
        self.supported_formats = ['mp3', 'wav', 'ogg']

    async def text_to_speech(self, request: TextToSpeechRequest) -> Dict[str, Any]:
        """文本转语音工具"""
        try:
            # 验证语音是否存在
            voice_info = await self.client.get_voice_info(request.voice)
            if not voice_info:
                return self._create_error_response(1002, f"语音不存在: {request.voice}")
            
            # 生成唯一文件名
            import hashlib
            import time
            timestamp = int(time.time())
            text_hash = hashlib.md5(request.text.encode()).hexdigest()[:8]
            filename = f"tts_{timestamp}_{text_hash}.{request.format}"
            
            # 生成音频并直接保存到文件
            audio_data = await self.client.text_to_speech(
                text=request.text,
                voice=request.voice,
                rate=request.rate,
                volume=request.volume,
                pitch=request.pitch,
                boundary=request.boundary
            )
            
            # 保存到文件
            with open(filename, 'wb') as f:
                f.write(audio_data)
            
            # 计算文件大小
            file_size = len(audio_data)
            
            # 返回简洁的文件信息，避免在控制台输出大量数据
            return {
                "success": True,
                "file_path": filename,
                "file_size": file_size,
                "message": f"音频文件已生成: {filename} ({file_size} 字节)",
                "_type": "file_reference"  # 标记为文件引用类型
            }
            
        except Exception as e:
            return self._create_error_response(1005, f"音频生成失败: {str(e)}")

    async def list_voices(self, request: ListVoicesRequest) -> Dict[str, Any]:
        """语音列表查询工具"""
        try:
            # 如果没有过滤条件，返回摘要信息避免大量数据
            if not any([request.locale, request.gender, request.name_pattern]):
                summary = await self.client.get_voice_list_summary()
                return summary
            
            # 有过滤条件时返回过滤后的结果
            voices = await self.client.filter_voices(
                locale=request.locale,
                gender=request.gender,
                name_pattern=request.name_pattern
            )
            
            return {
                "voices": [voice.dict() for voice in voices],
                "total_count": len(voices)
            }
            
        except Exception as e:
            return self._create_error_response(1004, f"获取语音列表失败: {str(e)}")

    async def save_audio(self, request: SaveAudioRequest) -> Dict[str, Any]:
        """保存音频工具"""
        try:
            # 验证文件格式
            if request.format not in self.supported_formats:
                return self._create_error_response(1003, f"不支持的格式: {request.format}")
            
            # 转换base64为音频数据
            audio_data = self.client.base64_to_audio(request.audio_data)
            
            # 确保文件名有正确的扩展名
            filename = request.filename
            if not filename.lower().endswith(f'.{request.format}'):
                filename = f"{filename}.{request.format}"
            
            # 保存文件
            with open(filename, 'wb') as f:
                f.write(audio_data)
            
            # 获取文件大小
            file_size = os.path.getsize(filename)
            
            return {
                "success": True,
                "file_path": os.path.abspath(filename),
                "file_size": file_size
            }
            
        except Exception as e:
            return self._create_error_response(1005, f"保存音频失败: {str(e)}")

    async def get_voice_info(self, voice_name: str) -> Dict[str, Any]:
        """语音详细信息查询工具"""
        try:
            voice_info = await self.client.get_voice_info(voice_name)
            
            if not voice_info:
                return self._create_error_response(1002, f"语音不存在: {voice_name}")
            
            return {"voice": voice_info.dict()}
            
        except Exception as e:
            return self._create_error_response(1004, f"获取语音信息失败: {str(e)}")

    async def generate_subtitles(self, request: GenerateSubtitlesRequest) -> Dict[str, Any]:
        """生成字幕工具"""
        try:
            # 验证语音是否存在
            voice_info = await self.client.get_voice_info(request.voice)
            if not voice_info:
                return self._create_error_response(1002, f"语音不存在: {request.voice}")
            
            # 验证字幕格式
            if request.subtitle_format.lower() != 'srt':
                return self._create_error_response(1003, "目前仅支持SRT格式")
            
            # 生成字幕
            subtitles = await self.client.generate_subtitles(
                text=request.text,
                voice=request.voice,
                boundary=request.boundary_type
            )
            
            # 计算分段数量
            segment_count = subtitles.count('-->')
            
            return {
                "subtitles": subtitles,
                "format": request.subtitle_format,
                "segment_count": segment_count
            }
            
        except Exception as e:
            return self._create_error_response(1005, f"生成字幕失败: {str(e)}")

    async def batch_text_to_speech(self, request: BatchTextToSpeechRequest) -> Dict[str, Any]:
        """批量文本转语音工具"""
        try:
            import tempfile
            import os
            from pydub import AudioSegment
            import hashlib
            import time
            
            # 生成唯一文件名
            timestamp = int(time.time())
            segments_hash = hashlib.md5(str([seg.text for seg in request.segments]).encode()).hexdigest()[:8]
            filename = request.output_filename or f"batch_tts_{timestamp}_{segments_hash}.{request.format}"
            
            # 处理每个语音段
            processed_segments = []
            errors = []
            
            for i, segment in enumerate(request.segments):
                try:
                    # 验证语音是否存在
                    voice_info = await self.client.get_voice_info(segment.voice)
                    if not voice_info:
                        errors.append({
                            "index": i,
                            "error": f"语音不存在: {segment.voice}"
                        })
                        continue
                    
                    # 生成单个语音段的音频
                    audio_data = await self.client.text_to_speech(
                        text=segment.text,
                        voice=segment.voice,
                        rate=segment.rate,
                        volume=segment.volume,
                        pitch=segment.pitch,
                        boundary=segment.boundary
                    )
                    
                    processed_segments.append({
                        "index": i,
                        "audio_data": audio_data,
                        "text": segment.text,
                        "voice": segment.voice
                    })
                    
                except Exception as e:
                    errors.append({
                        "index": i,
                        "error": f"处理语音段失败: {str(e)}"
                    })
            
            # 如果没有成功处理的语音段，返回错误
            if not processed_segments:
                return self._create_error_response(1005, "所有语音段处理失败", {"errors": errors})
            
            # 合并音频文件
            if len(processed_segments) == 1:
                # 只有一个语音段，直接保存
                audio_data = processed_segments[0]["audio_data"]
                with open(filename, 'wb') as f:
                    f.write(audio_data)
            else:
                # 多个语音段，需要合并
                combined_audio = None
                
                for segment in processed_segments:
                    # 创建临时文件
                    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                        temp_file.write(segment["audio_data"])
                        temp_filename = temp_file.name
                    
                    try:
                        # 加载音频段
                        audio_segment = AudioSegment.from_file(temp_filename, format="mp3")
                        
                        if combined_audio is None:
                            combined_audio = audio_segment
                        else:
                            combined_audio += audio_segment
                        
                    finally:
                        # 清理临时文件
                        os.unlink(temp_filename)
                
                # 保存合并后的音频
                if combined_audio:
                    combined_audio.export(filename, format=request.format)
                
            # 计算文件大小
            file_size = os.path.getsize(filename)
            
            return {
                "success": True,
                "file_path": os.path.abspath(filename),
                "file_size": file_size,
                "segment_count": len(request.segments),
                "processed_count": len(processed_segments),
                "failed_count": len(errors),
                "errors": errors,
                "message": f"批量音频文件已生成: {filename} ({file_size} 字节)",
                "_type": "file_reference"
            }
            
        except Exception as e:
            return self._create_error_response(1005, f"批量音频生成失败: {str(e)}")

    def _create_error_response(self, code: int, message: str, data: Optional[dict] = None) -> Dict[str, Any]:
        """创建错误响应"""
        return {
            "error": {
                "code": code,
                "message": message,
                "data": data or {}
            }
        }

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """获取工具schema"""
        return [
            {
                "name": "text_to_speech",
                "description": "将文本转换为语音音频",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "要转换的文本内容"},
                        "voice": {"type": "string", "description": "语音名称", "default": "en-US-EmmaMultilingualNeural"},
                        "rate": {"type": "string", "description": "语速调整", "default": "+0%"},
                        "volume": {"type": "string", "description": "音量调整", "default": "+0%"},
                        "pitch": {"type": "string", "description": "音调调整", "default": "+0Hz"},
                        "boundary": {"type": "string", "description": "边界类型", "default": "SentenceBoundary"},
                        "format": {"type": "string", "description": "输出格式", "default": "mp3"}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "batch_text_to_speech",
                "description": "批量文本转语音，支持多个语音配置合成一个音频文件",
                "inputSchema": {
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
                            "description": "语音段配置列表",
                            "minItems": 1,
                            "maxItems": 20
                        },
                        "format": {"type": "string", "description": "输出格式", "default": "mp3"},
                        "output_filename": {"type": "string", "description": "输出文件名（可选）"}
                    },
                    "required": ["segments"]
                }
            },
            {
                "name": "list_voices",
                "description": "查询可用的语音列表",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "locale": {"type": "string", "description": "语言区域过滤"},
                        "gender": {"type": "string", "description": "性别过滤", "enum": ["Male", "Female"]},
                        "name_pattern": {"type": "string", "description": "名称模式匹配"}
                    }
                }
            },
            {
                "name": "save_audio",
                "description": "将音频数据保存到文件",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "audio_data": {"type": "string", "description": "base64编码的音频数据"},
                        "filename": {"type": "string", "description": "保存的文件名"},
                        "format": {"type": "string", "description": "文件格式", "default": "mp3"}
                    },
                    "required": ["audio_data", "filename"]
                }
            },
            {
                "name": "get_voice_info",
                "description": "获取特定语音的详细信息",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "voice_name": {"type": "string", "description": "语音名称"}
                    },
                    "required": ["voice_name"]
                }
            },
            {
                "name": "generate_subtitles",
                "description": "生成语音的字幕文件",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "文本内容"},
                        "voice": {"type": "string", "description": "语音名称", "default": "en-US-EmmaMultilingualNeural"},
                        "subtitle_format": {"type": "string", "description": "字幕格式", "default": "srt"},
                        "boundary_type": {"type": "string", "description": "边界类型", "default": "SentenceBoundary"}
                    },
                    "required": ["text"]
                }
            }
        ]