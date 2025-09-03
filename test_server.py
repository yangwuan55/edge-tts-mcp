#!/usr/bin/env python3
"""
Edge-TTS MCP Server 测试脚本
"""

import asyncio
import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils import EdgeTTSClient
from src.tools import EdgeTTSTools


async def test_voices():
    """测试语音列表功能"""
    print("=== 测试语音列表功能 ===")
    
    async with EdgeTTSClient() as client:
        try:
            # 获取所有语音
            voices = await client.get_voices()
            print(f"总语音数量: {len(voices)}")
            
            # 过滤中文语音
            chinese_voices = await client.filter_voices(locale="zh-CN")
            print(f"中文语音数量: {len(chinese_voices)}")
            
            for voice in chinese_voices[:3]:  # 显示前3个
                print(f"  - {voice.name} ({voice.gender})")
                
        except Exception as e:
            print(f"测试失败: {e}")


async def test_tts():
    """测试文本转语音功能"""
    print("\n=== 测试文本转语音功能 ===")
    
    tools = EdgeTTSTools()
    
    try:
        # 测试中文TTS
        from src.models import TextToSpeechRequest
        request = TextToSpeechRequest(
            text="你好，世界！这是一个测试。",
            voice="zh-CN-XiaoxiaoNeural"
        )
        result = await tools.text_to_speech(request)
        
        if "error" in result:
            print(f"TTS失败: {result['error']['message']}")
        else:
            print(f"TTS成功: 生成 {len(result['audio_data'])} 字节的音频数据")
            print(f"元数据: {result['metadata']}")
            
    except Exception as e:
        print(f"测试失败: {e}")


async def test_voice_info():
    """测试语音信息查询"""
    print("\n=== 测试语音信息查询 ===")
    
    tools = EdgeTTSTools()
    
    try:
        result = await tools.get_voice_info("zh-CN-XiaoxiaoNeural")
        
        if "error" in result:
            print(f"查询失败: {result['error']['message']}")
        else:
            print(f"语音信息: {result['voice']}")
            
    except Exception as e:
        print(f"测试失败: {e}")


async def main():
    """主测试函数"""
    print("开始测试 Edge-TTS MCP Server 功能...")
    
    await test_voices()
    await test_tts()
    await test_voice_info()
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    asyncio.run(main())