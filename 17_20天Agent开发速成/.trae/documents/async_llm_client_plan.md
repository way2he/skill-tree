# Python 异步 LLM 客户端实现计划

## 1. 项目概述

在 `llm/` 目录下创建一个全新的异步版本，使用 asyncio 和 aiohttp，支持全球和国内主流大模型，保持与现有同步版本类似的架构但完全异步化。

## 2. 支持的模型列表

| 模型提供商 | 模型名称 | API 文档 |
|------------|----------|----------|
| Ollama | 本地模型 | https://github.com/ollama/ollama/blob/main/docs/api.md |
| OpenAI (GPT) | gpt-4o, gpt-4o-mini, gpt-4, gpt-3.5-turbo | https://platform.openai.com/docs/api-reference |
| Anthropic (Claude) | claude-3-5-sonnet, claude-3-opus | https://docs.anthropic.com/claude/reference/messages |
| 火山引擎 (豆包 Doubao) | doubao-pro, doubao-seed | https://www.volcengine.com/docs/82379 |
| 阿里云 (通义千问 Qwen) | qwen-plus, qwen-max | https://help.aliyun.com/zh/dashscope/ |
| 智谱 AI (GLM) | glm-4, glm-3-turbo | https://open.bigmodel.cn/dev/api |
| 百度 (文心一言 Wenxin) | ernie-4.0, ernie-3.5 | https://cloud.baidu.com/doc/WENXINWORKSHOP |
| 月之暗面 (Kimi) | moonshot-v1 | https://platform.moonshot.cn/docs |
| 深度求索 (DeepSeek) | deepseek-chat | https://platform.deepseek.com/docs |
| MiniMax | abab6.5s-chat | https://platform.minimaxi.com/document |

## 3. 目录结构

```
llm/
├── async/                  # 新增异步版本目录
│   ├── __init__.py
│   ├── clients.py          # 所有客户端实现
│   ├── config.py           # 配置和工厂函数
│   └── utils.py            # 工具函数（异步重试等）
├── openai/                 # 现有同步版本（保留）
└── requests/               # 现有同步版本（保留）
```

## 4. 核心实现要点

### 4.1 技术栈
- **asyncio**: 异步编程基础
- **aiohttp**: 异步 HTTP 请求库
- **pydantic**: 数据验证
- **tenacity** 或自定义实现: 异步重试装饰器

### 4.2 依赖更新
在 `pyproject.toml` 中添加:
- `aiohttp>=3.9.0`
- `tenacity>=8.2.0` (可选，用于重试)

### 4.3 核心架构

1. **抽象基类 `BaseAsyncLLMClient`**
   - `async def generate(prompt: str, **kwargs) -> str`
   - `async def generate_json(prompt: str, schema: dict | None = None, **kwargs) -> str`
   - `async def generate_with_response(prompt: str, **kwargs) -> AsyncLLMResponse`

2. **响应数据模型 `AsyncLLMResponse`** (pydantic)
   - content: str
   - model: str | None
   - prompt_tokens: int | None
   - completion_tokens: int | None
   - total_tokens: int | None
   - finish_reason: str | None

3. **各个模型客户端类**
   - `AsyncOllamaClient`
   - `AsyncOpenAIClient` (兼容 Azure OpenAI)
   - `AsyncAnthropicClient`
   - `AsyncDoubaoClient`
   - `AsyncQwenClient`
   - `AsyncGLMClient`
   - `AsyncWenxinClient`
   - `AsyncKimiClient`
   - `AsyncDeepSeekClient`
   - `AsyncMiniMaxClient`

4. **工厂函数**
   - `create_async_llm_client(provider, **kwargs)`
   - `async_llm_generate()`
   - `async_llm_generate_json()`

5. **工具函数**
   - 异步重试装饰器
   - JSON 校验
   - 环境变量加载

## 5. 实现步骤

1. **创建目录结构和基础文件**
   - 创建 `llm/async/` 目录
   - 创建 `__init__.py`

2. **实现核心基础组件**
   - `AsyncLLMResponse` pydantic 模型
   - `BaseAsyncLLMClient` 抽象基类
   - 异步重试装饰器

3. **逐个实现模型客户端**
   - Ollama (最简单，本地部署)
   - OpenAI (标准 API)
   - Anthropic
   - Doubao
   - Qwen
   - GLM
   - Wenxin
   - Kimi
   - DeepSeek
   - MiniMax

4. **实现配置和工厂函数**
   - `AsyncLLMConfig` 配置类
   - `create_async_llm_client` 工厂函数
   - 便捷函数 `async_llm_generate`, `async_llm_generate_json`

5. **实现工具函数**
   - 异步重试
   - JSON 验证
   - 环境变量加载

6. **更新依赖**
   - 更新 `pyproject.toml` 添加 aiohttp

## 6. 关键特性

- 完全异步化，支持高并发
- 统一的接口设计，与同步版本保持 API 一致性
- 完善的异常处理
- 支持重试机制
- 支持流式响应 (可选)
- 支持工具调用 (function calling)

## 7. API 示例

```python
import asyncio
from llm.async import create_async_llm_client, async_llm_generate

async def main():
    # 方式1: 使用工厂函数创建客户端
    client = create_async_llm_client("ollama", model="qwen3.5:9b")
    response = await client.generate("你好，请介绍一下自己")
    print(response)
    
    # 方式2: 使用便捷函数
    response = await async_llm_generate(
        "你好",
        provider="openai",
        model="gpt-4o-mini",
        api_key="sk-xxx"
    )
    print(response)
    
    # 方式3: 生成 JSON
    json_str = await async_llm_generate_json(
        "生成一个用户对象",
        provider="doubao",
        schema={"type": "object", "properties": {"name": {"type": "string"}}}
    )
    print(json_str)

if __name__ == "__main__":
    asyncio.run(main())
```

## 8. 注意事项

- 保持与现有同步版本的架构相似，便于理解和对比学习
- 所有方法必须是 async def
- 使用 aiohttp.ClientSession 进行 HTTP 请求
- 确保正确处理超时、重试等异常情况
- 遵循用户代码规范（函数注释、类型注解、异常处理等）
