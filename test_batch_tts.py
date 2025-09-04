#!/usr/bin/env python3
"""
批量文本转语音功能测试脚本
"""

import asyncio
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.tools import EdgeTTSTools
from src.models import BatchTextToSpeechRequest, VoiceSegment

async def test_batch_tts():
    """测试批量文本转语音功能"""
    tools = EdgeTTSTools()
    
    # 创建测试数据
    segments = [
        VoiceSegment(
            text="你好，这是第一个语音段",
            voice="zh-CN-XiaoxiaoNeural",
            rate="+0%",
            volume="+0%",
            pitch="+0Hz",
            boundary="SentenceBoundary"
        ),
        VoiceSegment(
            text="Hello, this is the second voice segment",
            voice="en-US-EmmaMultilingualNeural", 
            rate="+10%",
            volume="+0%",
            pitch="+0Hz",
            boundary="SentenceBoundary"
        ),
        VoiceSegment(
            text="こんにちは、これは三番目の音声セグメントです",
            voice="ja-JP-NanamiNeural",
            rate="+0%",
            volume="+0%", 
            pitch="+0Hz",
            boundary="SentenceBoundary"
        )
    ]
    
    request = BatchTextToSpeechRequest(
        segments=segments,
        format="mp3",
        output_filename="test_batch_output.mp3"
    )
    
    print("开始测试批量文本转语音功能...")
    print(f"语音段数量: {len(segments)}")
    
    try:
        # 调用批量处理功能
        result = await tools.batch_text_to_speech(request)
        
        if "error" in result:
            print(f"❌ 处理失败: {result['error']}")
            return False
        
        print("✅ 批量处理成功!")
        print(f"文件路径: {result.get('file_path')}")
        print(f"文件大小: {result.get('file_size')} 字节")
        print(f"处理统计: {result.get('processed_count')}/{result.get('segment_count')} 成功")
        
        if result.get('failed_count', 0) > 0:
            print(f"失败详情: {json.dumps(result.get('errors', []), indent=2, ensure_ascii=False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中发生异常: {str(e)}")
        return False

async def test_single_tts():
    """测试单个语音段处理"""
    tools = EdgeTTSTools()
    
    # 单个语音段测试
    segments = [
        VoiceSegment(
            text="这是一个单独的测试语音段",
            voice="zh-CN-XiaoxiaoNeural"
        )
    ]
    
    request = BatchTextToSpeechRequest(
        segments=segments,
        format="mp3"
    )
    
    print("\n开始测试单个语音段处理...")
    
    try:
        result = await tools.batch_text_to_speech(request)
        
        if "error" in result:
            print(f"❌ 单个语音段处理失败: {result['error']}")
            return False
        
        print("✅ 单个语音段处理成功!")
        print(f"文件路径: {result.get('file_path')}")
        return True
        
    except Exception as e:
        print(f"❌ 单个语音段测试异常: {str(e)}")
        return False

async def main():
    """主测试函数"""
    print("=" * 50)
    print("Edge-TTS MCP Server 批量文本转语音功能测试")
    print("=" * 50)
    
    # 测试批量处理
    batch_success = await test_batch_tts()
    
    # 测试单个处理
    single_success = await test_single_tts()
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print(f"批量处理: {'✅ 成功' if batch_success else '❌ 失败'}")
    print(f"单个处理: {'✅ 成功' if single_success else '❌ 失败'}")
    
    if batch_success and single_success:
        print("🎉 所有测试通过!")
    else:
        print("💥 部分测试失败!")
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())