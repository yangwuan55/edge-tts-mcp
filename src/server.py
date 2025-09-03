import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server

from tools import EdgeTTSTools
from models import (
    TextToSpeechRequest,
    ListVoicesRequest,
    SaveAudioRequest,
    GenerateSubtitlesRequest
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EdgeTTSServer:
    """Edge-TTS MCP Server"""
    
    def __init__(self):
        self.server = FastMCP("edge-tts-server")
        self.tools = EdgeTTSTools()
        
        # 注册工具处理函数
        self.server.tool("text_to_speech")(self.handle_text_to_speech)
        self.server.tool("list_voices")(self.handle_list_voices)
        self.server.tool("save_audio")(self.handle_save_audio)
        self.server.tool("get_voice_info")(self.handle_get_voice_info)
        self.server.tool("generate_subtitles")(self.handle_generate_subtitles)
        
    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """初始化处理"""
        logger.info("Edge-TTS MCP Server 初始化")
        return {
            "serverInfo": {
                "name": "edge-tts-server",
                "version": "0.1.0"
            },
            "capabilities": {
                "tools": {},
                "resources": {}
            }
        }
    
    async def handle_text_to_speech(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """处理文本转语音请求"""
        try:
            # 验证参数
            request = TextToSpeechRequest(**arguments)
            
            # 调用工具
            result = await self.tools.text_to_speech(request)
            
            # 检查是否有错误
            if "error" in result:
                return self._create_error_response(result["error"])
            
            return result
            
        except Exception as e:
            logger.error(f"文本转语音处理失败: {str(e)}")
            return self._create_error_response({
                "code": 1003,
                "message": f"参数验证失败: {str(e)}"
            })
    
    async def handle_list_voices(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """处理语音列表查询请求"""
        try:
            # 验证参数
            request = ListVoicesRequest(**arguments)
            
            # 调用工具
            result = await self.tools.list_voices(request)
            
            # 检查是否有错误
            if "error" in result:
                return self._create_error_response(result["error"])
            
            return result
            
        except Exception as e:
            logger.error(f"语音列表查询失败: {str(e)}")
            return self._create_error_response({
                "code": 1003,
                "message": f"参数验证失败: {str(e)}"
            })
    
    async def handle_save_audio(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """处理保存音频请求"""
        try:
            # 验证参数
            request = SaveAudioRequest(**arguments)
            
            # 调用工具
            result = await self.tools.save_audio(request)
            
            # 检查是否有错误
            if "error" in result:
                return self._create_error_response(result["error"])
            
            return result
            
        except Exception as e:
            logger.error(f"保存音频失败: {str(e)}")
            return self._create_error_response({
                "code": 1003,
                "message": f"参数验证失败: {str(e)}"
            })
    
    async def handle_get_voice_info(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """处理语音信息查询请求"""
        try:
            voice_name = arguments.get("voice_name")
            if not voice_name:
                return self._create_error_response({
                    "code": 1003,
                    "message": "voice_name 参数必填"
                })
            
            # 调用工具
            result = await self.tools.get_voice_info(voice_name)
            
            # 检查是否有错误
            if "error" in result:
                return self._create_error_response(result["error"])
            
            return result
            
        except Exception as e:
            logger.error(f"语音信息查询失败: {str(e)}")
            return self._create_error_response({
                "code": 1003,
                "message": f"参数验证失败: {str(e)}"
            })
    
    async def handle_generate_subtitles(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """处理生成字幕请求"""
        try:
            # 验证参数
            request = GenerateSubtitlesRequest(**arguments)
            
            # 调用工具
            result = await self.tools.generate_subtitles(request)
            
            # 检查是否有错误
            if "error" in result:
                return self._create_error_response(result["error"])
            
            return result
            
        except Exception as e:
            logger.error(f"生成字幕失败: {str(e)}")
            return self._create_error_response({
                "code": 1003,
                "message": f"参数验证失败: {str(e)}"
            })
    
    def _create_error_response(self, error_info: Dict[str, Any]) -> Dict[str, Any]:
        """创建错误响应"""
        return {
            "error": {
                "code": error_info.get("code", 1000),
                "message": error_info.get("message", "未知错误"),
                "data": error_info.get("data", {})
            }
        }
    
    def run(self):
        """运行服务器"""
        logger.info("启动 Edge-TTS MCP Server...")
        
        try:
            # FastMCP 使用简化的运行方式
            self.server.run()
        except Exception as e:
            logger.error(f"服务器运行错误: {e}")
            raise


def main():
    """主函数"""
    server = EdgeTTSServer()
    
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"服务器运行失败: {str(e)}")


if __name__ == "__main__":
    main()