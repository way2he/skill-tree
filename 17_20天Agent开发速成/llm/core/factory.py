"""
LLM 统一接口层 - 工厂与注册表
提供提供者注册和创建功能
"""

from typing import Dict, Any, Optional, Callable, Type

from .exceptions import LLMProviderNotFoundError
from .types import ProviderType
from .adapter import (
    BaseLLMAdapter,
    BaseAsyncLLMAdapter,
    RequestsLLMAdapter,
    AioHttpLLMAdapter,
    OpenAILLMAdapter,
    AnthropicLLMAdapter,
    OllamaLLMAdapter,
    SDKLLMAdapter
)


class LLMRegistry:
    """LLM 注册表
    
    管理提供者的注册和创建
    """
    
    def __init__(self):
        """初始化注册表"""
        # 同步注册表
        self._sync_registry: Dict[
            str, 
            Dict[str, Any]
        ] = {}
        
        # 异步注册表
        self._async_registry: Dict[
            str, 
            Dict[str, Any]
        ] = {}
    
    def register(
        self,
        name: str,
        client_factory: Callable[..., Any],
        adapter_class: Type[BaseLLMAdapter],
        provider_type: Optional[ProviderType] = None
    ):
        """注册同步提供者
        
        Args:
            name: 提供者名称
            client_factory: 客户端工厂函数
            adapter_class: 适配器类
            provider_type: 提供者类型（可选）
        """
        self._sync_registry[name] = {
            'client_factory': client_factory,
            'adapter_class': adapter_class,
            'provider_type': provider_type
        }
    
    def register_async(
        self,
        name: str,
        client_factory: Callable[..., Any],
        adapter_class: Type[BaseAsyncLLMAdapter],
        provider_type: Optional[ProviderType] = None
    ):
        """注册异步提供者
        
        Args:
            name: 提供者名称
            client_factory: 客户端工厂函数
            adapter_class: 适配器类
            provider_type: 提供者类型（可选）
        """
        self._async_registry[name] = {
            'client_factory': client_factory,
            'adapter_class': adapter_class,
            'provider_type': provider_type
        }
    
    def provider(self, name: str):
        """装饰器：注册同步提供者
        
        Args:
            name: 提供者名称
            
        Returns:
            装饰器
        """
        def decorator(factory):
            # 默认使用 RequestsLLMAdapter
            self.register(
                name, 
                factory, 
                RequestsLLMAdapter,
                ProviderType.REQUESTS
            )
            return factory
        return decorator
    
    def create(self, name: str, **kwargs) -> BaseLLMAdapter:
        """创建同步适配器
        
        Args:
            name: 提供者名称
            **kwargs: 客户端构造参数
            
        Returns:
            适配器实例
        """
        if name not in self._sync_registry:
            raise LLMProviderNotFoundError(
                f"提供者未注册: {name}，支持的选项: {list(self._sync_registry.keys())}",
                provider=name
            )
        
        entry = self._sync_registry[name]
        client_factory = entry['client_factory']
        adapter_class = entry['adapter_class']
        
        # 创建客户端
        client = client_factory(**kwargs)
        
        # 创建并返回适配器
        return adapter_class(client, provider_name=name)
    
    def create_async(self, name: str, **kwargs) -> BaseAsyncLLMAdapter:
        """创建异步适配器
        
        Args:
            name: 提供者名称
            **kwargs: 客户端构造参数
            
        Returns:
            异步适配器实例
        """
        if name not in self._async_registry:
            raise LLMProviderNotFoundError(
                f"异步提供者未注册: {name}，支持的选项: {list(self._async_registry.keys())}",
                provider=name
            )
        
        entry = self._async_registry[name]
        client_factory = entry['client_factory']
        adapter_class = entry['adapter_class']
        
        # 创建客户端
        client = client_factory(**kwargs)
        
        # 创建并返回适配器
        return adapter_class(client, provider_name=name)
    
    def _infer_adapter(self, client: Any) -> Type[BaseLLMAdapter]:
        """根据客户端类型自动推断适配器
        
        Args:
            client: 客户端实例
            
        Returns:
            适配器类
        """
        # 这是一个简化的实现
        # 实际项目中可以根据客户端的类型、模块等进行更智能的推断
        client_class_name = client.__class__.__name__.lower()
        
        if 'aiohttp' in client_class_name:
            return AioHttpLLMAdapter
        elif 'openai' in client_class_name:
            return OpenAILLMAdapter
        elif 'anthropic' in client_class_name:
            return AnthropicLLMAdapter
        elif 'ollama' in client_class_name:
            return OllamaLLMAdapter
        elif any(sdk in client_class_name for sdk in [
            'baidu', 'alibaba', 'zhipu', 'google', 
            'cohere', 'mistral', 'groq', 'volcengine'
        ]):
            return SDKLLMAdapter
        else:
            return RequestsLLMAdapter
    
    def list_providers(self) -> list[str]:
        """列出所有已注册的同步提供者
        
        Returns:
            提供者名称列表
        """
        return list(self._sync_registry.keys())
    
    def list_async_providers(self) -> list[str]:
        """列出所有已注册的异步提供者
        
        Returns:
            提供者名称列表
        """
        return list(self._async_registry.keys())


