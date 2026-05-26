# 模型版本注册表

## 概述

根据 MEMORY.md 规则实现的模型版本管理系统，确保使用最新的大模型版本。

## MEMORY.md 规则

```
第三方厂商大模型版本必须保持最新（2026-05-22 基准）
  - OpenAI: GPT-5.5（旗舰）/ GPT-5.4（性价比）- 严禁 GPT-4/GPT-4o/GPT-3.5
  - Anthropic: Claude Opus 4.7 / Claude Sonnet 4.6
  - Google: Gemini 3.1 Pro / Gemini 3 Pro
  - DeepSeek: DeepSeek V4 Pro / DeepSeek V4 Flash
  - Kimi: Kimi K2.6
  - GLM: GLM-5.1
  - Qwen: Qwen3-Max / Qwen3-Max-Thinking
  - MiniMax: MiniMax M2.5
  - 小米: MiMo V2.5 Pro
  - 文心: 文心一言 5.0
```

## 文件结构

```
llm/
├── core/
│   ├── model_registry.py   # 模型注册表（新增）
│   └── __init__.py         # 已更新，导出模型注册表
├── test_model_registry.py  # 测试脚本（新增）
└── MODEL_REGISTRY_README.md # 本文档
```

## 快速使用

### 1. 验证模型

```python
from llm.core import validate_model

# 验证模型是否是最新
is_latest, recommended = validate_model("openai", "gpt-4")
# 返回: (False, "gpt-5.4") 并发出 DeprecationWarning

# 不发出警告
is_latest, recommended = validate_model("openai", "gpt-4", warn=False)
```

### 2. 获取最新模型

```python
from llm.core import get_latest_model, get_model_registry

# 获取最新模型名
latest = get_latest_model("openai")
# 返回: "gpt-5.5"

# 获取注册表实例
registry = get_model_registry()

# 获取详细信息
info = registry.get_model_info("openai", "gpt-5.5")
print(info.price_per_1k_input)  # 0.015
```

### 3. 运行时效巡检

```python
from llm.core import get_model_registry

registry = get_model_registry()
audit = registry.run_audit()
# 返回: {"openai": ["gpt-4.1", "gpt-4", "gpt-4o", "gpt-3.5-turbo"]}
```

## API 参考

### ModelRegistry 类

| 方法 | 说明 |
|------|------|
| `get_latest(provider)` | 获取最新模型名 |
| `get_latest_models(provider)` | 获取所有最新模型列表 |
| `get_model_info(provider, model)` | 获取模型详细信息 |
| `validate_model(provider, model, warn=True)` | 验证模型是否最新 |
| `list_providers()` | 列出所有厂商 |
| `list_all_models(provider)` | 列出厂商所有模型 |
| `add_model(provider, model_info)` | 添加/更新模型 |
| `mark_deprecated(provider, model, deprecated_by)` | 标记模型为已废弃 |
| `run_audit()` | 运行时效巡检 |

### 全局便捷函数

| 函数 | 说明 |
|------|------|
| `get_model_registry()` | 获取全局注册表实例 |
| `validate_model(provider, model, warn=True)` | 验证模型 |
| `get_latest_model(provider)` | 获取最新模型 |

### 数据类：ModelInfo

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | str | 模型名 |
| `provider` | str | 厂商 |
| `is_latest` | bool | 是否最新 |
| `is_deprecated` | bool | 是否废弃 |
| `deprecated_by` | str \| None | 替代模型 |
| `price_per_1k_input` | float \| None | 输入价格（USD） |
| `price_per_1k_output` | float \| None | 输出价格（USD） |
| `last_updated` | datetime | 最后更新时间 |

## 运行测试

```bash
# 运行完整测试
python test_model_registry.py

# 运行模型注册表演示
python -c "from llm.core.model_registry import get_model_registry; r = get_model_registry(); print(r)"
```

## 注意事项

### 1. 每 3 个月需要做一次「模型时效巡检」

```python
from llm.core import get_model_registry

audit = get_model_registry().run_audit()
if audit:
    print("需要更新的模型:", audit)
```

### 2. 如何更新模型版本

编辑 `core/model_registry.py` 中的 `_init_models()` 方法。

### 3. 添加新厂商

在 `_init_models()` 中添加：

```python
self._models["new_provider"] = {
    "model-v1": ModelInfo("model-v1", "new_provider", is_latest=True),
}
```

## 导出的内容

在 `llm.core` 中已导出：

```python
# 类
ModelRegistry
ModelInfo

# 函数
get_model_registry()
validate_model(provider, model, warn=True)
get_latest_model(provider)
```

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.2.0 | 2026-05-25 | 新增模型注册表功能 |
