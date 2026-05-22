# OpenAI 通用协议 vs 各厂商官方 SDK 对比

## 概述

在大模型调用中，主要有两种集成方式：
1. **OpenAI 通用协议**（OpenAI-compatible API）- 行业标准接口
2. **各厂商官方 SDK**（Official SDK）- 厂商专属封装

---

## 一、OpenAI 通用协议

### 1.1 什么是 OpenAI 通用协议？

OpenAI 通用协议是指采用与 OpenAI API 相同的接口规范（Chat Completions API），包括：
- 相同的请求格式（JSON 结构）
- 相同的端点命名（`/v1/chat/completions`）
- 相同的参数名称（`messages`, `model`, `temperature`, `max_tokens` 等）
- 相同的响应格式

### 1.2 支持 OpenAI 协议的厂商

几乎所有主流厂商都支持 OpenAI 兼容接口：

| 类型 | 厂商列表 |
|------|----------|
| **国际厂商** | OpenAI、Anthropic、Google、Cohere、Mistral、Groq、Together、xAI 等 |
| **国内大厂** | 阿里云（通义千问）、百度（文心）、字节（豆包）、腾讯（混元）、华为（盘古）等 |
| **国内创业公司** | 智谱（ChatGLM）、月之暗面（Kimi）、MiniMax、零一万物、百川、商汤、阶跃星辰、DeepSeek 等 |

### 1.3 使用方式

```python
# 方式1：使用 openai 库（推荐）
from openai import OpenAI

# 只需修改 base_url 和 api_key 即可切换不同厂商
client = OpenAI(
    base_url="https://api.deepseek.com/v1",  # 厂商 endpoint
    api_key="your-api-key"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)

# 方式2：使用 requests/aiohttp 直接调用 HTTP API
import requests

response = requests.post(
    "https://api.deepseek.com/v1/chat/completions",
    headers={"Authorization": "Bearer your-api-key"},
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "你好"}]
    }
)
```

### 1.4 目录结构

```
llm/
├── openai/                    # 使用 openai SDK 的封装
│   ├── providers/
│   │   ├── doubao.py         # 豆包 OpenAI 兼容接口
│   │   ├── qwen.py           # 通义千问 OpenAI 兼容接口
│   │   ├── deepseek.py       # DeepSeek OpenAI 兼容接口
│   │   └── ...               # 其他厂商
│   └── client.py
├── requests/                  # 使用 requests 的 HTTP 调用
│   └── providers/
│       ├── doubao.py
│       ├── qwen.py
│       └── ...
└── aiohttp/                   # 使用 aiohttp 的异步 HTTP 调用
    └── providers/
        ├── doubao.py
        ├── qwen.py
        └── ...
```

---

## 二、各厂商官方 SDK

### 2.1 为什么有官方 SDK？

部分厂商提供了专属的 Python SDK，原因包括：
- **历史原因**：早期未支持 OpenAI 协议
- **特殊功能**：提供协议中不支持的特有功能
- **认证方式**：使用 AK/SK 等非标准认证
- **生态建设**：构建自己的开发者生态

### 2.2 拥有官方 SDK 的厂商

| 厂商 | SDK 名称 | 安装命令 | 认证方式 | 特点 |
|------|----------|----------|----------|------|
| **字节/豆包** | volcengine-python-sdk | `pip install volcengine-python-sdk` | AK/SK | 火山引擎 MaaS 服务 |
| **百度** | qianfan | `pip install qianfan` | AK/SK | 千帆大模型平台 |
| **阿里云** | dashscope | `pip install dashscope` | API Key | 灵积模型服务 |
| **智谱 AI** | zhipuai | `pip install zhipuai` | API Key | ChatGLM 系列 |
| **Google** | google-generativeai | `pip install google-generativeai` | API Key | Gemini 系列 |
| **Cohere** | cohere | `pip install cohere` | API Key | Command 系列 |
| **Mistral** | mistralai | `pip install mistralai` | API Key | 欧洲开源模型 |
| **Groq** | groq | `pip install groq` | API Key | 超高速推理 |

### 2.3 使用方式

```python
# 以百度 qianfan 为例
import qianfan

# 使用 AK/SK 认证
os.environ["QIANFAN_AK"] = "your-ak"
os.environ["QIANFAN_SK"] = "your-sk"

# 创建客户端（与 OpenAI 接口完全不同）
chat_comp = qianfan.ChatCompletion()

# 调用方式也不同
resp = chat_comp.do(
    model="ERNIE-Bot-4",
    messages=[{"role": "user", "content": "你好"}]
)

# 响应格式也不同
print(resp["result"])  # 不是 resp.choices[0].message.content
```

