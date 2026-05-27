"""
LLM 统一接口层 - 降级策略
主提供者 -> 备用链
"""

from typing import List, Any, Dict, Optional, Callable

from ..exceptions import LLMError

from ..logging_utils import get_logger

# 模块级日志器
_logger = get_logger("fallback")


class FallbackStrategy:
    """降级策略（同步版本）
    
    主提供者失败后，依次尝试备用提供者
    """
    
    def __init__(
        self,
        primary: Any,
        fallbacks: List[Any],
        on_fallback: Optional[Callable[[int, Exception], None]] = None
    ):
        """初始化降级策略
        
        Args:
            primary: 主提供者
            fallbacks: 备用提供者列表
            on_fallback: 降级回调函数
        """
        self._primary = primary
        self._fallbacks = fallbacks
        self._on_fallback = on_fallback
        self._client_cache: Dict[int, Any] = {}
    
    def _get_client(self, index: int) -> Any:
        """获取客户端（懒加载）
        
        Args:
            index: 提供者索引（0 是主提供者）
            
        Returns:
            客户端实例
        """
        if index in self._client_cache:
            return self._client_cache[index]
        
        if index == 0:
            client = self._primary
        else:
            client = self._fallbacks[index - 1]
        
        # 如果是工厂函数，调用它
        if callable(client):
            client = client()
        
        self._client_cache[index] = client
        return client
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本（带降级）
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        last_exception = None
        
        # 尝试主提供者
        try:
            client = self._get_client(0)
            return client.generate(prompt, **kwargs)
        except Exception as e:
            last_exception = e
            _logger.warning(
                "降级触发: 主提供者失败 exception=%s: %s",
                type(e).__name__, e,
            )
            if self._on_fallback:
                self._on_fallback(0, e)
        
        # 尝试备用提供者
        for i in range(len(self._fallbacks)):
            fallback_index = i + 1
            try:
                client = self._get_client(fallback_index)
                result = client.generate(prompt, **kwargs)
                _logger.info(
                    "降级成功: fallback_index=%d provider=%s",
                    fallback_index, getattr(client, 'provider_name', 'unknown'),
                )
                return result
            except Exception as e:
                last_exception = e
                if self._on_fallback:
                    self._on_fallback(fallback_index, e)
        
        # 所有都失败了
        if last_exception:
            raise last_exception
        raise LLMError("所有提供者都失败了")
    
    def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str:
        """生成 JSON 格式的文本（带降级）
        
        Args:
            prompt: 输入提示词
            schema: JSON Schema（可选）
            **kwargs: 其他参数
            
        Returns:
            JSON 格式的字符串
        """
        last_exception = None
        
        # 尝试主提供者
        try:
            client = self._get_client(0)
            return client.generate_json(prompt, schema, **kwargs)
        except Exception as e:
            last_exception = e
            _logger.warning(
                "降级触发: 主提供者失败 exception=%s: %s",
                type(e).__name__, e,
            )
            if self._on_fallback:
                self._on_fallback(0, e)
        
        # 尝试备用提供者
        for i in range(len(self._fallbacks)):
            fallback_index = i + 1
            try:
                client = self._get_client(fallback_index)
                result = client.generate_json(prompt, schema, **kwargs)
                _logger.info(
                    "降级成功: fallback_index=%d provider=%s",
                    fallback_index, getattr(client, 'provider_name', 'unknown'),
                )
                return result
            except Exception as e:
                last_exception = e
                if self._on_fallback:
                    self._on_fallback(fallback_index, e)
        
        # 所有都失败了
        if last_exception:
            raise last_exception
        raise LLMError("所有提供者都失败了")


class AsyncFallbackStrategy:
    """降级策略（异步版本）
    
    主提供者失败后，依次尝试备用提供者
    """
    
    def __init__(
        self,
        primary: Any,
        fallbacks: List[Any],
        on_fallback: Optional[Callable[[int, Exception], Any]] = None
    ):
        """初始化异步降级策略
        
        Args:
            primary: 主提供者
            fallbacks: 备用提供者列表
            on_fallback: 降级回调函数（可以是异步的）
        """
        self._primary = primary
        self._fallbacks = fallbacks
        self._on_fallback = on_fallback
        self._client_cache: Dict[int, Any] = {}
    
    async def _get_client(self, index: int) -> Any:
        """获取客户端（懒加载）
        
        Args:
            index: 提供者索引（0 是主提供者）
            
        Returns:
            客户端实例
        """
        if index in self._client_cache:
            return self._client_cache[index]
        
        if index == 0:
            client = self._primary
        else:
            client = self._fallbacks[index - 1]
        
        # 如果是工厂函数，调用它
        if callable(client):
            client = client()
        
        self._client_cache[index] = client
        return client
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """异步生成文本（带降级）
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        last_exception = None
        
        # 尝试主提供者
        try:
            client = await self._get_client(0)
            return await client.generate(prompt, **kwargs)
        except Exception as e:
            last_exception = e
            _logger.warning(
                "降级触发: 主提供者失败 exception=%s: %s",
                type(e).__name__, e,
            )
            if self._on_fallback:
                result = self._on_fallback(0, e)
                if hasattr(result, '__await__'):
                    await result
        
        # 尝试备用提供者
        for i in range(len(self._fallbacks)):
            fallback_index = i + 1
            try:
                client = await self._get_client(fallback_index)
                result = await client.generate(prompt, **kwargs)
                _logger.info(
                    "降级成功: fallback_index=%d provider=%s",
                    fallback_index, getattr(client, 'provider_name', 'unknown'),
                )
                return result
            except Exception as e:
                last_exception = e
                if self._on_fallback:
                    result = self._on_fallback(fallback_index, e)
                    if hasattr(result, '__await__'):
                        await result
        
        # 所有都失败了
        if last_exception:
            raise last_exception
        raise LLMError("所有提供者都失败了")
    
    async def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str:
        """异步生成 JSON 格式的文本（带降级）
        
        Args:
            prompt: 输入提示词
            schema: JSON Schema（可选）
            **kwargs: 其他参数
            
        Returns:
            JSON 格式的字符串
        """
        last_exception = None
        
        # 尝试主提供者
        try:
            client = await self._get_client(0)
            return await client.generate_json(prompt, schema, **kwargs)
        except Exception as e:
            last_exception = e
            _logger.warning(
                "降级触发: 主提供者失败 exception=%s: %s",
                type(e).__name__, e,
            )
            if self._on_fallback:
                result = self._on_fallback(0, e)
                if hasattr(result, '__await__'):
                    await result
        
        # 尝试备用提供者
        for i in range(len(self._fallbacks)):
            fallback_index = i + 1
            try:
                client = await self._get_client(fallback_index)
                result = await client.generate_json(prompt, schema, **kwargs)
                _logger.info(
                    "降级成功: fallback_index=%d provider=%s",
                    fallback_index, getattr(client, 'provider_name', 'unknown'),
                )
                return result
            except Exception as e:
                last_exception = e
                if self._on_fallback:
                    result = self._on_fallback(fallback_index, e)
                    if hasattr(result, '__await__'):
                        await result
        
        # 所有都失败了
        if last_exception:
            raise last_exception
        raise LLMError("所有提供者都失败了")
