import base64
import asyncio
import aiohttp
from typing import Optional, List, Dict, Any
import json
from models import VoiceInfo


class EdgeTTSClient:
    """Edge-TTS 客户端工具类"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.voices_cache = None
        self.cache_ttl = 3600  # 1小时
        self.last_cache_time = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_voices(self) -> List[Dict[str, Any]]:
        """获取语音列表"""
        try:
            from edge_tts import list_voices
            voices = await list_voices()
            return voices
        except Exception as e:
            raise Exception(f"获取语音列表失败: {str(e)}")

    async def text_to_speech(
        self, 
        text: str, 
        voice: str = "en-US-EmmaMultilingualNeural",
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        boundary: str = "SentenceBoundary"
    ) -> bytes:
        """文本转语音"""
        try:
            from edge_tts import Communicate
            
            communicate = Communicate(
                text=text,
                voice=voice,
                rate=rate,
                volume=volume,
                pitch=pitch,
                boundary=boundary
            )
            
            # 收集所有音频数据
            audio_chunks = []
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_chunks.append(chunk["data"])
            
            # 合并所有音频数据
            audio_data = b''.join(audio_chunks)
            return audio_data
            
        except Exception as e:
            raise Exception(f"文本转语音失败: {str(e)}")

    async def generate_subtitles(
        self,
        text: str,
        voice: str = "en-US-EmmaMultilingualNeural",
        boundary: str = "SentenceBoundary"
    ) -> str:
        """生成字幕"""
        try:
            from edge_tts import Communicate
            
            communicate = Communicate(
                text=text,
                voice=voice,
                boundary=boundary
            )
            
            subtitles = []
            segment_index = 1
            
            async for chunk in communicate.stream():
                if "Boundary" in chunk["type"]:
                    metadata = chunk.get("metadata", {})
                    text_offset = metadata.get("Offset", 0)
                    text_duration = metadata.get("Duration", 0)
                    
                    if text_offset is not None and text_duration is not None:
                        start_time = self._format_timestamp(text_offset / 10000000)  # 转换为秒
                        end_time = self._format_timestamp((text_offset + text_duration) / 10000000)
                        
                        # 提取对应的文本片段
                        text_start = metadata.get("text", {}).get("Offset", 0)
                        text_length = metadata.get("text", {}).get("Length", 0)
                        text_segment = text[text_start:text_start + text_length]
                        
                        subtitles.append(f"{segment_index}\n")
                        subtitles.append(f"{start_time} --> {end_time}\n")
                        subtitles.append(f"{text_segment}\n\n")
                        segment_index += 1
            
            return ''.join(subtitles)
            
        except Exception as e:
            raise Exception(f"生成字幕失败: {str(e)}")

    def _format_timestamp(self, seconds: float) -> str:
        """格式化时间戳为SRT格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')

    def audio_to_base64(self, audio_data: bytes) -> str:
        """音频数据转换为base64"""
        return base64.b64encode(audio_data).decode('utf-8')

    def base64_to_audio(self, base64_data: str) -> bytes:
        """base64转换为音频数据"""
        return base64.b64decode(base64_data)

    async def filter_voices(
        self, 
        locale: Optional[str] = None, 
        gender: Optional[str] = None,
        name_pattern: Optional[str] = None
    ) -> List[VoiceInfo]:
        """过滤语音列表"""
        voices = await self.get_voices()
        
        filtered_voices = []
        for voice in voices:
            # 按语言区域过滤
            if locale and voice.get('Locale', '').lower() != locale.lower():
                continue
                
            # 按性别过滤
            if gender and voice.get('Gender', '').lower() != gender.lower():
                continue
                
            # 按名称模式过滤
            if name_pattern and name_pattern.lower() not in voice.get('Name', '').lower():
                continue
            
            filtered_voices.append(VoiceInfo(
                name=voice.get('Name', ''),
                short_name=voice.get('ShortName', ''),
                gender=voice.get('Gender', ''),
                locale=voice.get('Locale', ''),
                supported_styles=voice.get('StyleList', []),
                voice_type=voice.get('VoiceType', '')
            ))
        
        return filtered_voices

    async def get_voice_info(self, voice_name: str) -> Optional[VoiceInfo]:
        """获取特定语音的详细信息"""
        voices = await self.get_voices()
        
        for voice in voices:
            if voice.get('Name') == voice_name or voice.get('ShortName') == voice_name:
                return VoiceInfo(
                    name=voice.get('Name', ''),
                    short_name=voice.get('ShortName', ''),
                    gender=voice.get('Gender', ''),
                    locale=voice.get('Locale', ''),
                    supported_styles=voice.get('StyleList', []),
                    voice_type=voice.get('VoiceType', '')
                )
        
        return None