### 2.4 目录结构

```
llm/
├── baidu/                     # 百度官方 SDK 封装
│   ├── client.py
│   └── providers/
│       └── wenxin.py         # 基于 qianfan SDK
├── alibaba/                   # 阿里云官方 SDK 封装
│   ├── client.py
│   └── providers/
│       └── qwen.py           # 基于 dashscope SDK
├── zhipu/                     # 智谱官方 SDK 封装
│   ├── client.py
│   └── providers/
│       └── chatglm.py        # 基于 zhipuai SDK
├── google/                    # Google 官方 SDK 封装
│   ├── client.py
│   └── providers/
│       └── gemini.py         # 基于 google-generativeai
├── cohere/                    # Cohere 官方 SDK 封装
│   ├── client.py
│   └── providers/
│       └── cohere_official.py
├── mistral/                   # Mistral 官方 SDK 封装
│   ├── client.py
│   └── providers/
│       └── mistral_official.py
├── groq/                      # Groq 官方 SDK 封装
│   ├── client.py
│   └── providers/
│       └── groq_official.py
└── volcengine/                # 火山引擎官方 SDK 封装
    ├── client.py
    └── providers/
        └── doubao.py         # 基于 volcengine-python-sdk
```

---

## 三、核心区别对比

### 3.1 接口层面

| 对比项 | OpenAI 通用协议 | 官方 SDK |
|--------|-----------------|----------|
| **接口标准** | 统一标准 | 各厂商自定义 |
| **调用方式** | HTTP REST API | Python 方法调用 |
| **认证方式** | Bearer Token (API Key) | API Key / AK+SK / OAuth |
| **参数命名** | 统一（temperature, max_tokens） | 可能不同（如 max_output_tokens） |
| **响应格式** | 统一 JSON 结构 | 各厂商自定义 |
| **错误处理** | 标准 HTTP 状态码 | SDK 自定义异常 |

### 3.2 代码层面

```python
# ========== OpenAI 通用协议 ==========
from openai import OpenAI

client = OpenAI(base_url="xxx", api_key="xxx")

# 统一接口
response = client.chat.completions.create(
    model="model-name",
    messages=[{"role": "user", "content": "你好"}],
    temperature=0.7,
    max_tokens=1000
)

# 统一响应提取
text = response.choices[0].message.content


# ========== 百度官方 SDK ==========
import qianfan

# 完全不同的初始化
chat_comp = qianfan.ChatCompletion()

# 完全不同的调用方式
response = chat_comp.do(
    model="ERNIE-Bot-4",
    messages=[{"role": "user", "content": "你好"}],
    temperature=0.7,
    max_output_tokens=1000  # 参数名不同！
)

# 完全不同的响应提取
text = response["result"]  # 不是 .choices[0].message.content
```

### 3.3 功能特性

| 特性 | OpenAI 协议 | 官方 SDK |
|------|-------------|----------|
| **流式输出** | 标准 Server-Sent Events | 各厂商实现不同 |
| **函数调用** | 标准 function calling | 部分厂商支持，格式可能不同 |
| **JSON 模式** | response_format={"type": "json_object"} | 部分 SDK 支持 |
| **多模态** | 标准 content 数组格式 | 各厂商格式不同 |
| **Embedding** | 标准 /v1/embeddings | SDK 可能有专门方法 |
| **微调** | 标准 /v1/fine_tuning | SDK 可能有专门接口 |

---

## 四、选择建议

### 4.1 何时使用 OpenAI 通用协议？

✅ **推荐使用场景：**
- 需要快速切换不同厂商模型
- 已有基于 OpenAI 接口的代码基础
- 需要统一的多厂商管理
- 只需要标准功能（文本生成、流式输出）
- 团队熟悉 OpenAI 接口规范

✅ **优势：**
- 学习成本低，一份代码适配多厂商
- 社区生态丰富，工具链完善
- 迁移成本低，切换厂商只需改 base_url
- 与 LangChain、LlamaIndex 等框架无缝集成

### 4.2 何时使用官方 SDK？

✅ **推荐使用场景：**
- 需要使用厂商特有功能
- 认证方式特殊（如 AK/SK）
- 厂商仅提供 SDK 方式（无 OpenAI 兼容接口）
- 需要更好的错误处理和调试信息
- 生产环境需要官方技术支持

✅ **优势：**
- 访问厂商全部功能
- 更好的错误提示和调试支持
- 官方维护，更新及时
- 可能有性能优化

---

## 五、项目中的封装策略

### 5.1 分层架构

