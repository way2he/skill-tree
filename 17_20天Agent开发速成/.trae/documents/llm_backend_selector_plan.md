# LLM 底层实现选择器设计方案

## 一、需求概述

用户希望能够方便地选择 LLM 客户端的底层实现方式：
- **requests** - 使用 requests 库同步 HTTP 调用
- **aiohttp** - 使用 aiohttp 库异步 HTTP 调用
- **openai_sdk** - 使用 OpenAI 官方 SDK
- **native_sdk** - 使用厂商自己的 SDK（如 anthropic、google 等）

**新增需求**：支持「一键配置」——全局设置默认底层实现后，所有客户端创建自动使用该实现，无需每次指定。

## 二、当前代码结构分析

```
llm/
├── requests/          # 同步请求实现（使用 requests 库）
│   └── providers/     # 各厂商客户端（25+）
├── aiohttp/           # 异步请求实现（使用 aiohttp 库）
│   └── providers/     # 各厂商异步客户端
├── openai/            # OpenAI SDK 实现
├── anthropic/         # Anthropic SDK 实现
├── core/
│   ├── adapter/       # 适配器基类和实现（已有6种适配器）
│   ├── factory.py     # 工厂和注册表
│   ├── config.py      # YAML/JSON 配置加载（已有）
│   ├── default.py     # 默认实例工厂（已有 provider 解析优先级）
│   ├── types.py       # 类型定义
│   ├── exceptions.py  # 异常类
│   └── llm_config.yaml # 配置文件（已有）
└── demo/              # 示例代码
```

**已有优势**：
- 适配器模式已实现（6种适配器）
- 工厂+注册表已存在
- YAML配置系统已存在（`config.py` + `llm_config.yaml`）
- 默认实例工厂已存在（`default.py`，支持 provider 解析优先级）
- 同步/异步接口已分离

**需要改进**：
- 缺少统一的「底层实现」选择接口
- `default.py` 只解析 provider，不解析 backend
- YAML配置中 `provider_type` 字段含义模糊（实际是厂商类型，不是实现层）
- 缺少运行时切换实现的能力

## 三、设计方案

### 3.1 一键配置：三种方式设置默认实现

配置优先级（从高到低）：

```
代码显式指定 > 环境变量 > YAML配置文件 > 代码全局设置 > 兜底默认值
```

#### 方式一：环境变量（最简单）

```bash
# .env 或系统环境变量
LLM_BACKEND=openai_sdk
```

一行搞定，所有 `get_llm()` 自动使用 OpenAI SDK。

#### 方式二：YAML 配置文件

```yaml
# llm/core/llm_config.yaml
default_provider: deepseek
default_backend: openai_sdk    # 新增字段

providers:
  deepseek:
    provider_type: requests
    backend: openai_sdk        # 可选：按厂商覆盖
    model: deepseek-chat
    api_key: ${DEEPSEEK_API_KEY}
    base_url: https://api.deepseek.com/v1
```

#### 方式三：代码全局设置

```python
from llm.core import set_default_backend, BackendType

# 一行代码，全局生效
set_default_backend("openai_sdk")
# 或
set_default_backend(BackendType.OPENAI_SDK)

# 之后所有 get_llm() 自动使用 openai_sdk
from llm.core import get_llm
client = get_llm("deepseek")  # 自动用 openai_sdk 实现
```

### 3.2 核心接口设计

#### BackendType 枚举

```python
class BackendType(str, Enum):
    """底层实现类型枚举"""
    REQUESTS = "requests"      # requests 库同步 HTTP
    AIOHTTP = "aiohttp"        # aiohttp 库异步 HTTP
    OPENAI_SDK = "openai_sdk"  # OpenAI 官方 SDK
    NATIVE_SDK = "native_sdk"  # 厂商原生 SDK
```

#### 一键配置 API

```python
# 设置全局默认实现
set_default_backend("openai_sdk")

# 查询当前默认实现
get_default_backend()  # -> BackendType.OPENAI_SDK

# 重置为默认值
reset_default_backend()
```

#### LLMClientBuilder 构建器（保留原有设计）