# 全局注册表实例
_registry = LLMRegistry()


# 便捷函数
def register_provider(
    name: str,
    client_factory: Callable[..., Any],
    adapter_class: Type[BaseLLMAdapter] = RequestsLLMAdapter,
    provider_type: Optional[ProviderType] = None
):
    """注册同步提供者（便捷函数）
    
    Args:
        name: 提供者名称
        client_factory: 客户端工厂函数
        adapter_class: 适配器类（默认 RequestsLLMAdapter）
        provider_type: 提供者类型（可选）
    """
    _registry.register(name, client_factory, adapter_class, provider_type)


def register_async_provider(
    name: str,
    client_factory: Callable[..., Any],
    adapter_class: Type[BaseAsyncLLMAdapter] = AioHttpLLMAdapter,
    provider_type: Optional[ProviderType] = None
):
    """注册异步提供者（便捷函数）
    
    Args:
        name: 提供者名称
        client_factory: 客户端工厂函数
        adapter_class: 适配器类（默认 AioHttpLLMAdapter）
        provider_type: 提供者类型（可选）
    """
    _registry.register_async(name, client_factory, adapter_class, provider_type)


def create_llm(name: str, **kwargs) -> BaseLLMAdapter:
    """创建同步 LLM 实例（便捷函数）
    
    Args:
        name: 提供者名称
        **kwargs: 客户端构造参数
        
    Returns:
        适配器实例
    """
    return _registry.create(name, **kwargs)


def create_async_llm(name: str, **kwargs) -> BaseAsyncLLMAdapter:
    """创建异步 LLM 实例（便捷函数）
    
    Args:
        name: 提供者名称
        **kwargs: 客户端构造参数
        
    Returns:
        异步适配器实例
    """
    return _registry.create_async(name, **kwargs)


def list_providers() -> list[str]:
    """列出所有已注册的同步提供者
    
    Returns:
        提供者名称列表
    """
    return _registry.list_providers()


def list_async_providers() -> list[str]:
    """列出所有已注册的异步提供者
    
    Returns:
        提供者名称列表
    """
    return _registry.list_async_providers()


