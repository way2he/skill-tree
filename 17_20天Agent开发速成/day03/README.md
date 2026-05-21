---
name: Day03 - 大模型API深度使用 + 评估指标（面试高频）
description: Day03 完整学习计划：精确到分钟，每个知识点对应面试考点，统一接口封装 + Agent效果评估
type: learning
tags: ["大模型API", "流式输出", "评估指标", "统一接口", "降级策略", "面试"]
created_at: 2026-05-21
updated_at: 2026-05-21
version: interview
---

# 🚀 Day 03：大模型 API 深度使用 + 评估指标（面试高频）

- **学习日期**：第 3 天 / 共 20 天
- **学习时长**：8 小时（精确到分钟）
- **核心目标**：能写出兼容 3 家模型的统一接口层，能设计完整的 Agent 效果评估方案，掌握 Token 成本优化

---

## ⏰ 今日学习时间表（精确到分钟）

| 时间段 | 学习内容 | 完成情况 |
|--------|---------|---------|
| **09:00-10:00** | OpenAI API 完整指南：流式/非流式、错误重试 | ⬜️ / ✅ |
| **10:00-11:00** | 国产模型对比：DeepSeek、Qwen、通义千问、文心一言 | ⬜️ / ✅ |
| **11:00-12:00** | Token 计费原理 + 成本估算 + 成本优化 5 大招 | ⬜️ / ✅ |
| **14:00-15:00** | 统一接口层封装：换模型只需要改一行配置 | ⬜️ / ✅ |
| **15:00-16:00** | 降级策略：模型挂了怎么办？怎么优雅降级？ | ⬜️ / ✅ |
| **16:00-17:00** | ML基础：评估指标（准确率、精确率、召回率、F1） | ⬜️ / ✅ |
| **19:00-20:00** | 【面试题专项】Day03 7 道大模型 API 面试题 | ⬜️ / ✅ |
| **20:00-21:00** | 复盘 + 整理面试话术 + 统一接口代码实战 | ⬜️ / ✅ |

---

## 🎯 09:00-10:00：OpenAI API 完整指南

### 📝 核心知识点 + 对应面试考点

| 知识点 | 面试考点 | 回答要点 |
|--------|---------|---------|
| **流式输出原理** | 流式输出的原理是什么？有什么好处？ | 1. SSE（Server-Sent Events）技术<br> 2. 分块生成，逐字返回，用户体验好<br> 3. 降低首字延迟（TTFT），不需要等完整生成<br> 4. 内存占用小，适合长文本生成 |
| **非流式 vs 流式** | 什么时候用流式，什么时候用非流式？ | 1. 流式：聊天、写作、实时交互场景<br> 2. 非流式：API调用、批量处理、需要完整结果才继续<br> 3. Agent内部思考：一般用非流式，用户界面：用流式 |
| **错误类型** | 大模型 API 常见错误有哪些？怎么处理？ | 1. 429：限流 → 指数退避重试<br> 2. 401：认证失败 → 检查 API Key<br>3. 400：参数错误 → 检查输入格式<br>4. 5xx：服务端错误 → 重试或降级 |

### 💻 必写代码 1：流式输出完整实现

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# 流式输出
def stream_chat(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True  # 关键参数
    )
    
    full_content = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_content += content
            print(content, end="", flush=True)  # 逐字打印
    
    return full_content

