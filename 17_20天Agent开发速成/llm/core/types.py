"""
LLM 统一接口层 - 类型定义
包含枚举、数据模型和 Protocol 定义
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import (
    Protocol,
    runtime_checkable,
    Optional,
    Dict,
    Any,
    Generator,
    AsyncGenerator
)


class ProviderType(str, Enum):
    """LLM 提供者类型枚举
    
    支持的 13 种提供者类型
    """
    OPENAI = "openai"
    REQUESTS = "requests"
    AIOHTTP = "aiohttp"
    ANTHROPIC = "anthropic"
    BAIDU = "baidu"
    ALIBABA = "alibaba"
    ZHIPU = "zhipu"
    GOOGLE = "google"
    COHERE = "cohere"
    MISTRAL = "mistral"
    GROQ = "groq"
    VOLCENGINE = "volcengine"
    OLLAMA = "ollama"


class CircuitState(str, Enum):
    """熔断器状态枚举
    
    熔断器的三种状态
    """
    CLOSED = "closed"       # 关闭状态：正常请求
    OPEN = "open"           # 打开状态：拒绝请求
    HALF_OPEN = "half_open" # 半开状态：试探请求


@dataclass
class LLMRequest:
    """LLM 请求数据模型
    
    封装了所有 LLM 请求参数
    """
    prompt: str
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    """LLM 响应数据模型
    
    封装了 LLM 响应的所有信息
    """
    content: str
    model: Optional[str] = None
    provider: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    finish_reason: Optional[str] = None
    latency_ms: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class LLMProvider(Protocol):
    """LLM 提供者 Protocol（同步版本）
    
    定义了 LLM 提供者需要实现的接口
    使用 Protocol 而不是 ABC，现有客户端无需修改继承关系
    """
    
    @property
    def provider_name(self) -> str:
        """提供者名称"""
        ...
    
    @property
    def default_model(self) -> str:
        """默认模型名称"""
        ...
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        ...
    
    def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str:
        """生成 JSON 格式的文本
        
        Args:
            prompt: 输入提示词
            schema: JSON Schema（可选）
            **kwargs: 其他参数
            
        Returns:
            JSON 格式的字符串
        """
        ...
    
    def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        """生成文本并返回完整响应
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            完整的 LLM 响应对象
        """
        ...
    
    def generate_stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """流式生成文本（可选实现）
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Yields:
            生成的文本片段
        """
        ...


@runtime_checkable
class AsyncLLMProvider(Protocol):
    """LLM 提供者 Protocol（异步版本）
    
    定义了异步 LLM 提供者需要实现的接口
    """
    
    @property
    def provider_name(self) -> str:
        """提供者名称"""
        ...
    
    @property
    def default_model(self) -> str:
        """默认模型名称"""
        ...
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """异步生成文本
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        ...
    
    async def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str:
        """异步生成 JSON 格式的文本
        
        Args:
            prompt: 输入提示词
            schema: JSON Schema（可选）
            **kwargs: 其他参数
            
        Returns:
            JSON 格式的字符串
        """
        ...
    
    async def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        """异步生成文本并返回完整响应
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            完整的 LLM 响应对象
        """
        ...
    
    async def generate_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """异步流式生成文本（可选实现）
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Yields:
            生成的文本片段
        """
        ...


@runtime_checkable
class StreamableLLMProvider(LLMProvider, Protocol):
    """可流式的 LLM 提供者 Protocol
    
    扩展了 LLMProvider，要求实现流式生成
    """
    
    def generate_stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """流式生成文本
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Yields:
            生成的文本片段
        """
        ...