# 内置注册 - 注册所有现有的 llm/requests/ 厂商
def _register_builtin_providers():
    """注册内置提供者"""
    # 导入现有的厂商客户端
    try:
        from llm.requests.providers import (
            OllamaClient,
            OpenAIClient,
            AnthropicClient,
            DoubaoClient,
            QwenClient,
            GLMClient,
            WenxinClient,
            KimiClient,
            DeepSeekClient,
            MiniMaxClient,
            CohereClient,
            HunyuanClient,
            PanguClient,
            MistralClient,
            TogetherClient,
            MiLMClient,
            XAIClient,
            GoogleClient,
            MetaClient,
            ShangtangClient,
            StepfunClient,
            TiangongClient,
            SparkClient,
            BaichuanClient,
            YiClient,
        )
        
        # 注册所有厂商 - 使用 RequestsLLMAdapter
        providers = [
            ("ollama", OllamaClient, OllamaLLMAdapter, ProviderType.OLLAMA),
            ("openai", OpenAIClient, OpenAILLMAdapter, ProviderType.OPENAI),
            ("anthropic", AnthropicClient, AnthropicLLMAdapter, ProviderType.ANTHROPIC),
            ("doubao", DoubaoClient, SDKLLMAdapter, ProviderType.BAIDU),
            ("qwen", QwenClient, SDKLLMAdapter, ProviderType.ALIBABA),
            ("glm", GLMClient, SDKLLMAdapter, ProviderType.ZHIPU),
            ("wenxin", WenxinClient, SDKLLMAdapter, ProviderType.BAIDU),
            ("kimi", KimiClient, SDKLLMAdapter, ProviderType.ZHIPU),
            ("deepseek", DeepSeekClient, RequestsLLMAdapter, ProviderType.REQUESTS),
            ("minimax", MiniMaxClient, SDKLLMAdapter, ProviderType.ZHIPU),
            ("cohere", CohereClient, SDKLLMAdapter, ProviderType.COHERE),
            ("hunyuan", HunyuanClient, SDKLLMAdapter, ProviderType.BAIDU),
            ("pangu", PanguClient, SDKLLMAdapter, ProviderType.BAIDU),
            ("mistral", MistralClient, SDKLLMAdapter, ProviderType.MISTRAL),
            ("together", TogetherClient, RequestsLLMAdapter, ProviderType.REQUESTS),
            ("milm", MiLMClient, SDKLLMAdapter, ProviderType.ZHIPU),
            ("xai", XAIClient, RequestsLLMAdapter, ProviderType.REQUESTS),
            ("google", GoogleClient, SDKLLMAdapter, ProviderType.GOOGLE),
            ("meta", MetaClient, SDKLLMAdapter, ProviderType.GOOGLE),
            ("shangtang", ShangtangClient, SDKLLMAdapter, ProviderType.BAIDU),
            ("stepfun", StepfunClient, SDKLLMAdapter, ProviderType.BAIDU),
            ("tiangong", TiangongClient, SDKLLMAdapter, ProviderType.BAIDU),
            ("spark", SparkClient, SDKLLMAdapter, ProviderType.BAIDU),
            ("baichuan", BaichuanClient, SDKLLMAdapter, ProviderType.ZHIPU),
            ("yi", YiClient, SDKLLMAdapter, ProviderType.ZHIPU),
        ]
        
        for name, client_class, adapter_class, provider_type in providers:
            register_provider(name, client_class, adapter_class, provider_type)
        
        # 尝试注册异步厂商
        try:
            from llm.aiohttp.providers import create_client as create_async_client
            
            # 这里简化处理，实际项目中可以根据需要注册更多异步厂商
            async_providers = [
                "ollama", "openai", "anthropic", "deepseek", "qwen",
            ]
            
            for name in async_providers:
                def factory(n=name):
                    def create(**kwargs):
                        from llm.aiohttp.providers import create_client
                        return create_client(n, **kwargs)
                    return create
                
                register_async_provider(name, factory(), AioHttpLLMAdapter, ProviderType.AIOHTTP)
        except (ImportError, Exception):
            # 异步模块可能不存在，忽略
            pass
        
    except ImportError:
        # 如果 llm.requests 模块不存在，只做简单的占位注册
        pass


_register_builtin_providers()
