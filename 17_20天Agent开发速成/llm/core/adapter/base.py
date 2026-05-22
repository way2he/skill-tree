"""
LLM 统一接口层 - 适配器基类
定义了同步和异步适配器的基础接口
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Generator, AsyncGenerator

from ..types import LLMResponse
from ..exceptions import LLMError


class BaseLLMAdapter(ABC):
    """LLM 适配器基类（同步版本）
    
    所有同步适配器的基类，提供了通用的功能和接口
    """
    
    def __init__(self, inner_client: Any):
        """初始化适配器
        
        Args:
            inner_client: 被适配的底层客户端实例
        """
        self._inner_client = inner_client
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """提供者名称（抽象属性）"""
        ...
    
    @property
    @abstractmethod
    def default_model(self) -> str:
        """默认模型名称（抽象属性）"""
        ...
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本（抽象方法）
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        ...
    
    @abstractmethod
    def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str:
        """生成 JSON 格式的文本（抽象方法）
        
        Args:
            prompt: 输入提示词
            schema: JSON Schema（可选）
            **kwargs: 其他参数
            
        Returns:
            JSON 格式的字符串
        """
        ...
    
    def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        """生成文本并返回完整响应（模板方法）
        
        包含计时逻辑
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            完整的 LLM 响应对象
        """
        start_time = time.perf_counter()
        
        try:
            content = self.generate(prompt, **kwargs)
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            return LLMResponse(
                content=content,
                model=kwargs.get('model', self.default_model),
                provider=self.provider_name,
                latency_ms=latency_ms
            )
        except Exception as e:
            if isinstance(e, LLMError):
                raise
            raise LLMError(
                f"调用 {self.provider_name} 失败: {str(e)}",
                provider=self.provider_name,
                cause=e
            )
    
    def generate_stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """流式生成文本（可选实现）
        
        默认抛出 NotImplementedError
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Yields:
            生成的文本片段
        """
        raise NotImplementedError(
            f"{self.provider_name} 适配器不支持流式生成"
        )


class BaseAsyncLLMAdapter(ABC):
    """LLM 适配器基类（异步版本）
    
    所有异步适配器的基类，提供了通用的功能和接口
    """
    
    def __init__(self, inner_client: Any):
        """初始化适配器
        
        Args:
            inner_client: 被适配的底层客户端实例
        """
        self._inner_client = inner_client
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """提供者名称（抽象属性）"""
        ...
    
    @property
    @abstractmethod
    def default_model(self) -> str:
        """默认模型名称（抽象属性）"""
        ...
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """异步生成文本（抽象方法）
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        ...
    
    @abstractmethod
    async def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str:
        """异步生成 JSON 格式的文本（抽象方法）
        
        Args:
            prompt: 输入提示词
            schema: JSON Schema（可选）
            **kwargs: 其他参数
            
        Returns:
            JSON 格式的字符串
        """
        ...
    
    async def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        """异步生成文本并返回完整响应（模板方法）
        
        包含计时逻辑
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            完整的 LLM 响应对象
        """
        start_time = time.perf_counter()
        
        try:
            content = await self.generate(prompt, **kwargs)
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            return LLMResponse(
                content=content,
                model=kwargs.get('model', self.default_model),
                provider=self.provider_name,
                latency_ms=latency_ms
            )
        except Exception as e:
            if isinstance(e, LLMError):
                raise
            raise LLMError(
                f"调用 {self.provider_name} 失败: {str(e)}",
                provider=self.provider_name,
                cause=e
            )
    
    async def generate_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """异步流式生成文本（可选实现）
        
        默认抛出 NotImplementedError
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Yields:
            生成的文本片段
        """
        raise NotImplementedError(
            f"{self.provider_name} 适配器不支持流式生成"
        )
