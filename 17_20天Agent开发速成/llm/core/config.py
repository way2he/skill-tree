"""
LLM 统一接口层 - 配置管理
支持 YAML/JSON 格式，支持环境变量替换
"""

import os
import json
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from .exceptions import LLMConfigError
from .types import ProviderType
from .factory import create_llm, create_async_llm, list_providers


@dataclass
class ResilienceConfigModel:
    """弹性机制配置模型"""
    # 重试配置
    retry_max_retries: int = 3
    retry_base_delay: float = 1.0
    retry_max_delay: float = 60.0
    retry_exponential_base: float = 2.0
    retry_jitter: bool = True
    
    # 熔断器配置
    circuit_breaker_enabled: bool = True
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_timeout: float = 30.0
    circuit_breaker_half_open_max_calls: int = 3
    circuit_breaker_success_threshold: int = 2
    
    # 限流器配置
    rate_limiter_enabled: bool = True
    rate_limiter_requests_per_minute: int = 60
    rate_limiter_requests_per_second: Optional[int] = None
    rate_limiter_burst_size: int = 10
    
    # 降级配置
    fallback_providers: List[str] = field(default_factory=list)


@dataclass
class ProviderConfig:
    """提供者配置模型"""
    name: str
    provider_type: ProviderType
    model: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    ak: Optional[str] = None
    sk: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[float] = None
    backend: Optional[str] = None  # 新增：底层实现类型
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMCoreConfig:
    """LLM 核心配置模型"""
    default_provider: Optional[str] = None
    default_backend: Optional[str] = None  # 新增：全局默认底层实现
    providers: Dict[str, ProviderConfig] = field(default_factory=dict)
    resilience: ResilienceConfigModel = field(default_factory=ResilienceConfigModel)


def _replace_env_vars(value: Any) -> Any:
    """递归替换字符串中的环境变量
    
    支持 ${ENV_VAR} 和 ${ENV_VAR:default} 格式
    
    Args:
        value: 输入值
        
    Returns:
        替换后的值
    """
    if isinstance(value, str):
        import re
        pattern = r'\$\{([^:\}]+)(?::([^\}]*))?\}'
        
        def replace_match(match):
            var_name = match.group(1)
            default_value = match.group(2)
            return os.environ.get(var_name, default_value or match.group(0))
        
        return re.sub(pattern, replace_match, value)
    elif isinstance(value, dict):
        return {k: _replace_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_replace_env_vars(v) for v in value]
    else:
        return value


