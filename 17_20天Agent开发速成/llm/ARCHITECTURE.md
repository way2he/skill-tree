# LLM 架构说明

## 📚 设计目的

本项目作为**学习案例**，展示**多种调用大模型的方式**，并支持**自由切换底层实现**。

---

## 🏗️ 架构分层

```
用户代码 (create_llm)
      │
      ▼
┌─────────────────────────────────────────┐
│  Unified Adapter (core/adapter/)        │
│  - 统一接口                               │
│  - 不指定具体模型                           │
│  - 事件发布、错误包装                        │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴───────────────────────┐
        │  可切换的 Implementation        │
        │  (implementations/)             │
        └─────────────────┬───────────────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
┌─────────────┬─────────────┬─────────────┐
│ requests/   │ aiohttp/    │ openai_sdk/ │
│ - 同步HTTP  │ - 异步HTTP  │ - 官方SDK   │
└─────────────┴─────────────┴─────────────┘
```

---

## 📁 目录说明

### 核心层
- **core/** - 统一接口、适配器、事件系统

### 实现方式（可切换）
- **implementations/requests/** - 方式1：requests 库（默认）
- **implementations/aiohttp/** - 方式2：aiohttp 库
- **implementations/openai_sdk/** - 方式3：OpenAI SDK
- **implementations/anthropic_sdk/** - 方式4：Anthropic SDK
- **implementations/qwen_sdk/** - 方式5：通义千问 SDK
- **implementations/glm_sdk/** - 方式6：智谱 GLM SDK
- **implementations/wenxin_sdk/** - 方式7：文心一言 SDK
- **implementations/doubao_sdk/** - 方式8：豆包 SDK
- **implementations/cohere_sdk/** - 方式9：Cohere SDK
- **implementations/gemini_sdk/** - 方式10：Gemini SDK
- **implementations/groq_sdk/** - 方式11：Groq SDK
- **implementations/mistral_sdk/** - 方式12：Mistral SDK
- **implementations/ollama/** - 方式13：Ollama

### 示例和测试
- **examples/** - 使用示例
- **tests/** - 测试套件

---

## 🎯 核心功能：实现方式切换

### 方式1：使用默认实现（requests）
```python
from llm.core.factory import create_llm

llm = create_llm("openai", api_key="sk-xxx")
result = llm.generate("Hello")
```

### 方式2：切换到 aiohttp 实现
```python
from llm.core.factory import create_llm

llm = create_llm("openai", implementation="aiohttp", api_key="sk-xxx")
result = await llm.agenerate("Hello")
```

### 方式3：切换到 OpenAI SDK 实现
```python
from llm.core.factory import create_llm

llm = create_llm("openai", implementation="openai_sdk", api_key="sk-xxx")
result = llm.generate("Hello")
```

---

## 🎓 学习目的

### 1. 不同 HTTP 客户端
- `requests/` - 同步 HTTP 客户端
- `aiohttp/` - 异步 HTTP 客户端

### 2. 不同 SDK
- 直接用 API 协议（requests/aiohttp）
- 用厂商官方 SDK（openai_sdk/anthropic_sdk/...）

### 3. 架构设计学习
- Adapter 层设计
- Provider 协议
- 依赖注入
- 事件系统
- **可切换的实现方式**

---

## 💡 使用建议

### 日常使用
使用默认实现（requests），它最稳定、最完整。

### 性能优化
切换到 aiohttp 实现以获得更好的异步性能。

### 厂商特定功能
使用对应的 SDK 实现以获取厂商特定功能。

### 学习参考
查看 `implementations/` 下的不同实现方式，学习：
- 如何用不同库调用大模型
- 如何封装 SDK
- 如何实现自己的 Provider

---

## 🎉 总结

- ✅ **清晰结构**：所有实现方式集中在 `implementations/` 目录
- ✅ **自由切换**：通过 `implementation` 参数简单切换底层实现
- ✅ **向后兼容**：旧代码不需要修改
- ✅ **易于扩展**：添加新的实现方式只需在 `implementations/` 下添加新目录