```python
# 显式指定实现（优先级最高，覆盖全局设置）
client = (LLMClientBuilder()
    .provider("deepseek")
    .openai_sdk()  # 显式指定
    .api_key("sk-xxx")
    .build())

# 不指定实现（自动使用全局默认）
client = (LLMClientBuilder()
    .provider("deepseek")
    .api_key("sk-xxx")
    .build())  # 自动用全局默认的 backend
```

#### BackendSwitcher 切换器（保留原有设计）

```python
switcher = (BackendSwitcher("deepseek")
    .add_backend("requests", api_key="sk-xxx")
    .add_backend("openai_sdk", api_key="sk-xxx", base_url="..."))

switcher.switch_to("openai_sdk")
client = switcher.get_client()
```

### 3.3 完整的解析优先级

```
┌─────────────────────────────────────────────────────────────┐
│                    Backend 解析优先级                         │
├─────────────────────────────────────────────────────────────┤
│ 1. Builder/便捷函数 显式指定 backend= 参数                   │
│ 2. YAML 配置中该厂商的 backend 字段（厂商级覆盖）              │
│ 3. 代码 set_default_backend() 设置的全局默认                  │
│ 4. 环境变量 LLM_BACKEND                                     │
│ 5. YAML 配置中的 default_backend 字段（全局默认）              │
│ 6. 兜底值: requests（同步）/ aiohttp（异步）                  │
└─────────────────────────────────────────────────────────────┘
```

## 四、需要修改/新增的文件

### 4.1 新增文件

| 文件路径 | 说明 |
|---------|------|
| `llm/core/backend.py` | 核心实现：BackendType 枚举、BackendConfig、LLMClientBuilder、BackendSwitcher、全局默认管理、便捷函数 |
| `llm/demo/demo_backend_selector.py` | 使用示例：一键配置、Builder 模式、运行时切换 |
| `llm/demo/demo_backend_async.py` | 异步使用示例 |

### 4.2 需要修改的文件

| 文件路径 | 修改内容 |
|---------|---------|
| `llm/core/factory.py` | 扩展 `LLMRegistry`，添加 `register_with_backend()`、`list_backends()`；修改 `_register_builtin_providers()` 支持多实现层 |
| `llm/core/default.py` | 扩展 `resolve_provider()` 为 `resolve_provider_and_backend()`，增加 backend 解析逻辑；`get_llm()` / `get_async_llm()` 传入 backend 参数 |
| `llm/core/config.py` | `ProviderConfig` 新增 `backend` 字段；`LLMCoreConfig` 新增 `default_backend` 字段；`_parse_config()` 解析新字段 |
| `llm/core/llm_config.yaml` | 新增 `default_backend` 字段示例 |
| `llm/core/__init__.py` | 导出新增的类和函数 |
| `llm/core/types.py` | 新增 `BackendType` 相关类型别名（可选） |

## 五、实现步骤

### 步骤 1：创建核心模块 `llm/core/backend.py`

包含以下组件：
1. `BackendType` 枚举 - 定义四种实现类型，支持字符串别名解析
2. `BackendConfig` 配置类 - 封装客户端配置
3. `_BackendGlobal` 内部类 - 管理全局默认 backend（线程安全）
4. `set_default_backend()` / `get_default_backend()` / `reset_default_backend()` - 一键配置 API
5. `resolve_backend()` - 按优先级解析最终使用的 backend
6. `LLMClientBuilder` 构建器 - Builder 模式创建客户端
7. `BackendSwitcher` 切换器 - 运行时切换实现
8. `create_client()` / `create_async_client()` - 便捷函数

### 步骤 2：扩展工厂模块 `llm/core/factory.py`

修改 `LLMRegistry` 类：
1. 添加 `register_with_backend()` 方法
2. 添加 `list_backends(provider)` 方法
3. 添加 `get_supported_backends()` 方法
4. 修改 `_register_builtin_providers()` 支持多实现层注册

### 步骤 3：扩展默认实例工厂 `llm/core/default.py`

1. 新增 `resolve_backend(backend=None, provider=None)` 函数
2. 修改 `_build_sync()` / `_build_async()` 接受 backend 参数
3. 修改 `get_llm()` / `get_async_llm()` 支持 backend 参数

### 步骤 4：扩展配置模块 `llm/core/config.py`