def _load_yaml_config(file_path: Path) -> Dict[str, Any]:
    """从 YAML 文件加载配置
    
    Args:
        file_path: 文件路径
        
    Returns:
        配置字典
    """
    if not HAS_YAML:
        raise LLMConfigError(
            "PyYAML 未安装，请安装: pip install pyyaml"
        )
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def _load_json_config(file_path: Path) -> Dict[str, Any]:
    """从 JSON 文件加载配置
    
    Args:
        file_path: 文件路径
        
    Returns:
        配置字典
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_config(config_path: str) -> LLMCoreConfig:
    """加载配置文件
    
    支持 YAML 和 JSON 格式
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置对象
    """
    file_path = Path(config_path)
    if not file_path.exists():
        raise LLMConfigError(f"配置文件不存在: {config_path}")
    
    # 根据扩展名选择加载方式
    suffix = file_path.suffix.lower()
    if suffix in ('.yaml', '.yml'):
        config_dict = _load_yaml_config(file_path)
    elif suffix == '.json':
        config_dict = _load_json_config(file_path)
    else:
        raise LLMConfigError(f"不支持的配置文件格式: {suffix}")
    
    # 替换环境变量
    config_dict = _replace_env_vars(config_dict)
    
    # 解析配置
    return _parse_config(config_dict)


def _parse_config(config_dict: Dict[str, Any]) -> LLMCoreConfig:
    """解析配置字典
    
    Args:
        config_dict: 配置字典
        
    Returns:
        配置对象
    """
    # 解析提供者配置
    providers = {}
    for name, provider_data in config_dict.get('providers', {}).items():
        provider_type_str = provider_data.get('provider_type', 'requests')
        try:
            provider_type = ProviderType(provider_type_str)
        except ValueError:
            raise LLMConfigError(f"无效的提供者类型: {provider_type_str}")
        
        providers[name] = ProviderConfig(
            name=name,
            provider_type=provider_type,
            model=provider_data.get('model'),
            api_key=provider_data.get('api_key'),
            base_url=provider_data.get('base_url'),
            ak=provider_data.get('ak'),
            sk=provider_data.get('sk'),
            system_prompt=provider_data.get('system_prompt'),
            temperature=provider_data.get('temperature'),
            max_tokens=provider_data.get('max_tokens'),
            timeout=provider_data.get('timeout'),
            backend=provider_data.get('backend'),  # 新增：解析 backend 字段
            extra=provider_data.get('extra', {})
        )
    
    # 解析弹性机制配置
    resilience_data = config_dict.get('resilience', {})
    resilience = ResilienceConfigModel(
        retry_max_retries=resilience_data.get('retry_max_retries', 3),
        retry_base_delay=resilience_data.get('retry_base_delay', 1.0),
        retry_max_delay=resilience_data.get('retry_max_delay', 60.0),
        retry_exponential_base=resilience_data.get('retry_exponential_base', 2.0),
        retry_jitter=resilience_data.get('retry_jitter', True),
        circuit_breaker_enabled=resilience_data.get('circuit_breaker_enabled', True),
        circuit_breaker_failure_threshold=resilience_data.get('circuit_breaker_failure_threshold', 5),
        circuit_breaker_recovery_timeout=resilience_data.get('circuit_breaker_recovery_timeout', 30.0),
        circuit_breaker_half_open_max_calls=resilience_data.get('circuit_breaker_half_open_max_calls', 3),
        circuit_breaker_success_threshold=resilience_data.get('circuit_breaker_success_threshold', 2),
        rate_limiter_enabled=resilience_data.get('rate_limiter_enabled', True),
        rate_limiter_requests_per_minute=resilience_data.get('rate_limiter_requests_per_minute', resilience_data.get('rate_limiter_rpm', 60)),
        rate_limiter_requests_per_second=resilience_data.get('rate_limiter_requests_per_second'),
        rate_limiter_burst_size=resilience_data.get('rate_limiter_burst_size', 10),
        fallback_providers=resilience_data.get('fallback_providers', [])
    )
    
    return LLMCoreConfig(
        default_provider=config_dict.get('default_provider'),
        default_backend=config_dict.get('default_backend'),  # 新增：解析全局默认 backend
        providers=providers,
        resilience=resilience
    )


def create_llm_from_config(
    config_path: str,
    provider_name: Optional[str] = None
):
    """从配置文件一站式创建 LLM 实例
    
    Args:
        config_path: 配置文件路径
        provider_name: 提供者名称（可选，使用默认提供者）
        
    Returns:
        LLM 实例
    """
    config = load_config(config_path)
    
    # 确定使用哪个提供者
    name = provider_name or config.default_provider
    if not name:
        raise LLMConfigError("未指定提供者，且配置中没有 default_provider")
    
    # 获取提供者配置
    provider_config = config.providers.get(name)
    if not provider_config:
        raise LLMConfigError(f"配置中未找到提供者: {name}")
    
    # 构建参数字典
    kwargs = {}
    if provider_config.api_key:
        kwargs['api_key'] = provider_config.api_key
    if provider_config.base_url:
        kwargs['base_url'] = provider_config.base_url
    if provider_config.ak:
        kwargs['ak'] = provider_config.ak
    if provider_config.sk:
        kwargs['sk'] = provider_config.sk
    if provider_config.model:
        kwargs['model'] = provider_config.model
    if provider_config.temperature is not None:
        kwargs['temperature'] = provider_config.temperature
    if provider_config.max_tokens is not None:
        kwargs['max_tokens'] = provider_config.max_tokens
    if provider_config.timeout is not None:
        kwargs['timeout'] = provider_config.timeout
    
    # 添加额外参数
    kwargs.update(provider_config.extra)
    
    # 创建 LLM 实例
    return create_llm(name, **kwargs)


def create_llm_async_from_config(
    config_path: str,
    provider_name: Optional[str] = None
):
    """从配置文件一站式创建异步 LLM 实例
    
    Args:
        config_path: 配置文件路径
        provider_name: 提供者名称（可选，使用默认提供者）
        
    Returns:
        异步 LLM 实例
    """
    config = load_config(config_path)
    
    # 确定使用哪个提供者
    name = provider_name or config.default_provider
    if not name:
        raise LLMConfigError("未指定提供者，且配置中没有 default_provider")
    
    # 获取提供者配置
    provider_config = config.providers.get(name)
    if not provider_config:
        raise LLMConfigError(f"配置中未找到提供者: {name}")
    
    # 构建参数字典
    kwargs = {}
    if provider_config.api_key:
        kwargs['api_key'] = provider_config.api_key
    if provider_config.base_url:
        kwargs['base_url'] = provider_config.base_url
    if provider_config.ak:
        kwargs['ak'] = provider_config.ak
    if provider_config.sk:
        kwargs['sk'] = provider_config.sk
    if provider_config.model:
        kwargs['model'] = provider_config.model
    if provider_config.temperature is not None:
        kwargs['temperature'] = provider_config.temperature
    if provider_config.max_tokens is not None:
        kwargs['max_tokens'] = provider_config.max_tokens
    if provider_config.timeout is not None:
        kwargs['timeout'] = provider_config.timeout
    
    # 添加额外参数
    kwargs.update(provider_config.extra)
    
    # 创建异步 LLM 实例
    return create_async_llm(name, **kwargs)