```
llm/
├── openai/              # OpenAI 协议封装（推荐首选）
│   └── providers/       # 25+ 厂商支持
├── requests/            # HTTP 原生封装（轻量级）
│   └── providers/
├── aiohttp/             # 异步 HTTP 封装
│   └── providers/
├── anthropic/           # Anthropic 原生 SDK（协议不兼容）
├── baidu/               # 百度官方 SDK
├── alibaba/             # 阿里云官方 SDK
├── zhipu/               # 智谱官方 SDK
├── google/              # Google 官方 SDK
├── cohere/              # Cohere 官方 SDK
├── mistral/             # Mistral 官方 SDK
├── groq/                # Groq 官方 SDK
└── volcengine/          # 火山引擎官方 SDK
```

### 5.2 使用建议

1. **优先使用 OpenAI 协议**：大部分场景下，使用 `llm/openai/` 下的封装即可
2. **特殊需求用官方 SDK**：需要特有功能时，使用对应厂商的官方 SDK 封装
3. **统一抽象层**：在业务代码中，可以进一步封装统一接口，底层根据配置自动选择协议/SDK

### 5.3 统一调用示例

```python
# 理想的使用方式（工厂模式）
from llm import create_client

# 自动根据配置选择 OpenAI 协议或官方 SDK
client = create_client(
    provider="qwen",
    use_official_sdk=False,  # True 则使用 dashscope，False 则使用 OpenAI 协议
    api_key="your-key"
)

# 统一接口调用
response = client.generate("你好")
```

---

## 六、常见问题

### Q1: 为什么 Anthropic 单独一个目录？

Anthropic 的 Claude 虽然支持 OpenAI 兼容模式，但其原生协议是 **Messages API**，与 OpenAI 的 Chat Completions API 有本质区别。为了完整支持 Claude 的全部功能（如系统提示词的特殊处理、特有的参数等），单独封装了 `llm/anthropic/`。

### Q2: 豆包为什么既有 openai/doubao 又有 volcengine/doubao？

- `openai/doubao.py`：使用 OpenAI 兼容协议，通过 HTTP 调用
- `volcengine/doubao.py`：使用火山引擎官方 SDK（volcengine-python-sdk），通过 AK/SK 认证

两者都可以使用，根据项目需求选择：
- 快速接入、已有 OpenAI 代码基础 → 用 OpenAI 协议
- 需要火山引擎生态、AK/SK 认证 → 用官方 SDK

### Q3: 如何决定为新厂商创建哪种封装？

决策流程：
1. 厂商是否支持 OpenAI 兼容接口？
   - 是 → 在 `llm/openai/providers/` 下创建
   - 否 → 继续判断
2. 厂商是否有官方 Python SDK？
   - 是 → 在 `llm/<vendor>/` 下创建官方 SDK 封装
   - 否 → 使用 `llm/requests/` 或 `llm/aiohttp/` 直接封装 HTTP API

---

## 七、附录：厂商支持情况速查

| 厂商 | OpenAI 协议 | 官方 SDK | 推荐方式 |
|------|-------------|----------|----------|
| OpenAI | ✅ | ✅ openai | OpenAI SDK |
| Anthropic | ✅ | ✅ anthropic | Anthropic SDK |
| Google Gemini | ✅ | ✅ google-generativeai | OpenAI 协议 |
| Cohere | ✅ | ✅ cohere | OpenAI 协议 |
| Mistral | ✅ | ✅ mistralai | OpenAI 协议 |
| Groq | ✅ | ✅ groq | OpenAI 协议 |
| 阿里云/通义千问 | ✅ | ✅ dashscope | OpenAI 协议 |
| 百度/文心 | ✅ | ✅ qianfan | OpenAI 协议 |
| 字节/豆包 | ✅ | ✅ volcengine-python-sdk | OpenAI 协议 |
| 智谱/ChatGLM | ✅ | ✅ zhipuai | OpenAI 协议 |
| 月之暗面/Kimi | ✅ | ❌ | OpenAI 协议 |
| MiniMax | ✅ | ❌ | OpenAI 协议 |
| 零一万物 | ✅ | ❌ | OpenAI 协议 |
| 百川 | ✅ | ❌ | OpenAI 协议 |
| 商汤 | ✅ | ❌ | OpenAI 协议 |
| 阶跃星辰 | ✅ | ❌ | OpenAI 协议 |
| DeepSeek | ✅ | ❌ | OpenAI 协议 |
| 腾讯/混元 | ✅ | ❌ | OpenAI 协议 |
| 华为/盘古 | ✅ | ❌ | OpenAI 协议 |

---

**最后更新**：2025年5月22日
