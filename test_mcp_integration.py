#!/usr/bin/env python3
"""
MCP服务器集成测试 - 测试批量文本转语音功能
"""

import asyncio
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.server import EdgeTTSServer

def create_test_request():
    """创建测试请求数据"""
    return {
        "segments": [
            {
                "text": "欢迎使用Edge-TTS MCP服务器",
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": "+0%",
                "volume": "+0%",
                "pitch": "+0Hz",
                "boundary": "SentenceBoundary"
            },
            {
                "text": "This is the second voice segment in English",
                "voice": "en-US-EmmaMultilingualNeural",
                "rate": "+10%",
                "volume": "+0%", 
                "pitch": "+0Hz",
                "boundary": "SentenceBoundary"
            },
            {
                "text": "これは日本語の音声セグメントです",
                "voice": "ja-JP-NanamiNeural",
                "rate": "+0%",
                "volume": "+0%",
                "pitch": "+0Hz",
                "boundary": "SentenceBoundary"
            }
        ],
        "format": "mp3",
        "output_filename": "integration_test_output.mp3"
    }

async def test_mcp_integration():
    """测试MCP服务器集成"""
    server = EdgeTTSServer()
    
    # 创建测试请求
    test_request = create_test_request()
    
    print("开始MCP服务器集成测试...")
    print(f"请求数据: {json.dumps(test_request, indent=2, ensure_ascii=False)}")
    
    try:
        # 直接调用处理函数
        result = await server.handle_batch_text_to_speech(test_request)
        
        if "error" in result:
            print(f"❌ MCP处理失败: {result['error']}")
            return False
        
        print("✅ MCP集成测试成功!")
        print(f"生成文件: {result.get('file_path')}")
        print(f"文件大小: {result.get('file_size')} 字节")
        print(f"处理统计: {result.get('processed_count')}/{result.get('segment_count')} 语音段成功")
        
        # 验证文件存在
        file_path = result.get('file_path')
        if file_path and os.path.exists(file_path):
            print(f"✅ 音频文件验证成功: {os.path.getsize(file_path)} 字节")
        else:
            print("❌ 音频文件不存在")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ MCP集成测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_error_cases():
    """测试错误情况"""
    server = EdgeTTSServer()
    
    print("\n开始错误情况测试...")
    
    # 测试1: 空语音段列表
    try:
        result = await server.handle_batch_text_to_speech({"segments": []})
        if "error" in result:
            print("✅ 空语音段列表测试通过")
        else:
            print("❌ 空语音段列表测试失败")
            return False
    except Exception as e:
        print(f"❌ 空语音段列表测试异常: {str(e)}")
        return False
    
    # 测试2: 不存在的语音
    try:
        result = await server.handle_batch_text_to_speech({
            "segments": [{"text": "测试", "voice": "invalid-voice"}]
        })
        if "error" in result:
            print("✅ 无效语音测试通过")
        else:
            print("❌ 无效语音测试失败")
            return False
    except Exception as e:
        print(f"❌ 无效语音测试异常: {str(e)}")
        return False
    
    return True

async def main():
    """主测试函数"""
    print("=" * 60)
    print("Edge-TTS MCP Server 批量文本转语音集成测试")
    print("=" * 60)
    
    # 测试正常功能
    integration_success = await test_mcp_integration()
    
    # 测试错误情况
    error_success = await test_error_cases()
    
    print("\n" + "=" * 60)
    print("集成测试结果汇总:")
    print(f"正常功能测试: {'✅ 成功' if integration_success else '❌ 失败'}")
    print(f"错误情况测试: {'✅ 成功' if error_success else '❌ 失败'}")
    
    if integration_success and error_success:
        print("🎉 所有集成测试通过!")
        print("批量文本转语音功能已成功集成到MCP服务器中")
    else:
        print("💥 部分集成测试失败!")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())