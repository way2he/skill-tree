"""
LLM 统一接口层 - Ollama 适配器
适配 ollama/ 目录
"""

import json
from typing import Any, Generator

from .base import BaseLLMAdapter
from ..exceptions import LLMError


class OllamaLLMAdapter(BaseLLMAdapter):
    """Ollama LLM 适配器
    
    适配 ollama/ 目录的客户端
    """
    
    def __init__(self, inner_client: Any, provider_name: str = "ollama"):
        """初始化 Ollama 适配器
        
        Args:
            inner_client: 被适配的 Ollama 客户端
            provider_name: 提供者名称
        """
        super().__init__(inner_client)
        self._provider_name = provider_name
        # 尝试从客户端获取默认模型
        self._default_model = getattr(
            inner_client, 
            'default_model', 
            'llama2'
        )
    
    @property
    def provider_name(self) -> str:
        """提供者名称"""
        return self._provider_name
    
    @property
    def default_model(self) -> str:
        """默认模型名称"""
        return self._default_model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        try:
            return self._inner_client.generate(prompt, **kwargs)
        except Exception as e:
            if isinstance(e, LLMError):
                raise
            raise LLMError(
                f"Ollama 调用失败: {str(e)}",
                provider=self.provider_name,
                cause=e
            )
    
    def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str:
        """生成 JSON 格式的文本
        
        Args:
            prompt: 输入提示词
            schema: JSON Schema（可选）
            **kwargs: 其他参数
            
        Returns:
            JSON 格式的字符串
        """
        try:
            result = self._inner_client.generate_json(prompt, schema, **kwargs)
            # 确保返回的是字符串
            if not isinstance(result, str):
                return json.dumps(result, ensure_ascii=False)
            return result
        except Exception as e:
            if isinstance(e, LLMError):
                raise
            raise LLMError(
                f"Ollama JSON 调用失败: {str(e)}",
                provider=self.provider_name,
                cause=e
            )
    
    def generate_stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """流式生成文本
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Yields:
            生成的文本片段
        """
        try:
            # 尝试调用客户端的流式方法
            if hasattr(self._inner_client, 'generate_stream'):
                yield from self._inner_client.generate_stream(prompt, **kwargs)
            else:
                # 如果不支持流式，回退到普通生成
                yield self.generate(prompt, **kwargs)
        except Exception as e:
            if isinstance(e, LLMError):
                raise
            raise LLMError(
                f"Ollama 流式调用失败: {str(e)}",
                provider=self.provider_name,
                cause=e
            )
