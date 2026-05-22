"""
LLM 统一接口层 - SDK 适配器
适配官方 SDK 模式：baidu/alibaba/zhipu/google/volcengine/cohere/mistral/groq
"""

import json
from typing import Any, Generator

from .base import BaseLLMAdapter
from ..exceptions import LLMError


class SDKLLMAdapter(BaseLLMAdapter):
    """SDK LLM 适配器
    
    适配官方 SDK 模式的客户端
    处理参数归一化（max_tokens <-> max_output_tokens）
    """
    
    def __init__(self, inner_client: Any, provider_name: str = "sdk"):
        """初始化 SDK 适配器
        
        Args:
            inner_client: 被适配的 SDK 客户端
            provider_name: 提供者名称
        """
        super().__init__(inner_client)
        self._provider_name = provider_name
        # 尝试从客户端获取默认模型
        self._default_model = getattr(inner_client, 'default_model', 'gpt-4')
    
    @property
    def provider_name(self) -> str:
        """提供者名称"""
        return self._provider_name
    
    @property
    def default_model(self) -> str:
        """默认模型名称"""
        return self._default_model
    
    def _normalize_kwargs(self, **kwargs) -> dict:
        """归一化参数字典
        
        处理 max_tokens 和 max_output_tokens 的差异
        
        Args:
            **kwargs: 原始参数
            
        Returns:
            归一化后的参数
        """
        normalized = kwargs.copy()
        
        # 处理 max_tokens <-> max_output_tokens
        if 'max_tokens' in normalized and 'max_output_tokens' not in normalized:
            normalized['max_output_tokens'] = normalized['max_tokens']
        elif 'max_output_tokens' in normalized and 'max_tokens' not in normalized:
            normalized['max_tokens'] = normalized['max_output_tokens']
        
        return normalized
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        try:
            normalized_kwargs = self._normalize_kwargs(**kwargs)
            return self._inner_client.generate(prompt, **normalized_kwargs)
        except Exception as e:
            if isinstance(e, LLMError):
                raise
            raise LLMError(
                f"SDK 调用失败: {str(e)}",
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
            normalized_kwargs = self._normalize_kwargs(**kwargs)
            result = self._inner_client.generate_json(prompt, schema, **normalized_kwargs)
            # 确保返回的是字符串
            if not isinstance(result, str):
                return json.dumps(result, ensure_ascii=False)
            return result
        except Exception as e:
            if isinstance(e, LLMError):
                raise
            raise LLMError(
                f"SDK JSON 调用失败: {str(e)}",
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
            normalized_kwargs = self._normalize_kwargs(**kwargs)
            # 尝试调用客户端的流式方法
            if hasattr(self._inner_client, 'generate_stream'):
                yield from self._inner_client.generate_stream(prompt, **normalized_kwargs)
            else:
                # 如果不支持流式，回退到普通生成
                yield self.generate(prompt, **kwargs)
        except Exception as e:
            if isinstance(e, LLMError):
                raise
            raise LLMError(
                f"SDK 流式调用失败: {str(e)}",
                provider=self.provider_name,
                cause=e
            )
