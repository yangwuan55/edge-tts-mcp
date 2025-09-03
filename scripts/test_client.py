#!/usr/bin/env python3
"""
Edge-TTS MCP Server 客户端测试脚本
"""

import asyncio
import aiohttp
import json
import base64
from pathlib import Path


async def test_list_voices():
    """测试语音列表查询"""
    print("🔊 测试语音列表查询...")
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "list_voices",
            "arguments": {
                "locale": "zh-CN"
            }
        }
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post("http://localhost:8000", json=payload) as response:
                result = await response.json()
                
                if "result" in result:
                    voices = result["result"]["voices"]
                    print(f"✅ 找到 {len(voices)} 个中文语音:")
                    for voice in voices[:5]:  # 显示前5个
                        print(f"   - {voice['name']} ({voice['gender']})")
                    if len(voices) > 5:
                        print(f"   - ... 和 {len(voices) - 5} 个其他语音")
                else:
                    print(f"❌ 错误: {result['error']}")
                    
        except Exception as e:
            print(f"❌ 请求失败: {e}")


async def test_text_to_speech():
    """测试文本转语音"""
    print("\n🎵 测试文本转语音...")
    
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "text_to_speech",
            "arguments": {
                "text": "你好，欢迎使用Edge-TTS语音服务！这是一个测试语音。",
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": "+0%",
                "volume": "+0%"
            }
        }
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post("http://localhost:8000", json=payload) as response:
                result = await response.json()
                
                if "result" in result:
                    audio_data = base64.b64decode(result["result"]["audio_data"])
                    metadata = result["result"]["metadata"]
                    
                    # 保存音频文件
                    with open("test_output.mp3", "wb") as f:
                        f.write(audio_data)
                    
                    print("✅ 语音生成成功！")
                    print(f"   📁 文件: test_output.mp3")
                    print(f"   ⏱️  时长: {metadata['audio_duration']}秒")
                    print(f"   📝 文本长度: {metadata['text_length']}字符")
                    print(f"   🎙️  语音: {metadata['voice']}")
                    
                else:
                    print(f"❌ 错误: {result['error']}")
                    
        except Exception as e:
            print(f"❌ 请求失败: {e}")


async def test_voice_info():
    """测试语音信息查询"""
    print("\n📋 测试语音信息查询...")
    
    payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "get_voice_info",
            "arguments": {
                "voice_name": "zh-CN-XiaoxiaoNeural"
            }
        }
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post("http://localhost:8000", json=payload) as response:
                result = await response.json()
                
                if "result" in result:
                    voice_info = result["result"]["voice"]
                    print("✅ 语音信息查询成功:")
                    print(f"   🎙️  名称: {voice_info['name']}")
                    print(f"   🔤 短名: {voice_info['short_name']}")
                    print(f"   👤 性别: {voice_info['gender']}")
                    print(f"   🌐 语言: {voice_info['locale']}")
                    print(f"   🎭 支持风格: {len(voice_info['supported_styles'])}种")
                    
                else:
                    print(f"❌ 错误: {result['error']}")
                    
        except Exception as e:
            print(f"❌ 请求失败: {e}")


async def main():
    """主测试函数"""
    print("🧪 Edge-TTS MCP Server 客户端测试")
    print("=" * 50)
    
    # 检查服务器是否运行
    print("🔍 检查服务器连接...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000", timeout=2) as response:
                if response.status == 200:
                    print("✅ 服务器连接正常")
                else:
                    print("❌ 服务器未响应")
                    print("请先启动服务器: python main.py")
                    return
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        print("请先启动服务器: python main.py")
        return
    
    # 运行测试
    await test_list_voices()
    await test_text_to_speech()
    await test_voice_info()
    
    print("\n" + "=" * 50)
    print("🎉 所有测试完成！")
    print("📁 生成的音频文件: test_output.mp3")


if __name__ == "__main__":
    asyncio.run(main())