"""
LLM 统一接口层 - 异常体系
定义了所有 LLM 相关的异常类，提供统一的错误处理机制
"""

from typing import Optional


class LLMError(Exception):
    """LLM 异常基类
    
    所有 LLM 相关异常的基类，包含提供者信息和原始异常
    """
    
    def __init__(
        self,
        message: str,
        provider: Optional[str] = None,
        cause: Optional[Exception] = None
    ):
        """初始化 LLM 异常
        
        Args:
            message: 异常消息
            provider: 提供者名称（可选）
            cause: 原始异常（可选）
        """
        self.provider = provider
        self.cause = cause
        full_message = message
        if provider:
            full_message = f"[{provider}] {full_message}"
        super().__init__(full_message)


class LLMConnectionError(LLMError):
    """连接错误
    
    当无法连接到 LLM 服务时抛出
    """
    pass


class LLMAuthError(LLMError):
    """认证错误（不可重试）
    
    当 API Key 无效或认证失败时抛出
    """
    pass


class LLMRateLimitError(LLMError):
    """限流错误 429（可重试）
    
    当请求被限流时抛出，包含重试等待时间
    """
    
    def __init__(
        self,
        message: str,
        provider: Optional[str] = None,
        cause: Optional[Exception] = None,
        retry_after: Optional[float] = None
    ):
        """初始化限流错误
        
        Args:
            message: 异常消息
            provider: 提供者名称（可选）
            cause: 原始异常（可选）
            retry_after: 建议的重试等待时间（秒，可选）
        """
        self.retry_after = retry_after
        super().__init__(message, provider, cause)


class LLMServerError(LLMError):
    """服务端错误 5xx（可重试）
    
    当服务端返回 5xx 错误时抛出
    """
    pass


class LLMTimeoutError(LLMError):
    """超时错误（可重试）
    
    当请求超时时抛出
    """
    pass


class LLMResponseError(LLMError):
    """响应解析错误
    
    当无法解析 LLM 响应时抛出
    """
    pass


class LLMCircuitOpenError(LLMError):
    """熔断器打开错误
    
    当熔断器处于打开状态，拒绝请求时抛出
    """
    
    def __init__(
        self,
        message: str,
        provider: Optional[str] = None,
        cause: Optional[Exception] = None,
        recovery_time: Optional[float] = None
    ):
        """初始化熔断器错误
        
        Args:
            message: 异常消息
            provider: 提供者名称（可选）
            cause: 原始异常（可选）
            recovery_time: 预计恢复时间（秒，可选）
        """
        self.recovery_time = recovery_time
        super().__init__(message, provider, cause)


class LLMProviderNotFoundError(LLMError):
    """提供者未注册错误
    
    当请求的提供者未在注册表中注册时抛出
    """
    pass


class LLMConfigError(LLMError):
    """配置错误
    
    当配置无效或缺失时抛出
    """
    pass