1. `ProviderConfig` 新增 `backend: Optional[str]` 字段
2. `LLMCoreConfig` 新增 `default_backend: Optional[str]` 字段
3. `_parse_config()` 解析新字段

### 步骤 5：更新 YAML 配置 `llm/core/llm_config.yaml`

新增 `default_backend` 字段。

### 步骤 6：更新导出 `llm/core/__init__.py`

导出新增的类和函数。

### 步骤 7：创建示例代码

1. `llm/demo/demo_backend_selector.py` - 一键配置 + Builder + 切换器
2. `llm/demo/demo_backend_async.py` - 异步使用示例

## 六、使用示例

### 6.1 一键配置（最常用）

```python
from llm.core import set_default_backend, get_llm

# ===== 方式一：代码设置 =====
set_default_backend("openai_sdk")

# 之后所有调用自动使用 openai_sdk
client = get_llm("deepseek")
result = client.generate("你好")

# ===== 方式二：环境变量 =====
# export LLM_BACKEND=openai_sdk
# 无需改代码，重启即生效

# ===== 方式三：YAML 配置 =====
# default_backend: openai_sdk
# 无需改代码，重启即生效
```

### 6.2 Builder 模式（精细控制）

```python
from llm.core import LLMClientBuilder, BackendType

# 显式指定实现（覆盖全局默认）
client = (LLMClientBuilder()
    .provider("deepseek")
    .openai_sdk()
    .api_key("sk-xxx")
    .model("deepseek-chat")
    .build())

# 不指定实现（使用全局默认）
client = (LLMClientBuilder()
    .provider("deepseek")
    .api_key("sk-xxx")
    .build())  # 自动用全局默认 backend
```

### 6.3 便捷函数

```python
from llm.core import create_client, create_async_client

# 显式指定 backend
client = create_client("deepseek", "openai_sdk", api_key="sk-xxx")

# 不指定 backend（使用全局默认）
client = create_client("deepseek", api_key="sk-xxx")

# 异步
async_client = create_async_client("deepseek", api_key="sk-xxx")
```

### 6.4 运行时切换

```python
from llm.core import BackendSwitcher

switcher = (BackendSwitcher("deepseek")
    .add_backend("requests", api_key="sk-xxx")
    .add_backend("openai_sdk", api_key="sk-xxx", base_url="..."))

switcher.switch_to("openai_sdk")
client = switcher.get_client()

# 故障转移
client = switcher.get_client_with_fallback(["openai_sdk", "requests"])
```

### 6.5 YAML 配置示例

```yaml
# llm/core/llm_config.yaml
default_provider: deepseek
default_backend: openai_sdk    # 全局默认实现层

providers:
  deepseek:
    provider_type: requests
    backend: openai_sdk        # 该厂商使用 openai_sdk
    model: deepseek-chat
    api_key: ${DEEPSEEK_API_KEY}
    base_url: https://api.deepseek.com/v1

  claude:
    provider_type: anthropic
    backend: native_sdk        # 该厂商使用原生 SDK
    model: claude-sonnet-4-20250514
    api_key: ${ANTHROPIC_API_KEY}

  local:
    provider_type: ollama
    # 不指定 backend，使用全局 default_backend
    model: qwen3.5:9b
```

## 七、设计优势

1. **一键配置**：环境变量 / YAML / 代码一行设置，全局生效
2. **优先级清晰**：显式指定 > 厂商配置 > 全局默认 > 环境变量 > YAML > 兜底
3. **向后兼容**：不指定 backend 时行为与现在完全一致（兜底 requests）
4. **厂商级覆盖**：YAML 中每个厂商可以单独指定 backend
5. **运行时切换**：BackendSwitcher 支持 A/B 测试和故障转移
6. **类型安全**：枚举 + 类型提示，IDE 自动补全

## 八、验证步骤

1. 运行示例代码验证基本功能
2. 测试 `set_default_backend()` 全局设置生效
3. 测试环境变量 `LLM_BACKEND` 生效
4. 测试 YAML 配置 `default_backend` 生效
5. 测试厂商级 `backend` 覆盖全局默认
6. 测试显式指定 backend 覆盖所有配置
7. 测试四种实现类型都能正常创建客户端
8. 测试运行时切换和故障转移
9. 验证向后兼容性（不指定任何 backend 时行为不变）
