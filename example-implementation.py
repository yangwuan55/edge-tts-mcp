#!/usr/bin/env python3
"""
Edge-TTS MCP Server 示例实现
"""

import asyncio
import base64
import json
from typing import Dict, List, Any, Optional
import edge_tts
from edge_tts import Communicate, VoicesManager


class EdgeTTSMCPServer:
    """Edge-TTS MCP Server 实现"""
    
    def __init__(self):
        self.voices_manager = None
        self.cached_voices = None
    
    async def initialize(self):
        """初始化服务器"""
        self.voices_manager = await VoicesManager.create()
        
    async def text_to_speech(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """文本转语音工具"""
        text = arguments.get("text")
        voice = arguments.get("voice", "en-US-EmmaMultilingualNeural")
        rate = arguments.get("rate", "+0%")
        volume = arguments.get("volume", "+0%")
        pitch = arguments.get("pitch", "+0Hz")
        boundary = arguments.get("boundary", "SentenceBoundary")
        
        # 创建 Communicate 实例
        comm = Communicate(
            text=text,
            voice=voice,
            rate=rate,
            volume=volume,
            pitch=pitch,
            boundary=boundary
        )
        
        # 生成音频
        audio_chunks = []
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                audio_chunks.append(chunk["data"])
        
        # 合并音频数据
        audio_data = b"".join(audio_chunks)
        
        return {
            "audio_data": base64.b64encode(audio_data).decode("utf-8"),
            "metadata": {
                "voice": voice,
                "text_length": len(text),
                "audio_duration": len(audio_data) / 16000,  # 估算时长
                "format": "mp3"
            }
        }
    
    async def list_voices(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """语音列表查询工具"""
        if self.cached_voices is None:
            voices = await edge_tts.list_voices()
            self.cached_voices = voices
        else:
            voices = self.cached_voices
        
        # 应用过滤器
        locale_filter = arguments.get("locale")
        gender_filter = arguments.get("gender")
        name_pattern = arguments.get("name_pattern")
        
        filtered_voices = []
        for voice in voices:
            if locale_filter and voice.get("Locale") != locale_filter:
                continue
            if gender_filter and voice.get("Gender") != gender_filter:
                continue
            if name_pattern and name_pattern not in voice.get("Name", ""):
                continue
            
            filtered_voices.append({
                "name": voice.get("Name"),
                "short_name": voice.get("ShortName"),
                "gender": voice.get("Gender"),
                "locale": voice.get("Locale"),
                "supported_styles": voice.get("StyleList", []),
                "voice_type": voice.get("VoiceType", "Neural")
            })
        
        return {
            "voices": filtered_voices,
            "total_count": len(filtered_voices)
        }
    
    async def get_voice_info(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """语音详细信息查询工具"""
        voice_name = arguments.get("voice_name")
        
        if self.cached_voices is None:
            voices = await edge_tts.list_voices()
            self.cached_voices = voices
        else:
            voices = self.cached_voices
        
        voice_info = None
        for voice in voices:
            if voice.get("ShortName") == voice_name or voice.get("Name") == voice_name:
                voice_info = voice
                break
        
        if not voice_info:
            raise ValueError(f"Voice not found: {voice_name}")
        
        return {
            "voice": {
                "name": voice_info.get("Name"),
                "short_name": voice_info.get("ShortName"),
                "gender": voice_info.get("Gender"),
                "locale": voice_info.get("Locale"),
                "supported_styles": voice_info.get("StyleList", []),
                "voice_type": voice_info.get("VoiceType", "Neural"),
                "status": voice_info.get("Status", "Available"),
                "words_per_minute": voice_info.get("WordsPerMinute", "150-200")
            }
        }
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """处理工具调用"""
        if tool_name == "text_to_speech":
            return await self.text_to_speech(arguments)
        elif tool_name == "list_voices":
            return await self.list_voices(arguments)
        elif tool_name == "get_voice_info":
            return await self.get_voice_info(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")


async def main():
    """主函数 - 测试示例"""
    server = EdgeTTSMCPServer()
    await server.initialize()
    
    # 测试语音列表
    print("=== 测试语音列表 ===")
    voices_result = await server.list_voices({"locale": "zh-CN"})
    print(f"找到 {voices_result['total_count']} 个中文语音:")
    for voice in voices_result["voices"][:5]:  # 显示前5个
        print(f"  - {voice['short_name']}: {voice['name']}")
    
    # 测试文本转语音
    print("\n=== 测试文本转语音 ===")
    try:
        tts_result = await server.text_to_speech({
            "text": "你好，这是一个测试",
            "voice": "zh-CN-XiaoxiaoNeural"
        })
        print(f"音频生成成功，长度: {len(tts_result['audio_data'])} 字符")
        print(f"元数据: {tts_result['metadata']}")
    except Exception as e:
        print(f"文本转语音错误: {e}")
    
    # 测试语音信息
    print("\n=== 测试语音信息 ===")
    try:
        voice_info = await server.get_voice_info({
            "voice_name": "zh-CN-XiaoxiaoNeural"
        })
        print(f"语音信息: {json.dumps(voice_info, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"获取语音信息错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())