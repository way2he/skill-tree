# LLM 统一接口层

为多个 LLM 提供者提供统一的接口，支持同步和异步调用。

## 功能特性

- ✅ **统一接口** - 所有 LLM 提供者使用相同的 API
- ✅ **策略模式** - 不同厂商可互换
- ✅ **工厂模式** - 配置驱动创建，开闭原则
- ✅ **适配器模式** - 统一不同厂商的接口差异
- ✅ **弹性机制** - 重试、熔断、限流、降级
- ✅ **观察者模式** - 事件总线和处理器
- ✅ **同步 + 异步** - 双版本支持

## 目录结构

```
llm/core/
├── __init__.py              # 包入口，导出公共 API
├── exceptions.py            # 统一异常体系
├── types.py                 # Protocol、数据模型、枚举
├── config.py                # YAML/JSON 配置加载
├── factory.py               # 注册表 + 工厂函数
├── llm_config.yaml          # 示例配置
├── adapter/                 # 适配器层
│   ├── __init__.py
│   ├── base.py              # 同步 + 异步基类
│   ├── requests_adapter.py  # requests 适配
│   ├── aiohttp_adapter.py   # aiohttp 适配
│   ├── openai_adapter.py    # OpenAI 适配
│   ├── anthropic_adapter.py # Anthropic 适配
│   ├── ollama_adapter.py    # Ollama 适配
│   └── sdk_adapter.py       # 其他 SDK 适配
├── resilience/              # 弹性机制
│   ├── __init__.py
│   ├── retry.py             # 指数退避 + Jitter
│   ├── circuit_breaker.py   # 熔断器
│   ├── rate_limiter.py      # 令牌桶限流器
│   ├── fallback.py          # 降级策略
│   └── decorator.py         # 组合装饰器
└── observer/                # 观察者
    ├── __init__.py
    ├── events.py            # 事件类型
    ├── event_bus.py         # 事件总线
    └── handlers.py          # 处理器
```

## 快速开始

### 同步版本

```python
from llm.core import create_llm, create_llm_from_config, LLMResponse

# 直接创建
llm = create_llm("deepseek", api_key="your-api-key")
result = llm.generate("你好")
response = llm.generate_with_response("你好")

# 配置驱动
llm = create_llm_from_config("llm_config.yaml")
```

### 异步版本

```python
from llm.core import create_async_llm, create_llm_async_from_config

llm = await create_async_llm("deepseek", api_key="your-api-key")
result = await llm.generate("你好")
```

### 弹性装饰器

```python
from llm.core import resilient, ResilienceConfig

config = ResilienceConfig(
    retry_max_retries=3,
    circuit_breaker_enabled=True,
    rate_limiter_enabled=True
)

@resilient(config)
def my_llm_call(prompt):
    return llm.generate(prompt)
```

## 配置文件

参见 `llm_config.yaml` 示例配置。

## 集成说明

要将此统一接口层与现有的 llm/ 目录集成，需要在 `factory.py` 中：

1. 导入现有的 llm 客户端
2. 使用 `register_provider()` 注册每个提供者
3. 选择合适的适配器类

## 设计模式

| 模式 | 应用位置 |
|------|----------|
| 策略模式 | 适配器 + 弹性策略 |
| 工厂模式 | LLMRegistry |
| 适配器模式 | adapter/ |
| 装饰器模式 | @resilient() |
| 观察者模式 | EventBus |
| 状态机模式 | CircuitBreaker |
| 模板方法 | BaseLLMAdapter.generate_with_response() |