# 非流式输出
def normal_chat(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content

# 使用
messages = [{"role": "user", "content": "什么是大模型 Agent？"}]
print("流式输出：")
stream_chat(messages)
print("\n\n非流式输出：")
print(normal_chat(messages))
```

### 💻 必写代码 2：指数退避重试装饰器

```python
import time
import random
from functools import wraps

def retry_with_exponential_backoff(
    max_retries=5,
    initial_delay=1,
    max_delay=30,
    backoff_factor=2,
    jitter=True
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise  # 最后一次重试失败，抛出异常
                    
                    # 计算延迟时间
                    if jitter:
                        delay = min(max_delay, delay * backoff_factor) * random.uniform(0.5, 1.5)
                    else:
                        delay = min(max_delay, delay * backoff_factor)
                    
                    print(f"第 {attempt + 1} 次尝试失败，{delay:.1f}秒后重试：{str(e)}")
                    time.sleep(delay)
            
            return None
        return wrapper
    return decorator

# 使用
@retry_with_exponential_backoff(max_retries=5)
def chat_with_retry(messages):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
```

### ⭐ 面试官追问：指数退避为什么要加 jitter（随机抖动）？

> **3分钟回答模板**：
> 
> 指数退避加 jitter 是为了避免「惊群效应」（Thundering Herd）。假设没有 jitter，100 个请求同时遇到 429 错误，它们会在 1 秒后同时重试，然后 2 秒后又同时重试，4 秒后又同时重试... 这样会形成请求风暴，把服务打垮。
> 
> 加上随机抖动后，每个请求的重试时间会分散开，不会同时打过去，能让服务更平滑地恢复。这是分布式系统中非常经典的设计思想。

---

## 🎯 10:00-11:00：国产模型对比与选型

### 📝 核心知识点 + 对应面试考点

| 知识点 | 面试考点 | 回答要点 |
|--------|---------|---------|
| **模型选型** | 各个模型的优缺点是什么？怎么选型？ | 1. GPT-4：质量最高，但贵，速度慢<br>2. DeepSeek：性价比高，代码能力强，国产<br>3. Qwen：阿里开源，本地化部署方便<br>4. 通义千问：阿里闭源，中文好，企业服务完善<br>5. 文心一言：百度，中文理解好，有企业版 |
| **成本对比** | 不同模型的成本差异有多大？ | 1. GPT-4: ~$30 / 1M tokens<br>2. GPT-3.5: ~$1 / 1M tokens<br>3. DeepSeek: ~¥1 / 1M tokens<br>4. 国产模型普遍比 OpenAI 便宜 5-10 倍 |
| **能力差异** | 国产模型和 GPT 比，能力差距在哪里？ | 1. 复杂推理：GPT-4 明显更强<br>2. 工具调用：GPT 更稳定，国产经常参数解析失败<br>3. 中文：国产模型更好，特别是本土文化相关<br>4. 长上下文：各有千秋，DeepSeek 支持 128K |

### 📊 主流模型详细对比表

| 模型 | 价格（输入/输出） | 上下文长度 | 代码能力 | 推理能力 | 中文能力 | 推荐使用场景 |
|------|-----------------|-----------|---------|---------|---------|-------------|
| **GPT-4o** | $5 / $15 | 128K | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 复杂推理、核心逻辑 |
| **GPT-3.5-turbo** | $0.5 / $1.5 | 16K | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 普通对话、批量处理 |
| **DeepSeek-Chat** | ¥1 / ¥2 | 128K | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 性价比首选、代码相关 |
| **Qwen-Max** | ¥2 / ¥6 | 32K | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 中文场景、企业内部 |
| **通义千问 Plus** | ¥2 / ¥6 | 32K | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 阿里生态、企业服务 |
| **文心一言 4.0** | ¥8 / ¥20 | 8K | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 百度生态、合规要求 |

### 💡 选型决策树

```
开始
  ↓
有数据合规/不出境要求吗？
  ├─ 是 → 只能选国产模型
  │      ├─ 需要本地化部署 → Qwen / Llama 等开源模型
  │      └─ 不需要本地部署 → DeepSeek / 通义 / 文心
  └─ 否 → 可以用 OpenAI
         ├─ 复杂推理 / 工具调用 → GPT-4o
         └─ 普通场景 / 成本敏感 → GPT-3.5
```

---

## 🎯 11:00-12:00：Token 计费原理与成本优化

### 📝 核心知识点 + 对应面试考点

| 知识点 | 面试考点 | 回答要点 |
|--------|---------|---------|
| **Token 定义** | 1K Token 大概是多少字？中英文有区别吗？ | 1. 英文：约 750 个单词 = 1K Token<br>2. 中文：约 500 个汉字 = 1K Token（因为中文每个字占 2 个 Token）<br>3. 所以同样长度的中文，Token 消耗是英文的 1.5 倍 |
| **计费方式** | Token 是怎么计费的？输入和输出分开算吗？ | 1. 输入 Token：你的 prompt 长度，算一次<br>2. 输出 Token：模型生成的内容，算一次<br>3. 输出通常比输入贵 2-3 倍<br>4. 长上下文模型 Token 单价更贵 |
| **成本优化** | 怎么降低 Token 成本？ | 1. 用更便宜的模型（降本 5-10 倍）<br>2. 精简 System Prompt，去掉废话<br>3. 上下文压缩，只保留相关信息<br>4. 输出限制长度，不要让模型瞎扯<br>5. 批量处理，减少 API 调用次数 |

### 💻 必写代码 3：Token 计数工具

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """计算文本的 Token 数量"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def count_messages_tokens(messages: list, model: str = "gpt-3.5-turbo") -> int:
    """计算对话消息的总 Token 数量"""
    encoding = tiktoken.encoding_for_model(model)
    
    # 每轮消息有固定开销
    tokens_per_message = 3
    tokens_per_name = 1
    
    total_tokens = 0
    for message in messages:
        total_tokens += tokens_per_message
        for key, value in message.items():
            total_tokens += len(encoding.encode(value))
            if key == "name":
                total_tokens += tokens_per_name
    
    # 最后有固定的 3 个 Token 开销
    total_tokens += 3
    return total_tokens

# 使用示例
text = "你好，我想了解一下什么是大模型 Agent。"
print(f"文本 Token 数：{count_tokens(text)}")

messages = [
    {"role": "system", "content": "你是一个 helpful 的助手。"},
    {"role": "user", "content": "什么是大模型 Agent？"}
]
print(f"对话 Token 数：{count_messages_tokens(messages)}")

# 成本估算（GPT-3.5-turbo: $0.5/1M 输入，$1.5/1M 输出）
input_tokens = count_messages_tokens(messages)
output_tokens = 100  # 假设输出 100 Token
input_cost = input_tokens * 0.5 / 1_000_000
output_cost = output_tokens * 1.5 / 1_000_000
print(f"预估成本：${input_cost + output_cost:.6f}")
```

### 📊 成本优化 5 大招效果对比

| 优化方法 | 降本幅度 | 实现难度 | 对效果影响 |
|---------|---------|---------|-----------|
| 换更便宜的模型 | 50-90% | ⭐ | 可能有轻微下降 |
| 精简 System Prompt | 10-30% | ⭐⭐ | 几乎无影响 |
| 上下文压缩 | 30-70% | ⭐⭐⭐ | 可能丢失关键信息 |
| 限制输出长度 | 20-50% | ⭐ | 可控 |
| 缓存重复请求 | 0-90% | ⭐⭐⭐ | 完全相同的请求效果好 |

---

## 🎯 14:00-15:00：统一接口层封装

### 📝 核心知识点 + 对应面试考点

| 知识点 | 面试考点 | 回答要点 |
|--------|---------|---------|
| **为什么要封装** | 为什么要设计统一接口层？直接调 SDK 不行吗？ | 1. 换模型不需要改业务代码，只改配置<br>2. 统一错误处理、重试、日志<br>3. 方便添加监控和统计<br>4. 符合开闭原则：对扩展开放，对修改关闭 |
| **设计模式** | 用什么设计模式来设计统一接口层？ | 1. 策略模式：每个模型一个策略类<br>2. 工厂模式：根据配置创建对应的实例<br>3. 适配器模式：统一不同 SDK 的接口 |
| **抽象维度** | 统一接口需要抽象哪些维度？ | 1. chat 方法：输入 messages，输出响应<br>2. stream_chat 方法：流式输出<br>3. embed 方法：文本向量化<br>4. 通用参数：model, temperature, max_tokens |

### 💻 必写代码 4：统一接口层完整实现

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator

class BaseLLM(ABC):
    """LLM 抽象基类"""
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """非流式聊天"""
        pass
    
    @abstractmethod
    def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        """流式聊天"""
        pass

class OpenAILLM(BaseLLM):
    """OpenAI 模型实现"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def chat(self, messages: List